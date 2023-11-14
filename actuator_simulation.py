import threading
from classes.actuator import Actuator

node_actuator = Actuator('localhost', 9008, 'actuator_1', 'apt1/temperature/bedroom', ("device_2", 9002))
def actuator_listen(actuator: Actuator):
    actuator.listen()

try:
    actuator = threading.Thread(target=actuator_listen, args=(node_actuator,))
    actuator.start()
    node_actuator.request_data()

except KeyboardInterrupt:
    print('Close the execution')
