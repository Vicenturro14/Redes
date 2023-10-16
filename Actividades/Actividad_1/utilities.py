import socket
import os.path
from constants import *
import json
from Message_HTTP import *

def send_full_message(sender_socket : socket.socket, message : str):
    """ Envía completamente el mensaje message mediante el socket sender_socket"""
    
    message_bytes = message.encode()
    message_size_bytes = len(message_bytes)
    total_bytes_sent = 0

    while total_bytes_sent < message_size_bytes:
        sent_bytes = sender_socket.send(message_bytes[total_bytes_sent : ])
        total_bytes_sent += sent_bytes


def receive_HTTP_head(receiver_socket : socket.socket, buff_size : int):
    """
    Recibe el head de un mensaje HTTP.
    Retorna una tupla con un string con el head sin doble salto de línea al final
    y un string con la primera parte del body recibida junto al final del head.
    """
    
    full_head_str = ""
    end_of_head_pos = full_head_str.find(HEAD_END_SEQ)

    # Mientras no se reciba el final del head, se sigue recibiendo partes del mensaje
    while end_of_head_pos == -1:
        
        # Se recibe una nueva parte del mensaje
        recv_message_bytes = receiver_socket.recv(buff_size)

        # Se añade como string la parte recibida del mensaje a la parte anteriormente recibida
        full_head_str += recv_message_bytes.decode()

        # Se verifica si se recibió el final del head
        end_of_head_pos = full_head_str.find(HEAD_END_SEQ)

    # Si lo recibido termina con la secuencia de término del head, no se recibió parte del body
    if full_head_str.endswith(HEAD_END_SEQ):
        return full_head_str, ""

    # En caso contrario, se separa la parte del body recibida    
    head_end_seq_len = len(HEAD_END_SEQ)
    body_begin_index = end_of_head_pos + head_end_seq_len
    return full_head_str[ : body_begin_index], full_head_str[body_begin_index : ] 



def receive_HTTP_body(receiver_socket : socket.socket, buff_size : int, body_size_bytes : int, body_first_part : str):
    """
    Recibe el body de un mensaje HTTP del que ya se recibió el head.
    Retorna el body como string.
    """

    received_bytes = len(body_first_part.encode())
    full_body_bytes = body_first_part.encode()

    # Mientras no se hayan recibido todos los bytes del body, se seguirán recibiendo partes del mensaje 
    while received_bytes < body_size_bytes:
        
        # Se recibe una nueva parte del mensaje
        received_body_bytes = receiver_socket.recv(buff_size)

        # Se añade como string la parte recibida del mensaje a la ya recibida
        full_body_bytes += received_body_bytes

        received_bytes += len(received_body_bytes)

    # Se ignoran los bytes no pertenecientes al body, en caso de recibirlos
    extra_bytes = received_bytes - body_size_bytes
    if extra_bytes > 0:
        return full_body_bytes[:-extra_bytes].decode()
    return full_body_bytes.decode()


def receive_HTTP_message(receiver_socket : socket.socket, buff_size : int):
    """
    Recibe un mensaje HTTP completo y lo retorna como string.
    """
    
    # Se recibe el head del mensaje y la parte del body que se envíe junto al final del head
    head_str, body_first_part_str = receive_HTTP_head(receiver_socket, buff_size)
    
    
    # Se extrae desde el head el largo en bytes del body
    body_size_begin = head_str.find("Content-Length: ")
    if body_size_begin != -1:
        body_size_end = head_str.find(HEAD_ENDLINE, body_size_begin, len(head_str))
        body_size_bytes = int(head_str[body_size_begin + len("Content-Length: ") : body_size_end])
    else:
        body_size_bytes = 0
    # Se recibe el body
    body = receive_HTTP_body(receiver_socket, buff_size, body_size_bytes, body_first_part_str)

    # Se forma el mensaje HTTP completo
    http_message = head_str + body
    return http_message



def getPath(fileName : str):
    """
    Retorna la ruta absoluta del archivo entregado.
    El archivo se debe encontrar en la misma carpeta del script desde el que se llama la función.
    """
    
    this_file_path = os.path.abspath(__file__)
    this_dir_path = os.path.dirname(this_file_path)
    requested_path = os.path.join(this_dir_path, fileName)
    return requested_path


def parse_HTTP_head(http_head : str):
    """Recibe un head HTTP como string y retorna un diccionario con los headers del head recibido.
    Las llaves del diccionarios son los nombres de los headers y están asociadas al contenido de sus headers sin el nombre.
    La start line del head está asociada a la llave "start line"."""

    # Se divide el head por sus saltos de línea en una lista
    # Para esto se requiere que el head no tenga el doble salto de línea al final
    end_seq_size = len(HEAD_END_SEQ)
    headers_list = http_head[:-end_seq_size].split(HEAD_ENDLINE)

    # Cada header tiene su contenido asociado a su nombre como llave en headers_dict
    headers_dict = dict()
    for i in range(len(headers_list)):
        if i == 0:
            headers_dict["start line"] = headers_list[i]
        else:
            header = headers_list[i].split(": ", 1)
            headers_dict[header[0]] = header[1]

    return headers_dict


def parse_HTTP_message(http_message : str):
    """ Recibe un mensaje HTTP en forma de string y 
    lo retorna como un objeto de la clase Message_HTTP."""
    
    head_body_list = http_message.split(HEAD_END_SEQ, 1)

    head_dict = parse_HTTP_head(head_body_list[0] + HEAD_END_SEQ)

    return Message_HTTP(head_dict, head_body_list[1])


def create_HTTP_message(message : Message_HTTP):
    """ Recibe un objeto de la clase Message_HTTP. 
    Retorna un string con el mensaje HTTP correspondiente al objeto recibido. """

    return str(message)


def create_HTTP_response(request : Message_HTTP, body_html_name : str, response_code : str):
    """ Retorna una respuesta a la request entregada con el body entregado, 
    como un objeto de la clase Message_HTTP. """

    # Se obtiene el body del archivo indicado
    with open(getPath(body_html_name)) as body_file:
        body_str = body_file.read()
        body_bytes = body_str.encode()
        body_size_bytes = len(body_bytes)
    
    # Se crea un diccionario con headers
    headers_dict = dict()

    # Se añade start line
    headers_dict["start line"] = "HTTP/1.1" + " " + response_code

    # Se añade el mismo header de conexión de la request recibida
    if "Connection" in request.head:
        headers_dict["Connection"] = request.head["Connection"]
    # Se usa keep-alive en caso de que la request no tenga este header
    else:
        headers_dict["Connection"] = "keep-alive"

    # Se añade el largo del html del body y el tipo de body
    headers_dict["Content-Length"] = str(body_size_bytes)
    headers_dict["Content-Type"] = "text/html; charset=utf-8"

    response = Message_HTTP(headers_dict, body_str)
    return response


def check_request(request : Message_HTTP, blocked_URIs : list):
    """ Comprueba si la URI de la request HTTP está permitida.
    Retorna True si la URI está permitida y False si está bloqueada."""
    
    request_URI = request.get_URI()
    
    is_allowed = request_URI not in blocked_URIs
    
    return is_allowed

def send_403_error(request : Message_HTTP, client_comm_socket : socket.socket):
    """ Crea una respuesta HTTP de error 403 y lo envía mediante el client_comm_socket. """
    error_response = create_HTTP_response(request, "blocked_URI.html", "403 Forbidden")
    error_response_str = create_HTTP_message(error_response)
    send_full_message(client_comm_socket, error_response_str)

def load_json(json_file_path : str):
    """ Carga un archivo JSON y lo retorna. """
    with open(json_file_path) as json_file:
        json_data = json.load(json_file)
    return json_data