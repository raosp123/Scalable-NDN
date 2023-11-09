from classes.sensor import Sensor
import os.path

node=Sensor("localhost", 9000,"sender", "localhost", 9004)

try:
    information=node.publish("apt1/temperature/bedroom")
except KeyboardInterrupt:
    print("Close the execution")


