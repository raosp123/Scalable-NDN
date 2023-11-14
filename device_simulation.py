from classes.device import Device
from classes.debug_window import DebugManager
import threading

devices = [
    (9001, "device_1"),
    (9002, "device_2"),
    (9003, "device_3"),
    (9004, "device_4"),
    (9005, "device_5"),
]
device_list = []
def create_listner(port, device_id, debugger):
    device = Device("localhost", port, device_id, debugger)
    device_list.append(device)
    print(f"Created {device_id} on port {port}")
    try:
        device.listen()
    except KeyboardInterrupt:
        print("We have finished this method")
        device.close()


def close_devices():
    for device in device_list:
        device.close()


if __name__ == "__main__":
    debugger = DebugManager(devices, close_devices)


    for port, name in devices:
        device_thread = threading.Thread(target=create_listner, args=(port, name, debugger))
        device_thread.start()
    
    debugger.main_loop()