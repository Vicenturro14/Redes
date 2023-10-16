import socket

def segment_send_to(sender_socket : socket.socket, message : bytes, receiver_address : tuple) -> None:
    """Envía un segmento a la dirección recibida. 
    Se asume que la sección de headers del segmento es de 16 bytes 
    y la sección de contenido es de a lo más 16 bytes."""

    # Se envían los headers del segmento
    sender_socket.sendto(message[ : 16], receiver_address)

    # Se envía el contenido del segmento
    sender_socket.sendto(message[16 : ], receiver_address)


def segment_recvfrom(receiver_socket : socket.socket, receiver_buff_size : int) -> tuple:
    """Recibe un segmento y lo retorna junto a la dirección del socket. 
    Se asume que la sección de headers del segmento es de 16 bytes
    y la sección de contenido es de a lo más de 16 bytes."""

    # Se reciben los headers del segmento
    segment_headers, sender_address = receiver_socket.recvfrom(receiver_buff_size)  
    
    # Se recibe el contenido del segmento
    segment_content, _ = receiver_socket.recvfrom(receiver_buff_size)
    
    full_segment = segment_headers + segment_content
    return full_segment, sender_address