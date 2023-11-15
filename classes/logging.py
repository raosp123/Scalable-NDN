import json
import re
import socket
import sys 
import threading
import time
from tkinter import *
from tkinter import ttk

class LogManager:
    def __init__(self, port, device_list):
        self.port = port
        self.parent_window = Tk()
        self.parent_window.title("Log Viewer")
        self.tab_controller =  ttk.Notebook(self.parent_window)
        self.device_logs = {}

        for device in device_list:
            self.device_logs[device] = DeviceLog(device, self.parent_window, self.tab_controller)

    def log(self, conn: socket):
        message = conn.recv(2048)
        message = json.loads(message.decode('utf-8'))

        device = message["device_name"]
        log_statement = message["log_statement"]

        self.device_logs[device].update_log(log_statement)
        conn.close()

    def listen(self):
        self.log_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log_listener.bind(("localhost", self.port))
        self.log_listener.listen(50)

        try:
            while True:
                conn, _ = self.log_listener.accept()
                thread = threading.Thread(target=self.log, args=(conn,))
                thread.start()
        except KeyboardInterrupt and OSError:
                sys.exit(0)

    def main_loop(self):
        def update():
            self.parent_window.after(100, update)
        def close():
            self.parent_window.destroy()
            self.log_listener.shutdown(0)

            

        self.parent_window.protocol("WM_DELETE_WINDOW", close)
        self.parent_window.after(100, update)
        self.parent_window.mainloop()



class DeviceLog:
    def __init__(self, device_name, parent_window, tab_controller):
        self.device_name = device_name
        self.device_log = []
        self.log_text_widgets = []
        
        self.tab_controller = tab_controller
        self.tab = ttk.Frame(tab_controller)
        self.tab_controller.add(self.tab, text=self.device_name)
        self.tab_controller.pack(expand = 1, fill="both")


    def update_log(self, text):
        new_text = []
        old_text = text.split("\n")
        for t in old_text:
            nt = re.sub("(.{150})", "\\1\n", t, 0, re.DOTALL)
            new_text.append(nt)

        text = "".join(new_text)
        self.update_tab_content(text)

    def empty_text_widgets(self):
        for text in self.log_text_widgets:
            text.destroy()

    def update_tab_content(self, text):
        text_w = Text(self.tab, width=150, height=text.count('\n') + 1)
        text_w.insert(END, text)
        text_w.pack()
        self.log_text_widgets.append(text_w)


