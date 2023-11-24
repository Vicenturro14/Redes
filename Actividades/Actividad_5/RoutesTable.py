class RoutesTable:
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        
        # Lista con los rangos de puertos, 
        # en el orden que aparecen en el archivo de texto
        self.port_ranges = []

        # Diccionario que guarda las posibles rutas, 
        # la última ruta tomada y la pŕoxima ruta por tomar,
        # de cada rango de puertos de destino
        self.round_robin_logic = {}
        
        # Se parsea la tabla de rutas y se guarda en la lista y diccionario anterior.
        with open(self.file_name) as file:
            for rout in file:
                rout_list = rout.split()
                port_range = (int(rout_list[1]), int(rout_list[2]))
                next_hop = (rout_list[3], int(rout_list[4]))
                
                # Si el rango de puertos no se encuentra en la lista, 
                # se agrega a la lista y al diccionario. 
                if port_range not in self.port_ranges:
                    self.port_ranges.append(port_range)
                    self.round_robin_logic[port_range] = {"routes" : [], "prev_route_index" : None, "next_route_index": 0}

                self.round_robin_logic[port_range]["routes"].append(next_hop)


    def check_routes(self, destination_address : tuple[str, int]) -> tuple[str, int] | None:
        """
        Retorna la dirección (IP, puerto) del siguiente salto para llegar a la
        dirección de destino recibida. En caso de haber varias rutas
        disponibles para llegar a un destino, se utiliza Round Robin para 
        decidir cual ruta tomar. Retorna None si no se encuentra una respuesta
        en la tabla de rutas.
        """
        _, dest_port = destination_address
        for port_range in self.port_ranges:
            if port_range[0] <= dest_port <= port_range[1]:
                # Se obtiene la dirección del siguiente salto 
                next_hop_index = self.round_robin_logic[port_range]["next_route_index"]
                next_hop_dir = self.round_robin_logic[port_range]["routes"][next_hop_index]

                # Se actualiza la última ruta utilizada y la siguiente a utilizar
                routes_num = len(self.round_robin_logic[port_range]["routes"])
                self.round_robin_logic[port_range]["prev_route_index"] = next_hop_index
                self.round_robin_logic[port_range]["next_route_index"] = (next_hop_index + 1) % routes_num
                
                return next_hop_dir
            
        return None