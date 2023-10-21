from constants import *
import SocketTCP

with open("file_to_send.txt") as file:
    file_to_receive = file.read()

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

# test 4: Archivo desde entrada estándar
buff_size = 27
message_part_1 = connection_socketTCP.recv(buff_size)
message_part_2 = connection_socketTCP.recv(buff_size)
full_message = message_part_1 + message_part_2
print("Test 4 received:", full_message)
if full_message.decode() == file_to_receive: print("Test 4: Passed")
else: print("Test 4: Failed")


# Se recibe el cierre de conexión
connection_socketTCP.close_recv()

# Se prueba que se cerró la conexión
if connection_socketTCP.other_side_address is None:
    print("Conexión cerrada con éxito")
else:
    print("Algo falló al cerrar la conexión")
