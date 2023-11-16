from classes.device import Device
import multiprocessing

logging_port = 30303

devices = [
    (9005, "device_5")]
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



if __name__ == "__main__":

    for port, name in devices:
        device_process = multiprocessing.Process(target=create_listner, args=(port, name))
        device_process.start()
    