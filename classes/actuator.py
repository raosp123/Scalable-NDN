import sys
from .node import Node
import time
import random
import json

class Actuator(Node):
    
    def __init__(self, ip, port, ID, dataInterests, parent_device):
        super().__init__(ip,port,ID)
        self.interests=dataInterests
        self.parent = parent_device
        
    def request_data(self):

        #reformat this to case 1
        message = {
            "type": "data_request",
            "step": 1,
            "tag": self.interests,
            "data": "",
            "src": (self.id,self.port),
            "dst": ""
        }
        
        # sends the request message
        self.send(message, self.parent[1], self.parent[0])
        print(f"Request message sent to device {self.parent[0]}")
        
    def handle_message(self, message, addr):
        if message["type"] == "data_not_found":
            print(message["type"])
            self.close()
        else:
            print(message)
            self.close()

        