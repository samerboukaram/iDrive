import socket

# IP = "127.0.0.1"
IP = "172.104.253.25"
PORT = 5005


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(b"Hello, World!", (IP, PORT))