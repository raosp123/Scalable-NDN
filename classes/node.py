import socket
import sys
import threading
import time
import random
import json
import rsa

class Node:
    def __init__(self,ip,port,ID):
        self.RPi_ip=ip
        self.port=port
        self.id=ID
        
    #Starts the listening process for the node, accepts any incoming connection and starts a thread to handle the connection
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
        
    #called by listen, tells the sender that it is about to receive a packet of certain data size, then receives the message
    # TODO: within the try, get back the name of the person receiving, so we can print in the except who we failed to connect to
    def handle_connection(self, sender_socket, addr):
        try:
            dataSize=sender_socket.recv(1024)
            data_size = int(dataSize.decode("utf-8"))
            sender_socket.send("ready".encode("utf-8"))
            print(f"We are ready to receive {data_size} from {addr}")
            message = sender_socket.recv(data_size+1024)
        except:
            print("failed to receive data from peer")

        self.handle_message(message.decode("utf-8"),addr)
        sender_socket.send("Message received correctly".encode("utf-8"))
     
        
    # TODO: process of sending packets, on a device level, we need to pass in what peer we are trying to connect to, use in "packet_receiver variable"
    def send(self,package,port, packet_receiver="test"):
        try:
            ip=self.RPi_ip
            sender_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sender_socket.connect((ip, port))
            sender_socket.send(str(sys.getsizeof(package)).encode("utf-8"))
            response= sender_socket.recv(1024).decode("utf-8")
            if response=="ready":
                print(f"Device {packet_receiver} is ready to receive message with {sys.getsizeof(package)} bytes") # we use our ip here because we assume localhost, we need better console debugging here
                sender_socket.send(package.encode("utf-8"))
                connection_received_conf=sender_socket.recv(1024)
                print(connection_received_conf)            
            sender_socket.close()
        except:
            print(f'failed to send packet to {packet_receiver}')

    def handle_message(self,message,addr):
        print(f"We have received {message}")
    # # We should probably define this function in a subclass of Node that inherits the elements
    # def generate_data(self, data_name, port):
    #     while True:
    #         data={'tag':data_name, 'timestamp':int(time.time()), 'temperature':random.uniform(10, 40)}
    #         package=json.dumps(data)
    #         self.send(package,port)
    #         time.sleep(20)
    
    def create_keys(self):
        """Creates and saves the keys that the node is going to use

        Returns:
            publickey, privatekey: the pair of keys that the node is going to use
        """
        # we create the keys
        publickey, privatekey = rsa.newkeys(512)
        # now we save the keys as file
        # Save the private key to a file
        with open(f"private_key{self.id}.pem", "wb") as f:
            f.write(privatekey.save_pkcs1("PEM"))
        # Save the public key to a file
        with open(f"public_key{self.id}.pem", "wb") as f:
            f.write(publickey.save_pkcs1("PEM"))
        return publickey, privatekey
    
    def encrypt(self, message, public_key_file):
        """Encrypts the message with the public key.

        Args:
            message: The message to encrypt.
            public_key: The public key file to use for encryption.

        Returns:
            The encrypted message."""
        
        with open(public_key_file, "rb") as f:
            public_key = f.read()
        public_key = rsa.PublicKey.load_pkcs1(public_key)
        enc_message = rsa.encrypt(message.encode("utf-8"), public_key)
        return enc_message
    
    def decrypt(self, enc_message, private_key_file):
        """Decrypts the message with the private key.

        Args:
            enc_message: The message to decrypt.
            private_key: The private key file to use for decryption.

        Returns:
            The decrypted message.
        """
        with open(private_key_file, "rb") as f:
            private_key = f.read()
        private_key = rsa.PrivateKey.load_pkcs1(private_key)
        dec_message = rsa.decrypt(enc_message, private_key).decode("utf-8")
        return dec_message
        
        

class Data:
    def __init__(self, tag, timestamp,content):
        self.tag=tag
        self.timestamp=timestamp
        self.content=content
    def __str__(self):
        return f"Tag: {self.tag}\nTimestap: {self.timestamp}\nContent: {self.content}"
