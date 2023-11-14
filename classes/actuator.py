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
        message = {
            "type": "request_data",
            "tag": self.interests,
            "actuator_id": self.id,
            "actuator_port": self.port
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

        