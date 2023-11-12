from classes.sensor import Sensor
import os.path

node=Sensor("localhost", 9000,"sensor_temp_bedroom", "localhost", 9014, "device_4")

try:
    information=node.publish("apt1/temperature/bedroom")
except KeyboardInterrupt:
    print("Close the execution")


