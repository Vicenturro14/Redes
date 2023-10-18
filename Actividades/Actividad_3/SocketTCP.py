import socket
from constants import *
from random import randint

class SocketTCP:
    def __init__(self) -> None:
        self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_address = None
        self.other_side_address = None
        self.seq_num = 0
        self.udp_buff_size = 64
        self.bytes_to_receive = 0
        self.last_asigned_port = 8000
        self.last_overflow = b""

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
        # Crea un segmento de largo entre 19 y 35 bytes.
        segment = segment_dict[SYN].to_bytes(1, "big") +\
              SEGMENT_SEPARATOR + segment_dict[ACK].to_bytes(1, "big") +\
              SEGMENT_SEPARATOR + segment_dict[FIN].to_bytes(1, "big") +\
              SEGMENT_SEPARATOR + segment_dict[SEQ].to_bytes(4, "big") +\
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
        connection_segment_dict = {
            SYN : 1,
            ACK : 0,
            FIN : 0,
            SEQ : self.seq_num,
            DATA: b""
            }
        connection_segment = self.create_segment(connection_segment_dict)
        
        # Se manda el segmento de sincronización
        self.socket_udp.sendto(connection_segment, address)

        # Se reciben segmentos hasta que se reciba uno de confirmación 
        # y sincronización con el número de secuencia correcto.
        received_segment, sender_address = self.socket_udp.recvfrom(self.udp_buff_size)
        received_segment_dict = self.parse_segment(received_segment)
        while received_segment_dict[SYN] != 1 or received_segment_dict[ACK] != 1 or received_segment_dict[SEQ] != self.seq_num + 1:
            received_segment, sender_address = self.socket_udp.recvfrom(self.udp_buff_size)
            received_segment_dict = self.parse_segment(received_segment)

        # Se guarda la dirección del socket con el que se establece la conexión.
        self.other_side_address = sender_address

        # Se reutiliza el segmento recibido para usarlo para confirmar
        # la comunicación de servidor a cliente.
        received_segment_dict[SYN] = 0
        received_segment_dict[SEQ] += 1
        self.seq_num = received_segment_dict[SEQ]
        acknowledge_segment = self.create_segment(received_segment_dict)
        self.socket_udp.sendto(acknowledge_segment, sender_address)

        
    def accept(self) -> tuple:
        """Espera y acepta una petición de tipo SYN.
        Retorna el socket que se utilizará para la comunicación con el cliente."""

        # Se reciben segmentos hasta que se reciba uno de sincronización.
        received_segment, sender_address = self.socket_udp.recvfrom(self.udp_buff_size)
        received_segment_dict = self.parse_segment(received_segment)
        while received_segment_dict[SYN] != 1:
            received_segment, sender_address = self.socket_udp.recvfrom(self.udp_buff_size)
            received_segment_dict = self.parse_segment(received_segment)        

        # Se reutiliza el segmento recibido, modificando sus headers
        received_segment_dict[ACK] = 1
        received_segment_dict[SEQ] += 1
        acknowledge_segment = self.create_segment(received_segment_dict)

        # Se crea el socket para la comunicación con el cliente
        communication_socket = SocketTCP()
        communication_address = (self.my_address[0], self.last_asigned_port + 1)
        self.last_asigned_port += 1
        communication_socket.bind(communication_address)
        communication_socket.seq_num = received_segment_dict[SEQ]
        communication_socket.other_side_address = sender_address

        # Se envía el segmento de confirmación y sincronización
        communication_socket.socket_udp.sendto(acknowledge_segment, sender_address)

        # Se reciben segmentos hasta encontrar uno 
        # de confirmación con el número de secuencia correcto.
        received_segment, _ = communication_socket.socket_udp.recvfrom(self.udp_buff_size)
        received_segment_dict = self.parse_segment(received_segment)
        while received_segment_dict[ACK] != 1  or received_segment_dict[SEQ] != communication_socket.seq_num + 1:
            received_segment, sender_address = communication_socket.socket_udp.recvfrom(self.udp_buff_size)
            received_segment_dict = self.parse_segment(received_segment)

        return communication_socket, communication_address


    def send(self, message : bytes) -> None:
        """Envía un mensaje en bytes al socket con el que se conectó"""

        # Se configura el timeout
        self.socket_udp.settimeout(TIMEOUT)

        # Se crea el segmento inicial con el largo del mensaje.
        message_len = len(message)
        segment_dict = {
            ACK : 0,
            SYN : 0,
            FIN : 0,
            SEQ : self.seq_num,
            DATA : message_len.to_bytes(4, "big")
        }
        sent_data_len = len(segment_dict[DATA])
        segment = self.create_segment(segment_dict)
        
        while True:
            try:
                # Se envía el segmento con el largo del mensaje
                self.socket_udp.sendto(segment, self.other_side_address)

                # Se espera a un mensaje hasta que llegue se cumpla el timeout o 
                # llegue uno de tipo ACK con el número de secuencia adecuado.
                received_segment, _ = self.socket_udp.recvfrom(self.udp_buff_size)
                received_segment_dict = self.parse_segment(received_segment)
                while received_segment_dict[ACK] != 1 or received_segment_dict[SEQ] != self.seq_num + sent_data_len:
                    received_segment, _ = self.socket_udp.recvfrom(self.udp_buff_size)
                    received_segment_dict = self.parse_segment(received_segment)
                self.seq_num = received_segment_dict[SEQ]
                break

            except TimeoutError:
                # Si se cumple el timeout se vuele a enviar el segmento
                continue
                
        # Se envía el mensaje por partes de largo a lo más 16 bytes, con la metodología anterior.
        sent_bytes = 0
        slice_max_len = 16
        while sent_bytes < message_len:
            slice_end = min(message_len, sent_bytes + slice_max_len)
            message_slice = message[sent_bytes : slice_end]
            sent_data_len = len(message_slice)
            segment_dict[DATA] = message_slice
            segment_dict[SEQ] = self.seq_num
            segment_to_send = self.create_segment(segment_dict)

            while True:
                try:
                    # Se envía el segmento
                    self.socket_udp.sendto(segment_to_send  , self.other_side_address)

                    # Se espera a un mensaje hasta que llegue se cumpla el timeout o 
                    # llegue uno de tipo ACK con el número de secuencia adecuado.
                    received_segment, _ = self.socket_udp.recvfrom(self.udp_buff_size)
                    received_segment_dict = self.parse_segment(received_segment)
                    while received_segment_dict[ACK] != 1 or received_segment_dict[SEQ] != self.seq_num + sent_data_len:
                        received_segment, _ = self.socket_udp.recvfrom(self.udp_buff_size)
                        received_segment_dict = self.parse_segment(received_segment)
                    self.seq_num = received_segment_dict[SEQ]
                    break

                except TimeoutError:
                # Si se cumple el timeout se vuele a enviar el segmento
                    continue
            
            sent_bytes += sent_data_len


    def recv(self, buff_size : int) -> bytes:
        """Recibe un mensaje en bytes del socket con el que se conectó
        usando un buffer de tamaño buff_size."""
        
        # Si no faltan bytes por recibir de una llamada anterior al método,
        # se recibe el largo del mensaje a recibir.
        if self.bytes_to_receive == 0:
            received_segment, sender_address = self.socket_udp.recvfrom(self.udp_buff_size)
            while sender_address != self.other_side_address:
                received_segment, sender_address = self.socket_udp.recvfrom(self.udp_buff_size)
            received_segment_dict = self.parse_segment(received_segment)
            self.bytes_to_receive = int.from_bytes(received_segment_dict[DATA], "big")
            
            # Se envía la confirmación
            received_segment_dict[ACK] = 1
            received_segment_dict[SEQ] += len(received_segment_dict[DATA])
            self.seq_num = received_segment_dict[SEQ]
            acknowledge_segment = self.create_segment(received_segment_dict)
            self.socket_udp.sendto(acknowledge_segment, self.other_side_address)
            
            received_bytes = 0
            received_message = b""
        else:
            received_message = self.last_overflow
            received_bytes = len(received_message)

        # Se recibe segmentos hasta que no queden bytes por recibir o que se alcance el tamaño del buffer.
        while received_bytes < self.bytes_to_receive and received_bytes < buff_size:

            # Se recibe un segmento
            received_segment, _ = self.socket_udp.recvfrom(self.udp_buff_size)
            received_segment_dict = self.parse_segment(received_segment)
            # Si se trata del segmento adecuado, se agrega al contenido recibido y se envía un mensaje de confirmación
            if received_segment_dict[SEQ] == self.seq_num:
                # Se agrega el segmento a mensaje recibido
                received_message += received_segment_dict[DATA]
                received_bytes += len(received_segment_dict[DATA])
                
                # Se reutiliza el diccionario del segmento recibido
                received_segment_dict[ACK] = 1
                received_segment_dict[SEQ] += len(received_segment_dict[DATA])
                self.seq_num = received_segment_dict[SEQ]
                acknowledge_segment = self.create_segment(received_segment_dict)
                self.socket_udp.sendto(acknowledge_segment, self.other_side_address)

            # En caso de recibir un número de secuencia menor al esperado, 
            # se vuelve a enviar el último segmento de confirmación enviado.
            elif received_segment_dict[SEQ] < self.seq_num:
                self.socket_udp.sendto(acknowledge_segment, self.other_side_address)

        # Si ya se recibieron todos los bytes del mensaje, simplemente se retorna
        if received_bytes == self.bytes_to_receive:
            self.bytes_to_receive = 0
            return received_message
        
        # En caso contrario se guarda los bytes que se recibieron
        # pero no cupieron en el buffer y se retornan los bytes del buffer
        bytes_to_return = received_message[ : buff_size]
        overflow = received_message[buff_size : ]

        self.bytes_to_receive -= buff_size
        self.last_overflow = overflow
        return bytes_to_return

    def close(self) -> None:
        """Cierra la conexión con el socket remoto."""

        # Se crea y manda el segmento para indicar el fin de la conexión.
        fin_segment_dict = {
            FIN : 1,
            ACK : 0,
            SYN : 0,
            SEQ : self.seq_num,
            DATA : b""
        }
        fin_segment = self.create_segment(fin_segment_dict)
        self.socket_udp.sendto(fin_segment, self.other_side_address)

        # Se espera un mensaje de fin de conexión y confirmación
        received_segment, _ = self.socket_udp.recvfrom(self.udp_buff_size)
        received_segment_dict = self.parse_segment(received_segment)
        while received_segment_dict[FIN] != 1 or received_segment_dict[ACK] != 1 or received_segment_dict[SEQ] != self.seq_num + 1:
            received_segment, _ = self.socket_udp.recvfrom(self.udp_buff_size)
            received_segment_dict = self.parse_segment(received_segment)

        # Se reutiliza el segmento recibido para enviar un segmento de confirmación
        received_segment_dict[FIN] = 0
        received_segment_dict[SEQ] += 1
        acknowledge_segment = self.create_segment(received_segment_dict)
        self.socket_udp.sendto(acknowledge_segment, self.other_side_address)
        
        # Se borra la dirección del socket remoto
        self.other_side_address = None


    def close_recv(self) -> None:
        """Recibe una indicacíon de cierre de conexión y se encarga de cerrarla."""

        # Se espera un mensaje de fin de conexión
        received_segment, _ = self.socket_udp.recvfrom(self.udp_buff_size)
        received_segment_dict = self.parse_segment(received_segment)
        while received_segment_dict[FIN] != 1:
            received_segment, _ = self.socket_udp.recvfrom(self.udp_buff_size)
            received_segment_dict = self.parse_segment(received_segment)
        
        # Se reutiliza el segmento recibido.
        received_segment_dict[ACK] = 1
        received_segment_dict[SEQ] += 1
        self.seq_num = received_segment_dict[SEQ]
        finack_segment = self.create_segment(received_segment_dict)
        self.socket_udp.sendto(finack_segment, self.other_side_address)

        # Se espera el segmento de confirmación con número de secuencia adecuado.
        received_segment, _ = self.socket_udp.recvfrom(self.udp_buff_size)
        received_segment_dict = self.parse_segment(received_segment)
        while received_segment_dict[ACK] != 1:
            received_segment, _ = self.socket_udp.recvfrom(self.udp_buff_size)
            received_segment_dict = self.parse_segment(received_segment)

        # Se borra la dirección del socket remoto
        self.other_side_address = None   
