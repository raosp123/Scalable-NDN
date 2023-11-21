from classes.sensor import Sensor
import time

logging_port = 30303
Sensor = Sensor("localhost", 9034,"sensor_light_cows_room", "localhost", 9002, "device_2", logging_port)


try:
    
    #node_actuator.request_data()

    while True:

        data_input = input(r'Enter a data tag you want to add to the system: ').strip()
        print("")
        data_value = input(r'Now enter a value, timestamp is calculated automatically: ').strip()
        print("")
        Sensor.publish(data_input, data_value)

        time.sleep(1)




except KeyboardInterrupt:
    print('Close the execution')