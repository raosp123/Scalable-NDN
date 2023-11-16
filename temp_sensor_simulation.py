from classes.sensor import Sensor
import os.path
import time
import numpy as np
logging_port = 30303
node1=Sensor("localhost", 9000,"sensor_temp_cows_room", "localhost", 9002, "device_2", logging_port)
node2 = Sensor("localhost", 9020,"sensor_temp_greenhouse", "localhost", 9003, "device_3", logging_port)
node3 = Sensor("localhost", 9021,"sensor_temp_barn", "localhost", 9001, "device_1", logging_port)
node4 = Sensor("localhost", 9022,"sensor_temp_storage_equipment", "localhost", 9005, "device_5", logging_port)
node5 = Sensor("localhost", 9023,"sensor_temp_water_tank", "localhost", 9004, "device_4", logging_port)

try:
    while True:
        # the metrics are in degrees
        node1_item = np.random.uniform(10,40)
        node2_item = np.random.uniform(0,30)
        node3_item = np.random.uniform(30,40)
        node4_item = np.random.uniform(5,25)
        node5_item = np.random.uniform(0,20)
        information1=node1.publish("farm1/temperature/cows_room", node1_item)
        information2 = node2.publish("farm1/temperature/greenhouse", node2_item)
        information3 = node3.publish("farm1/temperature/barn", node3_item)
        information4 = node4.publish("farm1/temperature/storage_equipment", node4_item)
        information5 = node5.publish("farm1/temperature/water_tank", node5_item)
        time.sleep(20)
except KeyboardInterrupt:
    print("Sensor finished publishing data")


