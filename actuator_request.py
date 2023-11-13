import threading
from classes.actuator import Actuator

node_actuator = Actuator('localhost', 9008, 'actuator_1', 'apt1/temperature/bedroom')
def actuator_listen(actuator: Actuator):
    actuator.listen()

try:
    actuator = threading.Thread(target=actuator_listen, args=(node_actuator,))
    actuator.start()
    node_actuator.request_data(9002, 'device_2', f"public_key{node_actuator.id}.pem")

except KeyboardInterrupt:
    print('Close the execution')
