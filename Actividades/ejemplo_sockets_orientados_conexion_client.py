import socket

# Se instancia socket cliente.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tupla de dirección de destino.
dest_adress = ("localhost", 5000)
client_socket.connect(dest_adress)

# Se define mensaje y final de mensaje del protocolo de inventado.
message = "Hello World, Hola Mundo, Hallo Welt"
end_of_message = "\n"

send_message_str = message + end_of_message
send_message_bytes = send_message_str.encode()

print(f"Enviando mensaje: {send_message_str}")
client_socket.send(send_message_bytes)

print("Mensaje enviado")

# Se espera respuesta y se define tamaño del buffer de recepción.
buffer_size = 1024
recv_message_bytes = client_socket.recv(buffer_size)
recv_message_str = recv_message_bytes.decode()

print(f"Respuesta del servidor {recv_message_str}.")

client_socket.close()
