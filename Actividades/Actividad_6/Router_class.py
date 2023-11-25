import socket
from RoutesTable import RoutesTable

class Router:
    def __init__(self, IP : str, port : int, routes_table_file_name : str) -> None:
        self.IP = IP
        self.port = port
        self.dir = (self.IP, self.port)
        self.routes_table = RoutesTable(routes_table_file_name)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.dir)


    @staticmethod
    def parse_packet(IP_packet : bytes) -> dict[str, str | int]:
        """Retorna un diccionario con los headers y el mensaje del paquete IP recibido."""
        IP_direction, port, ttl, id, offset, size, flag, data = IP_packet.decode().split(",")
        parsed_packet = {
            "IP_direction" : IP_direction, 
            "port" : int(port), 
            "TTL" : int(ttl),
            "id" : int(id),
            "offset" : int(offset),
            "size" : int(size),
            "flag" : int(flag),
            "data" : data
            }
        return parsed_packet
    
    @staticmethod
    def to_str(num : int, size : int) -> str:
        """
        Convierte el número recibido a un string de largo "size". Si el número 
        tiene menos de "size" dígitos, se rellena con ceros por la derecha. Si
        tiene más de "size" dígitos, se retornan los últimos "size" dígitos.
        """
        num_str = str(num)
        n = len(num_str)
        if n < size:
            return num_str.zfill(size)
        if size < n:
            return num_str[-size:]
        return num_str

    @staticmethod
    def create_packet(IP_packet_dict : dict[str, str | int]) -> bytes:
        """Retorna una cadena de bytes correspondiente al paquete IP representado en el diccionario recibido."""
        ip = IP_packet_dict['IP_direction']
        port_str = Router.to_str(IP_packet_dict["port"], 4)
        ttl_str = Router.to_str(IP_packet_dict["TTL"], 3)
        id_str = Router.to_str(IP_packet_dict["id"], 8)
        offset_str = Router.to_str(IP_packet_dict["offset"], 8)
        size_str = Router.to_str(IP_packet_dict["size"], 8)
        flag_str = Router.to_str(IP_packet_dict["flag"], 1)
        data = IP_packet_dict["data"]
        return f"{ip},{port_str},{ttl_str},{id_str},{offset_str},{size_str},{flag_str},{data}".encode()

    def check_routes(self, destination_address : tuple[str, int]) -> tuple[str, int] | None:
        """
        Retorna la dirección (IP, puerto) del siguiente salto indicado por
        la tabla de rutas para llegar a la dirección de destino recibida.
        Retorna None si no se encuentra una respuesta en la tabla de rutas.
        """
        return self.routes_table.check_routes(destination_address)
        
    def receive_packet(self):
        """Recibe un paquete, si es para este router lo imprime, si no lo redirecciona."""
        packet, _ = self.socket.recvfrom(4096)
        parsed_packet = self.parse_packet(packet)

        # Si el paquete tiene TTL no positivo, se ignora
        if parsed_packet["TTL"] <= 0:
            print(f"Se recibió paquete {packet} con TTL 0")
            return

        # Si el paquete es para este router, se imprime el contenido
        packet_dest_address = (parsed_packet["IP_direction"], parsed_packet["port"])
        if packet_dest_address == self.dir:
            print("Contenido paquete recibido:",parsed_packet["data"], end = "\n\n")
            return

        # En caso contrario se redirecciona el paquete
        
        # Se decrementa el TTL del paquete
        parsed_packet['TTL'] -= 1
        packet = self.create_packet(parsed_packet)

        # Se obtiene la dirección del próximo salto
        next_hop_address = self.check_routes(packet_dest_address)
        
        # Si se encuentra dirección para próximo salto, se redirecciona
        if next_hop_address is not None:
            print(f"Redirigiendo paquete {packet} con destino final {packet_dest_address} desde {self.dir} hacia {next_hop_address}.", end = "\n\n")
            self.socket.sendto(packet, next_hop_address)
            
        # Si no se encuentra dirección para el próximo salto, se ignora el mensaje
        else:
            print(f"No hay rutas hacia {packet_dest_address} para paquete {packet}", end = "\n\n")

    def send(self, packet : bytes):
        """Envía el paquete IP recibido"""
        packet_dict = self.parse_packet(packet)
        dest_address = (packet_dict["IP_direction"], packet_dict["port"])
        next_hop_address = self.check_routes(dest_address)
        self.socket.sendto(packet, next_hop_address)