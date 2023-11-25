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


if __name__=="__main__":
    # Test de create_packet y parse_packet
    parse_create_packet_test()

    # Tests de check_routes
    #check_routes_test()