from classes.sensor import Sensor
import os.path
import time
import numpy as np
logging_port = 30303
node1=Sensor("localhost", 9029,"sensor_dust_cows_room", "localhost", 9002, "device_2", logging_port)
node2 = Sensor("localhost", 9030,"sensor_dust_field1", "localhost", 9003, "device_3", logging_port)
node3 = Sensor("localhost", 9031,"sensor_dust_main_gate", "localhost", 9001, "device_1", logging_port)
node4 = Sensor("localhost", 9032,"sensor_dust_construction_area", "localhost", 9005, "device_5", logging_port)
node5 = Sensor("localhost", 9033,"sensor_dust_vineyard", "localhost", 9004, "device_4", logging_port)

try:
        # the metrics are in micrograms/m^3
        node1_item = np.random.uniform(0,30)
        node2_item = np.random.uniform(0,15)
        node3_item = np.random.uniform(0,60)
        node4_item = np.random.uniform(0,100)
        node5_item = np.random.uniform(0,25)
        information1=node1.publish("farm1/dust/cows_room", node1_item)
        information2 = node2.publish("farm1/dust/field1", node2_item)
        information3 = node3.publish("farm1/dust/main_gate", node3_item)
        information4 = node4.publish("farm1/dust/construction_area", node4_item)
        information5 = node5.publish("farm1/dust/vineyard", node5_item)
except KeyboardInterrupt:
    print("Sensor finished publishing data")


