import socket


listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listen_socket.bind(('localhost', 33400))

while True:
    message, address = listen_socket.recvfrom(1024)

    print(message)