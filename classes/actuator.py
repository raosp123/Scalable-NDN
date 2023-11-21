import sys
from .node import Node
import time
import random
import json

class Actuator(Node):
    
    def __init__(self, ip, port, ID, dataInterests, parent_device, logging_port):
        super().__init__(ip,port,ID,logging_port)
        self.interests=dataInterests
        self.parent = parent_device
        
    def request_data(self, tag):

        #reformat this to case 1

        

        message = {
            "type": "data_request",
            "step": 1,
            "tag": tag,
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
        else:
            print(message)
            

        