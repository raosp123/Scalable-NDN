import base64
import os
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
        self.is_listening = False
        
        self.load_keys()
        
    #Starts the listening process for the node, accepts any incoming connection and starts a thread to handle the connection
    def listen(self):
        self.is_listening = True
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((self.RPi_ip, self.port))
        self.listen_socket.listen(50)
        while True:
            # We need to divide into threads to allow multiple connections
            try:
                sender_socket, sender_address = self.listen_socket.accept()
            except OSError as e:
                if self.is_listening:
                    raise e
                sys.exit(0)

            # We first receive the size of the package
            thread = threading.Thread(target=self.handle_connection,args=(sender_socket, sender_address))
            thread.start() 
        
    #called by listen, tells the sender that it is about to receive a packet of certain data size, then receives the message
    # TODO: within the try, get back the name of the person receiving, so we can print in the except who we failed to connect to (done)
    def handle_connection(self, sender_socket, addr):
        sender_name = "Sender"
        try:
            dataSize=sender_socket.recv(1024)
            data_size = int(dataSize.decode("utf-8"))
            sender_socket.send("ready".encode("utf-8"))
            # implementig the to do so we now who is sending the data
            sender_name = sender_socket.recv(1024).decode("utf-8")
            #decrypt message with my private key
            message = self.decrypt(sender_socket.recv(data_size+1024))
            sender_socket.send("message_recieved".encode("utf-8"))
            self.handle_message(message, addr)
        except Exception as e:
            print(f"Failed to receive data from {sender_name} at address {addr}", e)
        
    # TODO: process of sending packets, on a device level, we need to pass in what peer we are trying to connect to, use in "packet_receiver variable"
    def send(self,package, port, packet_receiver):
        try:
            ip=self.RPi_ip
            sender_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sender_socket.connect((ip, port))
            encrpyted_packet = self.encrypt(package, packet_receiver)

            sender_socket.send(str(sys.getsizeof(encrpyted_packet)).encode("utf-8"))
            response = sender_socket.recv(1024).decode("utf-8")
            if response=="ready":
                ##print(f"Device {packet_receiver} is ready to receive message {package} with {sys.getsizeof(package)} bytes") # we use our ip here because we assume localhost, we need better console debugging here
                sender_socket.send(str(self.id).encode("utf-8"))
                #encrypt package with receivers public key, how do we get the public of the device
                sender_socket.send(encrpyted_packet)
                connection_received_conf=sender_socket.recv(1024)          
            sender_socket.close()
        except Exception as e:
            print(f'failed to send packet to {packet_receiver} , {e}')

    def handle_message(self,message,addr):
        pass
    # # We should probably define this function in a subclass of Node that inherits the elements
    # def generate_data(self, data_name, port):
    #     while True:
    #         data={'tag':data_name, 'timestamp':int(time.time()), 'temperature':random.uniform(10, 40)}
    #         package=json.dumps(data)
    #         self.send(package,port)
    #         time.sleep(20)
    
    def load_keys(self):
        """Creates and saves the keys that the node is going to use

        Returns:
            publickey, privatekey: the pair of keys that the node is going to use
        """
        # we create the keys
        if os.path.exists(f"keys/{self.id}_key_private.pem"):
            with open(f"keys/{self.id}_key_public.pem", "rb") as f:
                publickey = f.read()
            with open(f"keys/{self.id}_key_private.pem", "rb") as f:
                privatekey = f.read()
            self.keys = (privatekey, publickey)
        else:
            publickey, privatekey = rsa.newkeys(2048)
            # now we save the keys as file
            # Save the private key to a file
            with open(f"keys/{self.id}_key_public.pem", "wb") as f:
                f.write(publickey.save_pkcs1("PEM"))
            with open(f"keys/{self.id}_key_private.pem", "wb") as f:
                f.write(privatekey.save_pkcs1("PEM"))
            self.keys = (privatekey, publickey)
    
    def encrypt(self, message, node_id):
        """Encrypts the message with the public key.

        Args:
            message: The message to encrypt.

        Returns:
            The encrypted message."""
        with open(f"keys/{node_id}_key_public.pem", "rb") as f:
            public_key = f.read()
            loaded_key = rsa.PublicKey.load_pkcs1(public_key)
            utf_message = json.dumps(message).encode("utf-8")
            enc_message = rsa.encrypt(utf_message, loaded_key)
            #enc_message = rsa.encrypt(json.dumps(message).encode("utf-8"), rsa.PublicKey.load_pkcs1(public_key))
            return base64.b64encode(enc_message)

        
    
    def decrypt(self, enc_message):
        """Decrypts the message with the private key.

        Args:
            enc_message: The message to decrypt.
            private_key: The private key file to use for decryption.

        Returns:
            The decrypted message.
        """
        private_key = self.keys[0]
        dec_message = json.loads(rsa.decrypt(base64.b64decode(enc_message), rsa.PrivateKey.load_pkcs1(private_key)).decode("utf-8"))
        return dec_message
        
    def close(self):
        self.is_listening = False
        self.listen_socket.shutdown(socket.SHUT_RDWR)
        self.listen_socket.close()

class Data:
    def __init__(self, tag, timestamp,content):
        self.tag=tag
        self.timestamp=timestamp
        self.content=content
    def __str__(self):
        return f"Tag: {self.tag}\nTimestap: {self.timestamp}\nContent: {self.content}"
