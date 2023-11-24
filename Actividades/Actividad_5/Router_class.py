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

        


    def tests(self):
        # Tests de parse_packet y create_packet
        print("===== Test de parse_packet y create_packet =====")
        IP_packet_v1 = "127.0.0.1,8881,hola".encode()
        parsed_IP_packet = self.parse_packet(IP_packet_v1)
        IP_packet_v2 = self.create_packet(parsed_IP_packet)
        print(IP_packet_v1)
        print(IP_packet_v2)
        print("IP_packet_v1 == IP_packet_v2 ? {}".format(IP_packet_v1 == IP_packet_v2))
        print()

        # Tests de check_routes
        print("===== Tests de check_routes =====")
        print("Tests R1")
        print(f"Siguiente salto para destino ('127.0.0.1', 8882): {self.check_routes('rutas_R1_v2.txt', ('127.0.0.1', 8882))}")
        print(f"Siguiente salto para destino ('127.0.0.1', 8883): {self.check_routes('rutas_R1_v2.txt', ('127.0.0.1', 8883))}")
        print(f"Siguiente salto para destino ('127.0.0.1', 8884): {self.check_routes('rutas_R1_v2.txt', ('127.0.0.1', 8884))}")
        print()
        print("Tests R2")
        print(f"Siguiente salto para destino ('127.0.0.1', 8881): {self.check_routes('rutas_R2_v2.txt', ('127.0.0.1', 8881))}")
        print(f"Siguiente salto para destino ('127.0.0.1', 8883): {self.check_routes('rutas_R2_v2.txt', ('127.0.0.1', 8883))}")
        print(f"Siguiente salto para destino ('127.0.0.1', 8884): {self.check_routes('rutas_R2_v2.txt', ('127.0.0.1', 8884))}")
        print()
        print("Tests R3")
        print(f"Siguiente salto para destino ('127.0.0.1', 8881): {self.check_routes('rutas_R3_v2.txt', ('127.0.0.1', 8881))}")
        print(f"Siguiente salto para destino ('127.0.0.1', 8882): {self.check_routes('rutas_R3_v2.txt', ('127.0.0.1', 8882))}")
        print(f"Siguiente salto para destino ('127.0.0.1', 8884): {self.check_routes('rutas_R3_v2.txt', ('127.0.0.1', 8884))}")


    @staticmethod
    def parse_packet(IP_packet : bytes) -> dict[str, str | int]:
        """Retorna un diccionario con los headers y el mensaje del paquete IP recibido."""
        IP_direction, port, data = IP_packet.decode().split(",")
        return {"IP_direction" : IP_direction, "port" : int(port), "data" : data}  
    
    @staticmethod
    def create_packet(IP_packet_dict : dict[str, str | int]) -> bytes:
        """Retorna una cadena de bytes correspondiente al paquete IP representado en el diccionario recibido."""
        return f"{IP_packet_dict['IP_direction']},{IP_packet_dict['port']},{IP_packet_dict['data']}".encode()

    def check_routes(self, destination_address : tuple[str, int]) -> tuple[str, int] | None:
        """
        Retorna la dirección (IP, puerto) del siguiente salto indicado por
        la tabla de rutas para llegar a la dirección de destino recibida.
        Retorna None si no se encuentra una respuesta en la tabla de rutas.
        """
        return self.routes_table.check_routes(destination_address)
        
    def receive_packet(self):
        """Recibe un paquete, si es para este router lo imprime, si no lo redirecciona."""
        package, _ = self.socket.recvfrom(4096)
        parsed_packet = self.parse_packet(package)
        packet_dest_address = (parsed_packet["IP_direction"], parsed_packet["port"])
        # Si el paquete es para este router, se imprime el contenido
        if packet_dest_address == self.dir:
            print("Contenido paquete recibido:",parsed_packet["data"], end = "\n\n")
        
        # En caso contrario se redirecciona el paquete
        else:
            # Se obtiene la dirección del próximo salto
            next_hop_dir = self.check_routes(packet_dest_address)

            # Si se encuentra dirección para próximo salto, se redirecciona a esa dirección
            if next_hop_dir is not None:
                print(f"Redirigiendo paquete {package} con destino final {packet_dest_address} desde {self.dir} hacia {next_hop_dir}.", end = "\n\n")
                self.socket.sendto(package, next_hop_dir)
                
            # Si no se encuentra dirección para el próximo salto, se ignora el mensaje
            else:
                print(f"No hay rutas hacia {packet_dest_address} para paquete {package}", end = "\n\n")