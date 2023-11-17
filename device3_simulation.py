from classes.device import Device
import multiprocessing

logging_port = 30303

devices = [
    (9003, "device_3")]
device_list = []
def create_listner(port, device_id):
    device = Device("localhost", port, device_id, logging_port)
    device_list.append(device)
    print(f"Created {device_id} on port {port}")
    try:
        device.listen()
    except KeyboardInterrupt:
        print("We have finished this method")
        device.close()



create_listner(9003, "device_3")