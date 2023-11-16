from classes.sensor import Sensor
import os.path
import time
import numpy as np
logging_port = 30303
node1=Sensor("localhost", 9024,"sensor_wind_field1", "localhost", 9002, "device_2", logging_port)
node2 = Sensor("localhost", 9025,"sensor_wind_crop_canopy", "localhost", 9003, "device_3", logging_port)
node3 = Sensor("localhost", 9026,"sensor_wind_grazing_area", "localhost", 9001, "device_1", logging_port)
node4 = Sensor("localhost", 9027,"sensor_wind_storage_equipment", "localhost", 9005, "device_5", logging_port)
node5 = Sensor("localhost", 9028,"sensor_wind_vineyard", "localhost", 9004, "device_4", logging_port)

try:
    while True:
        # the metrics are in m/s
        node1_item = np.random.uniform(0,8)
        node2_item = np.random.uniform(0,5)
        node3_item = np.random.uniform(0,10)
        node4_item = np.random.uniform(0,7)
        node5_item = np.random.uniform(0,4.8)
        information1=node1.publish("farm1/wind/field1", node1_item)
        information2 = node2.publish("farm1/wind/crop_canopy", node2_item)
        information3 = node3.publish("farm1/wind/grazing_area", node3_item)
        information4 = node4.publish("farm1/wind/storage_equipment", node4_item)
        information5 = node5.publish("farm1/wind/vineyard", node5_item)
        time.sleep(40)
except KeyboardInterrupt:
    print("Sensor finished publishing data")


