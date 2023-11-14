from classes.debug_window import DebugManager
from .node import Node
import json
import os.path
import time
import base64

class Device(Node):
    def __init__(self,ip,port,ID, debugger: DebugManager):
        super().__init__(ip, port, ID)
        self.debugger = debugger
        # The data Store needs to store the data kept by data name, so that when another actuator or device asks
        # for it has a way to know if it has it
        self.routing_table={}
        self.interest_table={}
        self.data_storage={}
        self.actuator_buffer={}

        #for testing only, fills routing table with "device_X": (next_hop, port), this works with the current gossip implementation
        self.initialize_routing_table()

        self.debug(f'I am device {self.id} with routing table: {self.routing_table}')
        
        # We need to add the interest table
        # We also need to add available connections
    
    ### TODO: Handle errors that might occur from inccorect formatting of the data
    def handle_message(self, message, addr):        
        type = message['type']
        if type=="publish":
            self.debug("Recieved publish packet: " + str(message))
            self.update_data_store(message)
        elif type=="data_request":
            self.debug("Recieved request packet: " + str(message))
            # When we find the data in the datastore
            self.handle_data_request(message)    
        elif type == "interest_gossip":
            stored = self.data_exists(message["tag"])
            if not stored:
                self.debug("Recieved gossip packet: " + str(message))
                self.save_gossip_data(message)
                self.forward_gossip_data(message)
        else:
            self.debug("Recieved unrecognised packet: " + str(message))
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

        match step:

            case 1: #from actuator -> device
                try:
                    self.update_actuator_buffer(message)
                    if self.data_exists(tag):
                        # if we have the data ourselves
                        if tag in self.data_storage.keys():
                            self.debug(f'I have the data requested from {message["src"]}')

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
                            # if there is already a request for this data, don't send packet
                            message = {
                                "type": "data_request",
                                "step": 2,
                                "tag": message["tag"],
                                "data": "",
                                "src": self.id,
                                "dst": self.interest_table[tag]
                            }
                            
                            device_id, device_port = self.routing_table[message["dst"]]
                            self.send(message, device_port, device_id)
                    else:
                        self.debug(f"There is no data {tag} in the network")
                        deny_message = {
                            "type": "data_not_found",
                            "tag": "none"
                        }
                        actuator_id, actuator_port = message["src"]
                        self.send(deny_message, actuator_port, actuator_id)
                except Exception as e:
                    print(f'failed to send data back to actuator, Error:\n {e}')
            case 2:

                #if we are the device with the requested data, change step and set dst as original device
                if self.id == message["dst"]: 
                    self.debug(f'I have the data requested from {message["src"]}')  
                    message = {
                            "type": "data_request",
                            "step": 3,
                            "tag": message["tag"],
                            "data": self.data_storage[tag],
                            "src": self.id,
                            "dst": message["src"]
                    }

                device_id, device_port = self.routing_table[message["dst"]]
                self.debug(f'forwarding request to {message["dst"]}, next hop is {device_id}') 
                self.send(message, device_port, device_id)

            case 3:
                    # if I am the final destination, check my actuator buffer, then send to all actuators

                    if self.id == message["dst"]:
                        self.debug(f'I have received the data from {message["src"]}, now sending to my actuators')
                        self.return_data_to_actuator(message)
                        
                    else:
                        device_id, device_port = self.routing_table[message["dst"]]
                        self.debug(f'I am not the destination for the data forwarding to {message["dst"]}, next hop is {device_id}')
                        self.send(message, device_port, device_id)

            case _:
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
           
        self.debug(f"tag {'added' if not delete else 'deleted'}Actuator Buffer:\n{self.actuator_buffer}")
        

    # called by the device who has the data, starts sending back to original src
    def return_data_to_actuator(self, message):

        #send data to actuator
        for actuator_id, actuator_port in self.actuator_buffer[message["tag"]]:

            self.send(message, actuator_port, actuator_id)
            self.debug(f"Data sent back to {actuator_id}")

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
        for device_key in self.routing_table.keys():
            counter += 1
            if device_key == packet["device_id"]: continue
            
            # if using portmaps, read id and port separately
            device_id, device_port = self.routing_table[device_key] 
            if  device_key == device_id:
                self.debug(f'Sending gossip packet to peer {device_key}')
                gossip_sent = False
                max_tries = 20
                # keep trying to send gossip packet for 20 attempts, handles the case where device might be working, but cannot connect to any peer
                for i in range(0, max_tries):
                    if not gossip_sent:
                        try:
                            self.send(packet, device_port, device_id)
                        except:
                            self.debug(f'failed to send gossip packet to {device_id}, waiting 3s before trying again')
                            time.sleep(3)
                            continue
                        gossip_sent = True

    def save_gossip_data(self, gossip_data):
        self.interest_table[gossip_data["tag"]] = gossip_data["device_id"]
        
    def initialize_routing_table(self):
        # for testing only, initialize routing info
        with open(os.path.join((os.path.split(os.path.dirname(__file__))[0]), "routing_data/peer_config_tuples.json")) as json_file:
            data = json.load(json_file)
            self.routing_table = data[f'{self.id}_peer_table']

    def data_exists(self, tag):
        ## Check the interest table for presence of this data type
        data_types = self.interest_table.keys()
        if tag in data_types:
            return True
        
        return False
    
    def debug(self, text):
        try:
            self.debugger.debug(self.id, str(text))
        except Exception as e : 
            print("Failed to debug", e)