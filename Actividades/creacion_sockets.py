import socket

# Creación de socket orientado a conexión
socket_orient_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Creación de socket no orientado a conexión
socket_no_orient_con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)