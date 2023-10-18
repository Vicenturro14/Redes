import socket
from constants import *
import SocketTCP


# # Se crea socket no orientado a conexión del cliente
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Se recibe archivo por enviar
# file_to_send_str = ""
# while True:
#     try:
#         file_to_send_str += input() + '\n'
#     except EOFError:
#         break 
# file_to_send_bytes = file_to_send_str.encode()
# print(file_to_send_str)

# # Se envía el archivo recibido por trozos
# file_len_bytes = len(file_to_send_bytes)
# slice_max_len = 16
# sended_bytes = 0

# # TODO: Actualizar diccionario
# segment_dict = {"DATA" : b""}
# while sended_bytes + slice_max_len <= file_len_bytes:
#     file_byte_slice = file_to_send_bytes[sended_bytes : sended_bytes + slice_max_len]
#     segment_dict["DATA"] = file_byte_slice
#     segment_with_headers = SocketTCP.create_segment(segment_dict)
#     client_socket.sendto(segment_with_headers, SERVER_ADDRESS)
#     sended_bytes += slice_max_len

# if sended_bytes != file_len_bytes:
#     final_slice = file_to_send_bytes[sended_bytes : ]
#     client_socket.sendto(final_slice, SERVER_ADDRESS)
    

client_socketTCP = SocketTCP.SocketTCP()
client_socketTCP.connect(SERVER_ADDRESS)
# test 1
message = "Mensje de len=16".encode()
client_socketTCP.send(message)
# test 2
message = "Mensaje de largo 19".encode()
client_socketTCP.send(message)
# test 3
message = "Mensaje de largo 19".encode()
client_socketTCP.send(message)