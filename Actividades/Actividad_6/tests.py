from Router_class import Router

def parameter_reception_test(IP_param, port_param, routes_table_param):
    """
    Imprime los valores de los parámetros recibidos,
    para verificar si son los esperados
    """
    print(" ===== Tests de recepción de parámetros =====")
    print(f"Router IP: {IP_param}")
    print(f"Router port: {port_param}")
    print(f"Routs table file name: {routes_table_param}")
    print()

def parse_create_packet_test():
    """Testea los métodos parse_packet y create_packet"""
    print("===== Test de parse_packet y create_packet =====")
    IP_packet_v1 = "127.0.0.1,8881,222,12345678,00000000,00001234,1,hola".encode()
    parsed_IP_packet = Router.parse_packet(IP_packet_v1)
    IP_packet_v2 = Router.create_packet(parsed_IP_packet)
    print(IP_packet_v1)
    print(IP_packet_v2)
    print("IP_packet_v1 == IP_packet_v2 ? {}".format(IP_packet_v1 == IP_packet_v2))
    print()

def check_routes_test():
    # Tests de check_routes
    print("===== Tests de check_routes =====")
    print("Tests R1")
    r1 = Router("127.0.0.1", 8881, "rutas_R1_v2.txt")
    print(f"Salto correcto para destino ('127.0.0.1', 8882)?: {('127.0.0.1', 8882) == r1.check_routes(('127.0.0.1', 8882))}")
    print(f"Salto correcto para destino ('127.0.0.1', 8883)?: {('127.0.0.1', 8882) == r1.check_routes(('127.0.0.1', 8883))}")
    print(f"Salto correcto para destino ('127.0.0.1', 8884)?: {r1.check_routes(('127.0.0.1', 8884)) is None}")
    print()

    print("Tests R2")
    r2 = Router("127.0.0.1", 8882, "rutas_R2_v2.txt")
    print(f"Salto correcto para destino ('127.0.0.1', 8881): {('127.0.0.1', 8881) == r2.check_routes(('127.0.0.1', 8881))}")
    print(f"Salto correcto para destino ('127.0.0.1', 8883): {('127.0.0.1', 8883) == r2.check_routes(('127.0.0.1', 8883))}")
    print(f"Salto correcto para destino ('127.0.0.1', 8884): {r2.check_routes(('127.0.0.1', 8884)) is None}")
    print()
    
    print("Tests R3")
    r3 = Router("127.0.0.1", 8883, "rutas_R3_v2.txt")
    print(f"Salto correcto para destino ('127.0.0.1', 8881): {('127.0.0.1', 8882) == r3.check_routes(('127.0.0.1', 8881))}")
    print(f"Salto correcto para destino ('127.0.0.1', 8882): {('127.0.0.1', 8882) == r3.check_routes(('127.0.0.1', 8882))}")
    print(f"Salto correcto para destino ('127.0.0.1', 8884): {r3.check_routes(('127.0.0.1', 8884)) is None}")


if __name__=="__main__":
    # Test de create_packet y parse_packet
    parse_create_packet_test()

    # Tests de check_routes
    #check_routes_test()