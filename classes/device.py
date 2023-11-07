from .node import Node
import json

class Device(Node):
    def __init__(self,ip,port,ID ):
        super().__init__(ip, port, ID)
        # The data Store needs to store the data kept by data name, so that when another actuator or device asks
        # for it has a way to know if it has it
        self.routing_table={}
        self.interest_table={}
        self.data_storage={}
        self.search_buffer = {}
        # We need to add the interest table
        # We also need to add available connections
    
    ### TODO: Handle errors that might occur from inccorect formatting of the data
    def handle_message(self, message, addr):
        message=json.loads(message)
        type = message.pop('type')
        if type=="publish":
            self.update_data_store(message)
        elif type=="request":
            # When we find the data in the datastore
            self.find_data_for_actuator()    
        elif type == "gossip":
            stored = self.data_exists(message["tag"])
            if not stored:
                pass
            pass   

    ## When sensor uploads data    
    def update_data_store(self, message):
        print(self.interest_table)
        tag=message.pop('tag')
        if not self.data_exists(tag):
            self.interest_table[tag] = self.id
            self.data_storage[tag] = {}
            self.create_gossip_data(tag)
        timestamp=message.pop('timestamp')
        content=message
        ## TODO: make data class with complex functionality
        self.data_storage[tag].update({timestamp: content.pop("item")})
        print(json.dumps(self.data_storage, indent=4))
        # Make sure to manage time stamp to delete old versions every so often

    ## When actuator requests data
    def find_data_for_actuator(self, message):
        pass
    
    ## When another device wants to find data
    def find_data_for_device(self, message):
        pass 

    ## When data is to be sent to a device
    def forward_data_to_device(self):
        pass

    ## Create and send gossip packet to adjecent peers
    def create_gossip_data(self, tag):
        gossip_packet = {
            "type": "gossip",
            "tag": tag,
            "device_id": self.id
        }
        self.forward_gossip_data(json.dumps(gossip_packet).encode("utf-8"))

    ## send gossip packet to adjecent peers
    def forward_gossip_data(self, packet, stored = False):
        ## doesnt send the packet if it already has the data in its interest table
        if stored: return
        
        ## sends to each direct one hop peers unless it is the original packet creator
        for device_key in self.routing_table.keys():
            if device_key == packet["device_id"]: continue
            device_id, device_port = self.routing_table[device_key]
            if  device_key == device_id:
                self.send(packet, device_port)

    def save_gossip_data(self, packet):
        gossip_data = json.loads(packet.decode("utf-8"))
        pass

        

    def data_exists(self, tag):
        ## Check the interest table for presence of this data type
        data_types = self.interest_table.keys()
        if tag in data_types:
            return True
        
        return False