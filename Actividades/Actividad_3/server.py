import socket
from constants import *
import SocketTCP


# # Se crea el socket no orientado a conexión del servidor
# connection_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# connection_socket.bind(SERVER_ADDRESS)
# buff_size = 16

# # Se recibe el mensaje
# received_file_bytes = "".encode()
# while True:
#     received_slice, sender_address = connection_socket.recvfrom(16)
#     segment_dict = SocketTCP.parse_segment(received_slice)
#     print(segment_dict["DATA"], end="")
#     received_file_bytes += segment_dict["DATA"]

server_socketTCP = SocketTCP.SocketTCP()
server_socketTCP.bind(SERVER_ADDRESS)
connection_socketTCP, new_address = server_socketTCP.accept()