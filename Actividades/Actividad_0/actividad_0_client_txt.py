import socket
from utilities import *


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message_path = getPath("message.txt")

with open(message_path) as msg_file:

    message_str = msg_file.read()

    message_str_w_end = message_str + END_OF_MSG

    send_full_msg(client_socket, SERVER_BUFF_SIZE, SERVER_ADDRESS, message_str_w_end)
    print("Mensaje enviado")

    received_msg_str, sender_address = rcv_full_msg_str(client_socket, CLIENT_BUFF_SIZE, END_OF_MSG)
    print(f"Se recibió un mensaje: \n {received_msg_str}")

    if message_str == received_msg_str:
        print("El eco fue exitoso :)")
    else:
        print("Hubo un error al realizar el eco :(")

