import threading
from classes.actuator import Actuator
import time

logging_port = 30303
node_actuator = Actuator('localhost', 9008, 'actuator_1', 'farm1/light/cows_room', ("device_5", 9005), logging_port)

def actuator_listen(actuator: Actuator):
    actuator.listen()

try:
    actuator = threading.Thread(target=actuator_listen, args=(node_actuator,))
    actuator.start()

    #node_actuator.request_data()

    while True:
        print("")
        data_query = input(r'Enter a data tag you want to query for: ').strip()
        print("")
        node_actuator.request_data(data_query)

        time.sleep(1)




except KeyboardInterrupt:
    print('Close the execution')
