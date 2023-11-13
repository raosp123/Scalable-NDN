from .node import Node
import time
import random
import json

class Actuator(Node):
    
    def __init__(self, ip, port, ID, dataInterests):
        super().__init__(ip,port,ID)
        self.interests=dataInterests
        self.create_keys('actuator')
        
    def request_data(self, device_port, device_id, public_key):
        message = {
            "type": "request_data",
            "tag": self.interests,
            "actuator_id": self.id,
            "actuator_port": self.port,
            "public_key":public_key
        }
        
        # sends the request message
        self.send(message, device_port, device_id)
        print(f"Request message sent to device {device_id}")
        
    # def handle_message(self, message, addr):
    #     return super().handle_message(message, addr)
        