import threading
from classes.actuator import Actuator
logging_port = 30303
node_actuator = Actuator('localhost', 9008, 'actuator_1', 'apt1/temperature/bedroom', ("device_5", 9005), logging_port)
def actuator_listen(actuator: Actuator):
    actuator.listen()

try:
    actuator = threading.Thread(target=actuator_listen, args=(node_actuator,))
    actuator.start()
    node_actuator.request_data()

except KeyboardInterrupt:
    print('Close the execution')
