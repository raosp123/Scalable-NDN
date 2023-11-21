from classes.sensor import Sensor
import os.path
import time
import numpy as np
logging_port = 30303
node1=Sensor("localhost", 9044,"sensor_gas_cows_room", "localhost", 9002, "device_2", logging_port)
node2 = Sensor("localhost", 9045,"sensor_gas_field1", "localhost", 9003, "device_3", logging_port)
node3 = Sensor("localhost", 9046,"sensor_gas_manure_storage", "localhost", 9001, "device_1", logging_port)
node4 = Sensor("localhost", 9047,"sensor_gas_kitchen", "localhost", 9005, "device_5", logging_port)
node5 = Sensor("localhost", 9048,"sensor_gas_composting_area", "localhost", 9004, "device_4", logging_port)

try:
        # the metrics are parts per million (ppm)
        node1_item = np.random.uniform(0,3)
        node2_item = np.random.uniform(0,25)
        node3_item = np.random.uniform(0,10)
        node4_item = np.random.uniform(0,3)
        node5_item = np.random.uniform(0,1000)
        information1=node1.publish("farm1/gas/root1", node1_item)
        information2 = node2.publish("farm1/gas/field1", node2_item)
        information3 = node3.publish("farm1/gas_manure_storage", node3_item)
        information4 = node4.publish("farm1/gas/kitchen", node4_item)
        information5 = node5.publish("farm1/gas/composting_area", node5_item)

except KeyboardInterrupt:
    print("Sensor finished publishing data")


