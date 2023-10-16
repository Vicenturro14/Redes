import socket

def receive_full_msg(connection_socket : socket.socket, buff_size : int, end_sequence : str):

    recv_msg_bytes = connection_socket.recv(buff_size)
    full_msg_str = recv_msg_bytes.decode()

    is_end_of_msg = contains_end_of_msg(full_msg_str, end_sequence)

    while not is_end_of_msg:
        recv_msg_bytes = connection_socket.recv(buff_size)
        full_msg_str += recv_msg_bytes.decode()

        is_end_of_msg = contains_end_of_msg(full_msg_str, end_sequence)

    full_msg_str = remove_end_of_msg(full_msg_str, end_sequence)    

    return full_msg_str


def contains_end_of_msg(msg : str, end_sequence : str):
    return msg.endswith(end_sequence)

def remove_end_of_msg(full_msg : str, end_sequence : str):
    index = full_msg.rfind(end_sequence)
    return full_msg[:index]

buff_size = 4 
end_of_msg = "\n"
new_socket_address = ("localhost", 5000)

print("Creando socket - servidor")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(new_socket_address)
server_socket.listen(3)

print("Esperando clientes ..")

while True:
    new_socket, new_socket_address = server_socket.accept()

    recv_msg_str = receive_full_msg(new_socket, buff_size, end_of_msg)
    new_msg_str = f"Se ha recibido el siguiente mensaje: {recv_msg_str}"
    print(f"Se ha recibido el siguiente mensaje: {recv_msg_str}")
    new_socket.send(new_msg_str.encode())
    new_socket.close()
    print(f"Conexión con {new_socket_address} ha sido cerrada")
