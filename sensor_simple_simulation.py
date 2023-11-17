from classes.sensor import Sensor

logging_port = 30303
x = Sensor("localhost", 9034,"sensor_light_cows_room", "localhost", 9002, "device_2", logging_port)
x.publish("farm1/light/cows_room", 500)