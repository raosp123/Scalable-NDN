from .node import Node
from .route_getter import RouteGetter
import json
import os.path
import time
import base64

class Device(Node):
    def __init__(self,ip,port,ID, logging_port):
        super().__init__(ip, port, ID, logging_port)
        # The data Store needs to store the data kept by data name, so that when another actuator or device asks
        # for it has a way to know if it has it
        self.routing_table = RouteGetter()
        self.interest_table={}
        self.data_storage={}
        self.actuator_buffer={}

        self.log(f'I am device {self.id}')
        
    
    ### TODO: Handle errors that might occur from inccorect formatting of the data
    def handle_message(self, message, addr):        
        type = message['type']
        if type=="publish":
            self.log("Recieved publish packet: " + str(message))
            self.update_data_store(message)
        elif type=="data_request":
            self.log("Recieved request packet: " + str(message))
            # When we find the data in the datastore
            self.handle_data_request(message)    
        elif type == "interest_gossip":
            stored = self.data_exists(message["tag"])
            if not stored:
                self.log("Recieved gossip packet: " + str(message))
                self.save_gossip_data(message)
                self.forward_gossip_data(message)
        else:
            self.log("Recieved unrecognised packet: " + str(message))
            return False # failed to decrypt

    ## When sensor uploads data, store it and start the gossip process   
    def update_data_store(self, message):
        message.pop("type")
        tag=message.pop('tag')
        if not self.data_exists(tag):
            self.interest_table[tag] = self.id
            self.data_storage[tag] = {}
            self.create_gossip_data(tag)
        timestamp=message.pop('timestamp')
        content=message
        ## TODO: make data class with complex functionality
        self.data_storage[tag].update({timestamp: content.pop("item")})
        # Make sure to manage time stamp to delete old versions every so often

    ## When actuator requests data
    def handle_data_request(self, message):
        tag = message['tag']
        step = message['step']


        if int(step) == 1: #from actuator -> device
            self.update_actuator_buffer(message)
            if self.data_exists(tag):
                # if we have the data ourselves
                if tag in self.data_storage.keys():
                    self.log(f'I have the data requested from {message["src"]}')

                    message = {
                        "type": "data_request",
                        "step": 1,
                        "tag": message["tag"],
                        "data": self.data_storage[tag],
                        "src": self.id,
                        "dst": ""
                    }

                    self.return_data_to_actuator(message) #return to actuator

                else:
                    message = {
                        "type": "data_request",
                        "step": 2,
                        "tag": message["tag"],
                        "data": "",
                        "src": self.id,
                        "dst": self.interest_table[tag]
                    }
                    
                    device_id, device_port = self.routing_table.get_next_hop(self.id, message["dst"])
                    success = self.try_send(message, device_port, device_id, message["dst"])
                    if not success:
                        message = {
                            "type": "data_request",
                            "step": 3,
                            "tag": message["tag"],
                            "data": f"Node {message['dst']} couldn't be accessed",
                            "src": self.id,
                            "dst": message["src"]
                        }
                        
                        device_id, device_port = self.routing_table.get_next_hop(self.id, message["src"])
                        success = self.try_send(message, device_port, device_id, message["dst"])
                        
            else:
                self.log(f"There is no data {tag} in the network")
                deny_message = {
                    "type": "data_not_found",
                    "tag": "none"
                }
                actuator_id, actuator_port = message["src"]
                self.try_send(deny_message, actuator_port, actuator_id)
        elif int(step) ==  2:

            #if we are the device with the requested data, change step and set dst as original device
            if self.id == message["dst"]: 
                self.log(f'I have the data requested from {message["src"]}')  
                message = {
                        "type": "data_request",
                        "step": 3,
                        "tag": message["tag"],
                        "data": self.data_storage[tag],
                        "src": self.id,
                        "dst": message["src"]
                }

            device_id, device_port = self.routing_table.get_next_hop(self.id, message["dst"])
            self.log(f'forwarding request to {message["dst"]}, next hop is {device_id}') 
            self.try_send(message, device_port, device_id, message["dst"])

        elif int(step) ==  3:
                # if I am the final destination, check my actuator buffer, then send to all actuators

                if self.id == message["dst"]:
                    self.log(f'I have received the data from {message["src"]}, now sending to my actuators')
                    self.return_data_to_actuator(message)
                    
                else:
                    device_id, device_port = self.routing_table.get_next_hop(self.id, message["dst"])
                    self.log(f'I am not the destination for the data forwarding to {message["dst"]}, next hop is {device_id}')
                    self.try_send(message, device_port, device_id, message["dst"])

        else:
            print("incorrect step index found in packet")


    # function saves ongoing data requests for actuators or deletes an interest tag from the buffer
    def update_actuator_buffer(self, message, delete=False):

        tag = message["tag"]
        if not delete:
            
            if not (tag in self.actuator_buffer):

                self.actuator_buffer[tag] = []

            self.actuator_buffer[tag].append(message["src"])
        else:
            self.actuator_buffer.pop(tag)
           
        self.log(f"tag {'added' if not delete else 'deleted'}Actuator Buffer:\n{self.actuator_buffer}")
        

    # called by the device who has the data, starts sending back to original src
    def return_data_to_actuator(self, message):

        #send data to actuator
        for actuator_id, actuator_port in self.actuator_buffer[message["tag"]]:

            self.try_send(message, actuator_port, actuator_id)
            self.log(f"Data sent back to {actuator_id}")

        self.update_actuator_buffer(message, delete=True)

    ## Create and send gossip packet to adjecent peers
    def create_gossip_data(self, tag):
        gossip_packet = {
            "type": "interest_gossip",
            "tag": tag,
            "device_id": self.id
        }
        self.forward_gossip_data(gossip_packet)

    ## send gossip packet to adjecent peers
    def forward_gossip_data(self, packet):
        ## sends to each direct one hop peers unless it is the original packet creator
        counter = 0 
        for device_key in self.routing_table.keys(self.id):
            counter += 1
            if device_key == packet["device_id"]: continue
            
            # if using portmaps, read id and port separately
            device_id, device_port = self.routing_table.get_next_hop(self.id, device_key)
            if  device_key == device_id:
                # self.log(f'Sending gossip packet to peer {device_key}')
                # keep trying to send gossip packet for 20 attempts, handles the case where device might be working, but cannot connect to any peer
                self.try_send(packet, device_port, device_id)

    def save_gossip_data(self, gossip_data):
        self.interest_table[gossip_data["tag"]] = gossip_data["device_id"]
        

    def data_exists(self, tag):
        ## Check the interest table for presence of this data type
        data_types = self.interest_table.keys()
        if tag in data_types:
            return True
        
        return False
    
    def try_send(self, packet, port, id, specific_dest = None):
        temp_router = self.routing_table
        attempts = 0
        while attempts <= 20:
            attempts += 1
            try:
                self.send(packet, port, id)
                return True
            except Exception as e:
                if specific_dest == id:
                    return False

            if specific_dest:
                try:
                    temp_router.remove_from_graph(id)
                    id, port = temp_router.get_next_hop(self.id, specific_dest)
                except Exception:
                    return False
                
                
        
        return False