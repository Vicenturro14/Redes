import socket
from utilities import *
from constants import *
import sys

# Se guarda el nombre y la ruta del archivo json entregados al ejecutar el código.
if len(sys.argv) == 3:
    json_file_name = sys.argv[1]
    json_file_path = sys.argv[2]

# En caso de no ser entregados, se utiliza por defecto el archivo json_actividad_http.json
else:
    json_file_name = "json_actividad_http.json"
    json_file_path = getPath(json_file_name)

# Se cargan los datos del archivo JSON con las páginas bloqueadas y palabras prohibidas.
config_data = load_json(json_file_path)

# Se crea un socket para la conexión con el cliente
client_connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se le asigna una dirección al socket para la conexión con un cliente
client_connection_socket.bind(PROXY_ADDRESS)
client_connection_socket.listen(5)

while True:        
    # Se acepta la conexión con un cliente y se crea un socket para la comunicación
    client_comm_socket, client_comm_socket_address = client_connection_socket.accept()
    print("Se aceptó una conexión nueva")

    # Se recibe un mensaje HTTP desde el cliente
    client_recvd_msg_str = receive_HTTP_message(client_comm_socket, BUFF_SIZE)
    print("Mensaje del cliente recibido")

    # Se guarda el mensaje HTTP recibido como un objeto de la clase Message_HTTP
    client_http_msg = parse_HTTP_message(client_recvd_msg_str)


    # Si el cliente intenta acceder a una página bloqueada, se le envía un mensaje de error.
    if not check_request(client_http_msg, config_data["blocked"]):
        send_403_error(client_http_msg, client_comm_socket)
        print("Se ha enviado un error")

        # Se cierran los sockets utilizados
        client_comm_socket.close()

    # En caso contrario, se envía la request del cliente al servidor
    else:    
        # Se obtiene dirección del servidor desde el mensaje recibido
        server_dir = client_http_msg.get_request_destiny_address()
        server_address = (server_dir, 80)

        # Se crea socket para la comunicación con el servidor y se conecta con el servidor
        server_comm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_comm_socket.connect(server_address)

        # Se añade el header X-ElQuePregunta a la request recibida
        client_http_msg.add_header("X-ElQuePregunta", config_data["user"])
        
        # Se envía al servidor el mensaje con el header añadido
        msg_to_send_to_server = create_HTTP_message(client_http_msg)
        send_full_message(server_comm_socket, msg_to_send_to_server)
        print("Esperando respuesta del servidor")

        # Se recibe respuesta HTTP del servidor
        server_recvd_msg_str = receive_HTTP_message(server_comm_socket, BUFF_SIZE)
        server_recvd_msg = parse_HTTP_message(server_recvd_msg_str)

        # Se reemplaza el contenido inadecuado
        server_recvd_msg.replace_forbidden_words(config_data["forbidden_words"])
        
        # Se envía respuesta del servidor con censura al cliente
        msg_to_send_to_client = create_HTTP_message(server_recvd_msg)
        send_full_message(client_comm_socket, msg_to_send_to_client)
        print("Respuesta enviada al cliente")

        # Se cierran los sockets utilizados
        client_comm_socket.close()
        server_comm_socket.close()
        
    print("Se cerró la conexión.\n")
