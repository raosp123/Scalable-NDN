from classes.sensor import Sensor
import os.path
import time
import numpy as np
logging_port = 30303
node1=Sensor("localhost", 9034,"sensor_light_cows_room", "localhost", 9002, "device_2", logging_port)
node2 = Sensor("localhost", 9035,"sensor_light_greenhouse", "localhost", 9003, "device_3", logging_port)
node3 = Sensor("localhost", 9036,"sensor_light_bedroom", "localhost", 9001, "device_1", logging_port)
node4 = Sensor("localhost", 9037,"sensor_light_storage_equipment", "localhost", 9005, "device_5", logging_port)
node5 = Sensor("localhost", 9038,"sensor_light_gate", "localhost", 9004, "device_4", logging_port)

try:
        # the metrics are in LUX
        node1_item = np.random.uniform(10000,20000)
        node2_item = np.random.uniform(20000,100000)
        node3_item = np.random.uniform(500,2000)
        node4_item = np.random.uniform(200,500)
        node5_item = np.random.uniform(10000,20000)
        information1=node1.publish("farm1/light/cows_room", node1_item)
        information2 = node2.publish("farm1/light/greenhouse", node2_item)
        information3 = node3.publish("farm1/light/bedroom", node3_item)
        information4 = node4.publish("farm1/light/storage_equipment", node4_item)
        information5 = node5.publish("farm1/light/gate", node5_item)
except KeyboardInterrupt:
    print("Sensor finished publishing data")


