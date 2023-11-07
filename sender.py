from classes.sensor import Sensor

node=Sensor("localhost", 9000,"sender", "localhost", 8888)
try:
    information=node.publish("information")
except KeyboardInterrupt:
    print("Close the execution")


