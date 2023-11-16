from classes.sensor import Sensor
import os.path
import time
import numpy as np
logging_port = 30303
node1=Sensor("localhost", 9039,"sensor_soil_moisture_root1", "localhost", 9002, "device_2", logging_port)
node2 = Sensor("localhost", 9040,"sensor_soil_moisture_field1", "localhost", 9003, "device_3", logging_port)
node3 = Sensor("localhost", 9041,"sensor_soil_moisture_dripirrigation1", "localhost", 9001, "device_1", logging_port)
node4 = Sensor("localhost", 9042,"sensor_soil_moisture_garden", "localhost", 9005, "device_5", logging_port)
node5 = Sensor("localhost", 9043,"sensor_soil_moisture_greenhouse_bed", "localhost", 9004, "device_4", logging_port)

try:
    while True:
        # the metrics are in percentage between (0,1)
        node1_item = np.random.uniform(0,1)
        node2_item = np.random.uniform(0,1)
        node3_item = np.random.uniform(0,1)
        node4_item = np.random.uniform(0,1)
        node5_item = np.random.uniform(0,1)
        information1=node1.publish("farm1/soil_moisture/root1", node1_item)
        information2 = node2.publish("farm1/soil_moisture/field1", node2_item)
        information3 = node3.publish("farm1/soil_moisture_dripirrigation1", node3_item)
        information4 = node4.publish("farm1/soil_moisture/garden", node4_item)
        information5 = node5.publish("farm1/soil_moisture/greenhouse_bed", node5_item)
        time.sleep(240)
except KeyboardInterrupt:
    print("Sensor finished publishing data")


