import socket
import sys
import threading
import time
import random
import json

class Node:
    def __init__(self,ip,port,ID):
        self.RPi_ip=ip
        self.port=port
        self.id=ID
        
    def listen(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((self.RPi_ip, self.port))
        listen_socket.listen(50)
        while True:
            # We need to divide into threads to allow multiple connections
            sender_socket, sender_address = listen_socket.accept()
            # We first receive the size of the package
            thread = threading.Thread(target=self.handle_connection,args=(sender_socket, sender_address))
            thread.start()  
        
    def handle_connection(self, conn, addr):
        dataSize=conn.recv(1024)
        data_size = int(dataSize.decode("utf-8"))
        conn.send("ready".encode("utf-8"))
        print(f"We are ready to receive {data_size} from {addr}")
        message = conn.recv(data_size+1024)
        self.handle_message(message.decode("utf-8"),addr)
        conn.send("Message received correctly".encode("utf-8"))
        
    def send(self,package,port):
        ip=self.RPi_ip
        sender_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.connect((ip, port))
        sender_socket.send(str(sys.getsizeof(package)).encode("utf-8"))
        response= sender_socket.recv(1024).decode("utf-8")
        if response=="ready":
            print(f"Device {ip} is ready to receive message with {sys.getsizeof(package)} bytes")
            sender_socket.send(package.encode("utf-8"))
            connection_received_conf=sender_socket.recv(1024)
            print(connection_received_conf)            
        sender_socket.close()
    def handle_message(self,message,addr):
        print(f"We have received {message}")
    # # We should probably define this function in a subclass of Node that inherits the elements
    # def generate_data(self, data_name, port):
    #     while True:
    #         data={'tag':data_name, 'timestamp':int(time.time()), 'temperature':random.uniform(10, 40)}
    #         package=json.dumps(data)
    #         self.send(package,port)
    #         time.sleep(20)


class Data:
    def __init__(self, tag, timestamp,content):
        self.tag=tag
        self.timestamp=timestamp
        self.content=content
    def __str__(self):
        return f"Tag: {self.tag}\nTimestap: {self.timestamp}\nContent: {self.content}"
