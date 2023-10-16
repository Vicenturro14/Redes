import socket
import os.path

# Constantes
SERVER_ADDRESS = ("localhost", 5000)
END_OF_MSG = '|'
SERVER_BUFF_SIZE = 4
CLIENT_BUFF_SIZE = 4


def contains_end_of_msg(msg : str, end_seq : str):
    return msg.endswith(end_seq) 

def remove_end_of_msg(msg : str, end_seq : str):
    index = msg.find(end_seq)
    return msg[:index]


def rcv_full_msg_str(server_socket : socket.socket, buff_size : int, end_seq : str):
    
    received_msg_bytes, msg_address = server_socket.recvfrom(buff_size)
    full_msg_str = received_msg_bytes.decode()

    is_end_of_msg = contains_end_of_msg(full_msg_str, end_seq)

    while not is_end_of_msg:
        received_msg_bytes, msg_address = server_socket.recvfrom(buff_size)
        full_msg_str += received_msg_bytes.decode()
        
        is_end_of_msg = contains_end_of_msg(full_msg_str, end_seq)

    full_msg_str = remove_end_of_msg(full_msg_str, end_seq)
    return full_msg_str, msg_address


def send_full_msg(sender_socket : socket.socket, receiver_buff_size: int, receiver_address: tuple, msg : str):
    msg_len = len(msg)
    index_first_char = 0
    msg_send = ""
    while True: 

        index_last_char = min(msg_len, index_first_char + receiver_buff_size)
        slice_to_send = msg[index_first_char: index_last_char]
        sender_socket.sendto(slice_to_send.encode(), receiver_address)
        msg_send += slice_to_send

        if msg_send.endswith(END_OF_MSG):
            break

        index_first_char += receiver_buff_size 

def getPath(fileName : str):
    this_file_path = os.path.abspath(__file__)
    this_dir_path = os.path.dirname(this_file_path)
    requested_path = os.path.join(this_dir_path, fileName)
    return requested_path
