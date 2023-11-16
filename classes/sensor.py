from .node import Node
import time
import numpy as np
import json

class Sensor(Node):
    
    def __init__(self, ip, port, ID,ParentDevice_ip,ParentDevice_port,ParentDevice_id, logging_port):
        super().__init__(ip, port, ID, logging_port)
        self.set_parent_device(ParentDevice_ip,ParentDevice_port,ParentDevice_id)
        
    def set_parent_device(self, ParentDevice_ip,ParentDevice_port,ParentDevice_id):
        self.ParentDevice_ip=ParentDevice_ip
        self.ParentDevice_port=ParentDevice_port
        self.ParentDevice_id = ParentDevice_id
    
    def publish(self, data_name, item):
        # we generate random data every schedule seconds until we pause it by keyboard interrupt
        data={'type': "publish", 'tag':data_name, 'timestamp':int(time.time()), 'item': item}
        package=data
        self.send(package,self.ParentDevice_port, self.ParentDevice_id)