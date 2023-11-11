from .node import Node
import time
import random
import json


class Actuator(Node):
    
    def __init__(self, ip, port, ID, dataInterests):
        super().__init__(ip,port,ID)
        self.interests=dataInterests
        
    def request_data(self, device_port, device_id):
        
        message = {
            "type": "request_data",
            "tag": self.interests,
            "actuator_id": self.id
        }
        
        # sends the request message
        self.send(json.dumps(message), device_port, device_id)
        print(f"Request message sent to device {device_id}")