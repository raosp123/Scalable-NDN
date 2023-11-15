from classes.sensor import Sensor
import os.path
logging_port = 30300
node=Sensor("localhost", 9000,"sensor_temp_bedroom", "localhost", 9002, "device_2", logging_port)

try:
    information=node.publish("apt1/temperature/bedroom")
except KeyboardInterrupt:
    print("Close the execution")


