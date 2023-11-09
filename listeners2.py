from classes.device import Device
import threading

devices = [
    (9001, "device_1"),
    (9002, "device_2"),
    # (9003, "device_3"),
    # (9004, "device_4"),
    # (9005, "device_5"),
]

def create_listner(port, device_id):
    device = Device("localhost", port, device_id)
    print(f"Created {device_id} on port {port}")
    try:
        device.listen()
    except KeyboardInterrupt:
        print("We have finished this method")


if __name__ == "__main__":

    create_listner(9002, "device_2")

    # for port, name in devices:
    #     device_thread = threading.Thread(target=create_listner, args=(port, name))
    #     device_thread.start()