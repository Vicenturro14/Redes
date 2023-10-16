import socket
from constants import *
from random import randint
from utilities import segment_send_to, segment_recvfrom

class SocketTCP:
    def __init__(self) -> None:
        self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_address = ()
        self.other_side_address = ()
        self.seq_num = 0
        self.buff_size = 32

    @staticmethod
    def parse_segment(segment : bytes) -> dict:
        """Separa el segmento recibido por la secuencia de bytes b"|||" 
        y retorna las partes en un diccionario."""
        divided_segment = segment.split(SEGMENT_SEPARATOR)
        segment_dict = {
            SYN : int.from_bytes(divided_segment[0], byteorder = "big"),
            ACK : int.from_bytes(divided_segment[1], byteorder = "big"),
            FIN : int.from_bytes(divided_segment[2], byteorder = "big"),
            SEQ : int.from_bytes(divided_segment[3], byteorder = "big"),
            DATA : divided_segment[4]
        }
        return segment_dict
    
    @staticmethod
    def create_segment(segment_dict : dict) -> bytes:
        segment = segment_dict[SYN].to_bytes(1, "big") +\
              SEGMENT_SEPARATOR + segment_dict[ACK].to_bytes(1, "big") +\
              SEGMENT_SEPARATOR + segment_dict[FIN].to_bytes(1, "big") +\
              SEGMENT_SEPARATOR + segment_dict[SEQ].to_bytes(1, "big") +\
              SEGMENT_SEPARATOR + segment_dict[DATA]
            
        return segment
    
    def bind(self, address : tuple) -> None:
        """Indica la dirección a la que debe escuchar el socket."""
        self.my_address = address
        self.socket_udp.bind(address)

    def connect(self, address : tuple) -> None:
        """Inicia la conexión con otro objeto de la clase SocketTCP que escucha la dirección address"""
        
        # Se define el número de secuencia de manera aleatoria.
        self.seq_num = randint(0, 100)

        # Se crea el segmento de sincronización a enviar.
        connection_segment_dict = {SYN : 1,
                                   ACK : 0,
                                   FIN : 0,
                                   SEQ : self.seq_num,
                                   DATA: b""
                                   }
        connection_segment = self.create_segment(connection_segment_dict)
        
        # Se manda el segmento de sincronización
        segment_send_to(self.socket_udp, connection_segment, address)

        # Se reciben segmentos hasta que se reciba uno de confirmación 
        # y sincronización con el número de secuencia correcto.
        received_segment, _ = segment_recvfrom(self.socket_udp, 16)
        received_segment_dict = self.parse_segment(received_segment)
        while received_segment_dict[SYN] != 1 or received_segment_dict[ACK] != 1 or received_segment_dict[SEQ] != self.seq_num + 1:
            received_segment, _ = segment_recvfrom(self.socket_udp, 16)
            received_segment_dict = self.parse_segment(received_segment)

        # Se guarda la dirección del socket con el que se establece la conexión.
        self.other_side_address = address

        # Se reutiliza el segmento recibido para usarlo para confirmar
        # la comunicación de servidor a cliente.
        received_segment_dict[SYN] = 0
        received_segment_dict[SEQ] += 1
        self.seq_num = received_segment_dict[SEQ]
        acknowledge_segment = self.create_segment(received_segment_dict)
        segment_send_to(self.socket_udp, acknowledge_segment, address)

        

    def accept(self) -> tuple:
        """Espera y acepta una petición de tipo SYN.
        Retorna el socket que se utilizará para """

        # Se reciben segmentos hasta que se reciba uno de sincronización.
        received_segment, sender_address = segment_recvfrom(self.socket_udp, 16)
        received_segment_dict = self.parse_segment(received_segment)
        while received_segment_dict[SYN] != 1:
            received_segment, sender_address = segment_recvfrom(self.socket_udp, 16)
            received_segment_dict = self.parse_segment(received_segment)        

        # Se reutiliza el segmento recibido, modificando sus headers
        received_segment_dict[ACK] = 1
        received_segment_dict[SEQ] += 1
        self.seq_num = received_segment_dict[SEQ]

        acknowledge_segment = self.create_segment(received_segment_dict)
        segment_send_to(self.socket_udp, acknowledge_segment, sender_address)

        # Se reciben segmentos hasta encontrar uno 
        # de confirmación con el número de secuencia correcto.
        received_segment, sender_address = segment_recvfrom(self.socket_udp, 16)
        received_segment_dict = self.parse_segment(received_segment)
        while received_segment_dict[ACK] != 1  or received_segment_dict[SEQ] != self.seq_num + 1:
            received_segment, sender_address = segment_recvfrom(self.socket_udp, 16)
            received_segment_dict = self.parse_segment(received_segment)

        # Se crea el socket para la comunicación con el cliente
        communication_socket = SocketTCP()
        communication_address = (self.my_address[0], self.my_address[1] + 1)
        communication_socket.bind(communication_address)
        communication_socket.seq_num = self.seq_num
        communication_socket.other_side_address = sender_address

        
        return communication_socket, communication_address

    def send(self, message : bytes) -> None:
        """Envía un mensaje en bytes al socket con el que se conectó"""
        
        # Se crea el segmento inicial con el largo del mensaje.
        message_len = len(message)
        segment_dict = {
            ACK : 0,
            SYN : 0,
            FIN : 0,
            SEQ : self.seq_num,
            DATA : message_len.to_bytes(1, "big")
        }
        segment = self.create_segment(segment_dict)
        

    def recv(self, buff_size : int) -> bytes:
        """Recibe un mensaje en bytes del socket con el que se conectó
        usando un buffer de tamaño buff_size."""
        pass
