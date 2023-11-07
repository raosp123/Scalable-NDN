from .node import Node, Data
import json

class Device(Node):
    def __init__(self,ip,port,ID ):
        super().__init__(ip, port, ID)
        # The data Store needs to store the data kept by data name, so that when another actuator or device asks
        # for it has a way to know if it has it
        self.dataStorage=[]
        self.search_buffer = {}
        # We need to add the interest table
        # We also need to add available connections
    
    ### TODO: Handle errors that might occur from inccorect formatting of the data
    def handle_message(self, message, addr):
        message=json.loads(message)
        type1=message.pop('type')
        if type1=="publish":
            self.add_to_store(message)
        elif type1=="request":
            # When we find the data in the datastore
            self.send("Found this data", addr[1])           

    ## When sensor uploads data     
    def add_to_store(self, message):
        tag=message.pop('tag')
        timestamp=message.pop('timestamp')
        content=message
        data=Data(tag, timestamp, content)
        # Make sure to manage time stamp to delete old versions every so often
        self.dataStorage.append(data)

    ## When actuator requests data
    def find_data_for_actuator(self, message):
        pass
    
    ## When another device wants to find data
    def find_data_for_device(self, message):
        pass

    ## When data is to be sent to a device
    def forward_data_to_device():
        pass