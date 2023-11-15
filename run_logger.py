import threading
from classes.logging import LogManager

devices = [
    "device_1",
    "device_2",
    "device_3",
    "device_4",
    "device_5",
]
logging_port = 30303
def main():
    
    logger = LogManager(logging_port, devices)
    logger_window = threading.Thread(target=logger.listen)
    logger_window.start()
    logger.main_loop()

if __name__ == "__main__":
    main()