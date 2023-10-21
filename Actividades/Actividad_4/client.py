from constants import *
import SocketTCP

# Se recibe archivo por enviar
file_to_send_str = ""
while True:
    try:
        file_to_send_str += input() + '\n'
    except EOFError:
        break 
file_to_send_bytes = file_to_send_str[:-1].encode()

# Se crea el socketTCP del cliente
client_socketTCP = SocketTCP.SocketTCP()

# Se conecta con el socket del servidor
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

# test 4: Archivo desde entrada estándar
client_socketTCP.send(file_to_send_bytes)

# Cierre de conexíon
client_socketTCP.close()

# Se verifica que la conexión fue cerrada
if client_socketTCP.other_side_address is None:
    print("Conexión cerrada exitosamente")
else:
    print("Algo falló al cerrar la conexión")
