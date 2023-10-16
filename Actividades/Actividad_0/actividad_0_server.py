import socket
from utilities import *


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = SERVER_ADDRESS

server_socket.bind(server_address)

print("Esperando clientes ...")
while True:
    received_msg_str, msg_address = rcv_full_msg_str(server_socket, SERVER_BUFF_SIZE, END_OF_MSG)
    print(f"Se recibió el mensaje: {received_msg_str}.")

    response_message_str = received_msg_str + END_OF_MSG
    send_full_msg(server_socket, CLIENT_BUFF_SIZE, msg_address, response_message_str)
    print("Se ha hecho eco del mensaje :)")

    