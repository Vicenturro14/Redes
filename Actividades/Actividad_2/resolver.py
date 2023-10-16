import socket
from functions import *

buff_size = 4096
address = ("localhost", 8000)

resolver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
resolver_socket.bind(address)

try:
    while True:
        recv_msg, client_address = resolver_socket.recvfrom(buff_size)
        resolved_message = resolver(recv_msg)
        if resolved_message is not None:
            resolver_socket.sendto(resolved_message, client_address)
except KeyboardInterrupt:
    resolver_socket.close() 
