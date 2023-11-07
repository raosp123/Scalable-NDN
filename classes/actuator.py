from .node import Node
import time
import random
import json


class Actuator(Node):
    
    def __init__(self, ip, port, ID, dataInterests):
        super().__init__(ip,port,ID)
        self.interests=dataInterests
        
        