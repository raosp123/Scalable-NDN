from tkinter import *
import json
import re

class DebugManager:
    def __init__(self, ids, window_name = "Debug Window"):
        self.tk_root = Tk()
        self.tk_root.title(window_name)
        self.log_windows: dict[str, DeviceLoggingWindow] = {}

        for (_, id) in ids:
            self.log_windows[id] = DeviceLoggingWindow(id, self.tk_root)

        self.make_buttons()
        

    def debug(self, device_name, text):
        self.log_windows[device_name].add_log(text)

    def main_loop(self):

        try:
            self.tk_root.mainloop()
        except KeyboardInterrupt:
            print("Stopping debugger")

    def make_buttons(self):
        for window in self.log_windows.values():
            call_back = window.open_window
            b = Button(self.tk_root, text=window.device_name, command=call_back)
            b.pack(side="left")
        pass


class DeviceLoggingWindow:
    def __init__(self, device_name: str, master):
        self.frame_on = False
        self.master = master
        self.device_name = device_name
        self.log_data = []
        self.texts = []

    def empty_window_text(self):
        for text in self.texts:
            text.config(state=NORMAL)
            text.destroy()      
        self.texts = []

    def update_window_text(self):
        self.empty_window_text()
        for text in self.log_data: 
            text_w = Text(self.frame, width=150, height=text.count('\n') + 1)
            
            text_w.insert(END, text)
            text_w.pack()
            text_w.config(state=DISABLED)
            self.texts.append(text_w)

    def add_log(self, text: str):
        new_text = []
        old_text = text.split("\n")
        for t in old_text:
            nt = re.sub("(.{150})", "\\1\n", t, 0, re.DOTALL)
            new_text.append(nt)

        text = "".join(new_text)
        self.log_data.append(text)
        if self.frame_on: self.update_window_text()

    def open_window(self):
        def update():
            self.frame.after(100, update)

        def close_frame():
            self.frame_on = False
            self.empty_window_text()
            self.frame.destroy()
        self.frame = Toplevel(self.master)
        self.frame_on = True
        self.frame.protocol("WM_DELETE_WINDOW", func=close_frame)
        self.frame.after(100, update)

        self.text = Text(self.frame, height=1, width=len("DEVICE_LOG"))
        self.text.insert(INSERT, "DEVICE_LOG")
        self.text.pack()
        self.text.config(state=DISABLED)
        self.update_window_text()

        self.frame.title(self.device_name)
        
        

        

            