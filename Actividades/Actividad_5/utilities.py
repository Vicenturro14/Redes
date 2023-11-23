
def parse_packet(IP_packet : bytes) -> dict[str, str | int]:
    """Retorna un diccionario con los headers y el mensaje del paquete IP recibido."""
    IP_direction, port, data = IP_packet.decode().split(",")
    return {"IP_direction" : IP_direction, "port" : int(port), "data" : data}  

def create_packet(IP_packet_dict : dict[str, str | int]) -> bytes:
    """Retorna una cadena de bytes correspondiente al paquete IP representado en el diccionario recibido."""
    return f"{IP_packet_dict['IP_direction']},{IP_packet_dict['port']},{IP_packet_dict['data']}".encode()

def check_routes(routes_file_name : str, destination_address : tuple[str, int]) -> tuple[str, int] | None:
    """Retorna una tupla con la dirección IP y el puerto del siguiente salto
    indicado por la tabla de rutas para llegar a la dirección de destino recibida.
    Retorna None si no se encuentra una respuesta en la tabla de rutas."""
    IP_dest, port_dest = destination_address
    with open(routes_file_name) as file:
        for route in file:
            route_list = route.split()
            if IP_dest in ["localhost", "127.0.0.1"] and int(route_list[1]) <= port_dest <= int(route_list[2]):
                return (route_list[3], int(route_list[4]))
        return None
    