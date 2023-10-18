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

# test 1
buff_size = 16
full_message = connection_socketTCP.recv(buff_size)
print("Test 1 received:", full_message)
if full_message == "Mensje de len=16".encode(): print("Test 1: Passed")
else: print("Test 1: Failed")

# test 2
buff_size = 19
full_message = connection_socketTCP.recv(buff_size)
print("Test 2 received:", full_message)
if full_message == "Mensaje de largo 19".encode(): print("Test 2: Passed")
else: print("Test 2: Failed")

# test 3
buff_size = 14
message_part_1 = connection_socketTCP.recv(buff_size)
message_part_2 = connection_socketTCP.recv(buff_size)
print("Test 3 received:", message_part_1 + message_part_2)
if (message_part_1 + message_part_2) == "Mensaje de largo 19".encode(): print("Test 3: Passed")
else: print("Test 3: Failed")