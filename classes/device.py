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
        self.search_buffer = {}

        #for testing only, fills routing table with "device_X": (next_hop, port), this works with the current gossip implementation
        self.initialize_routing_table()

        self.debug(f'I am device {self.id} with routing table: {self.routing_table}')
        


        # We need to add the interest table
        # We also need to add available connections
    
    ### TODO: Handle errors that might occur from inccorect formatting of the data
    def handle_message(self, message, addr):
        message=json.loads(message)
        type = message['type']
        if type=="publish":
            self.update_data_store(message)
        elif type=="request_data":
            # When we find the data in the datastore
            print(f"Device {self.id} is looking for your data")
            self.find_data_for_actuator(message)    
        elif type == "interest_gossip":
            stored = self.data_exists(message["tag"])
            if not stored:
                self.save_gossip_data(message)
                self.forward_gossip_data(message)
        else:
            return False # failed to decrypt
        self.debug(self.interest_table)

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
    def find_data_for_actuator(self, message):
        tag = message['tag']
        actuator_key = message['public_key']
        # this means we know where the data is because there is some data
        if self.data_exists(tag):
            # this means we have the data then we just send it back
            if tag in self.data_storage.keys():
                data_encrypted = self.encrypt(self.data_storage[tag], actuator_key, 'actuator')
                encoded_data = base64.b64encode(data_encrypted)
                print(f"I am going to send {encoded_data}")
                self.send("hello",message['actuator_port'],message['actuator_id'])
                print(f"Data sent back to {message['actuator_id']}")
            else:
                # this means we need to ask other devices
                pass
                self.find_data_for_device()
        
        # this means there is no data with data tag
        else:
            print(f"There is no data {tag} in the network")
        

    
    ## When another device wants to find data
    def find_data_for_device(self, message):
        pass 

    ## When data is to be sent to a device
    def forward_data_to_device(self):
        pass

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
        for device_key in self.routing_table.keys():
            if device_key == packet["device_id"]: continue
            print(f'Sending gossip packet to peer {device_key}')
            # if using portmaps, read id and port separately
            device_id, device_port = self.routing_table[device_key] 
            if  device_key == device_id:
                gossip_sent = False
                max_tries = 20
                # keep trying to send gossip packet for 20 attempts, handles the case where device might be working, but cannot connect to any peer
                for i in range(0, max_tries):
                    if not gossip_sent:
                        try:
                            print(device_port)
                            self.send(json.dumps(packet), device_port, device_id)
                        except:
                            print(f'failed to send gossip packet to {device_id}, waiting 3s before trying again')
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