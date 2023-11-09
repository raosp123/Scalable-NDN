from .node import Node
import time
import random
import json

class Sensor(Node):
    
    def __init__(self, ip, port, ID,ParentDevice_ip,ParentDevice_port):
        super().__init__(ip, port, ID)
        self.set_parent_device(ParentDevice_ip,ParentDevice_port)
        
    def set_parent_device(self, ParentDevice_ip,ParentDevice_port):
        self.ParentDevice_ip=ParentDevice_ip
        self.ParentDevice_port=ParentDevice_port
    
    def publish(self, data_name):
        data={'type': "publish", 'tag':data_name, 'timestamp':int(time.time()), 'item': random.uniform(10, 40)}
        package=json.dumps(data)
        self.send(package,self.ParentDevice_port)