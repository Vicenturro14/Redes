import socket
from RoutesTable import RoutesTable
import math

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

    def check_routes(self, destination_address : tuple[str, int]) -> tuple[tuple[str, int], int] | None:
        """
        Retorna un par con la dirección (IP, puerto) y el MTU de la ruta del 
        siguiente salto indicado por la tabla de rutas para llegar a la 
        dirección de destino recibida. Retorna None si no se encuentra una 
        respuesta en la tabla de rutas.
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
        next_hop_address, route_mtu = self.check_routes(packet_dest_address)
        
        # Si no se encuentra dirección para próximo salto, se desecha
        if next_hop_address is None:
            print(f"No hay rutas hacia {packet_dest_address} para paquete {packet}", end = "\n\n")
            return    

        # Fragmenta el paquete IP y envía cada fragmento
        fragments_list = self.fragment_IP_packet(packet, route_mtu)
        for fragment in fragments_list:
            print(f"Redirigiendo paquete {fragment} con destino final {packet_dest_address} desde {self.dir} hacia {next_hop_address}.", end = "\n\n")
            self.socket.sendto(fragment, next_hop_address)


    def send(self, packet : bytes):
        """Envía el paquete IP recibido"""
        packet_dict = self.parse_packet(packet)
        dest_address = (packet_dict["IP_direction"], packet_dict["port"])
        next_hop_address, route_mtu = self.check_routes(dest_address)
        fragment_list = self.fragment_IP_packet(packet, route_mtu)
        for fragment in fragment_list:    
            self.socket.sendto(fragment, next_hop_address)

    @staticmethod
    def fragment_IP_packet(IP_packet : bytes, MTU : int) -> list[bytes]:
        """
        Fragmenta el paquete IP recibido para tener paquetes que sean de 
        tamaño menor o igual al MTU. Retorna una lista con los fragmentos
        de paquetes.
        """
        # Si el tamaño del paquete IP es menor o igual al MTU no se requiere 
        # de fragmentación
        original_packet_size = len(IP_packet)
        if original_packet_size <= MTU:
            return [IP_packet]
        
        original_packet_dict = Router.parse_packet(IP_packet)
        headers_size = original_packet_size - original_packet_dict["size"]
        new_data_area_size = MTU - headers_size
        
        fragments_num = math.ceil(original_packet_dict["size"]/new_data_area_size)

        fragments_list = []
        fragment_dict = original_packet_dict.copy()
        for i in range(fragments_num):
            # Se calcula el offset
            offset = i * new_data_area_size
            fragment_dict["offset"] = offset

            # Se obtienen los datos de este fragmento
            fragment_data = original_packet_dict["data"][offset : offset + new_data_area_size]
            fragment_dict["data"] = fragment_data
            fragment_dict["size"] = len(fragment_data)
            
            # Se obtiene la flag del fragmento
            # Solo si la flag del paquete original es cero y este es el último
            # fragmento, la flag del fragmento es 0
            if original_packet_dict["flag"] == 0 and i == fragments_num - 1:
                fragment_dict["flag"] = 0
            else: 
                fragment_dict["flag"] = 1

            # Se crea el fragmento en bytes y se agrega a la lista
            fragment = Router.create_packet(fragment_dict)
            fragments_list.append(fragment)

        return fragments_list
        
    @staticmethod
    def reassemble_IP_packet(fragment_list : list[bytes]):
        # Se crea una lista de los fragmentos paseados
        parsed_fragment_list = [Router.parse_packet(fragment) for fragment in fragment_list]
        
        # Si hay solo un fragmento 
        if len(parsed_fragment_list) == 1:
            # Si el fragmento tiene offset o flag distinto a 0, faltan fragmentos
            if parsed_fragment_list[0]["flag"] != 0 or parsed_fragment_list[0]["offset"] != 0:
                return None
            return fragment_list[0]
        
        # Se ordena la lista de fragmentos parseados por su offset
        parsed_fragment_list.sort(key= lambda x : x["offset"])

        # Si el primer fragmento no tiene offset 0 o el último fragmento tiene flag en 1, faltan fragmentos
        if parsed_fragment_list[0]["offset"] != 0 or parsed_fragment_list[-1]["flag"] == 1:
            return None
        
        # Se re-ensambla los fragmentos
        bytes_sum = 0
        reassambled_data = ""
        for parsed_fragment in parsed_fragment_list:
            # Si el offset no coincide con la cantidad de bytes re-ensamblados, faltan fragmentos
            if parsed_fragment["offset"] != bytes_sum:
                return None
            
            reassambled_data += parsed_fragment["data"]
            bytes_sum += parsed_fragment["size"]

        # Se reutilizan los headers de dirección IP, puerto, TTL, id y offset del primer fragmento  
        reassambled_packet_dict = parsed_fragment_list[0]
        reassambled_packet_dict["size"] = bytes_sum
        reassambled_packet_dict["flag"] = 0
        reassambled_packet_dict["data"] = reassambled_data
        
        return Router.create_packet(reassambled_packet_dict)

