from classes.actuator import Actuator

node_actuator = Actuator('localhost', 9008, 'actuator_1', 'apt1/temperature/bedroom')

try:
    sent = node_actuator.request_data(9004, 'device_4')
except KeyboardInterrupt:
    print('Close the execution')
