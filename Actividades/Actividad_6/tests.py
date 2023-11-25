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

def fragment_IP_packet_test():
    """Testea el método de fragmentación de paquetes IP"""
    print("===== Test de fragment_IP_packet =====")
    # Fragmentación cualquiera
    packet_1 = b"127.0.0.1,8885,010,00000347,00000000,00000005,0,hola!"
    fragments_list_1 = Router.fragment_IP_packet(packet_1, 51)
    expected_list_1 = [b"127.0.0.1,8885,010,00000347,00000000,00000003,1,hol",
                       b"127.0.0.1,8885,010,00000347,00000003,00000002,0,a!"]
    print(f"Fragmentación 1 correcta?: {fragments_list_1 == expected_list_1}")

    # Caso que no se fragmenta
    fragments_list_2 = Router.fragment_IP_packet(packet_1, 60)
    expected_list_2 = [packet_1]
    print(f"Fragmentación 2 correcta?: {fragments_list_2 == expected_list_2}")

    # Caso que todos los fragmentos tienen flag 1
    packet_2 = b"127.0.0.1,8885,010,00000347,00000000,00000005,1,hola!"
    fragments_list_3 = Router.fragment_IP_packet(packet_2, 51)
    expected_list_3 = [b"127.0.0.1,8885,010,00000347,00000000,00000003,1,hol",
                       b"127.0.0.1,8885,010,00000347,00000003,00000002,1,a!"]
    print(f"Fragmentación 3 correcta?: {fragments_list_3 == expected_list_3}")
    print()

def reassemble_IP_packet_test():
    print("===== Test de re-ensamble de reassemble_IP_packet =====")
    packet_1 = b"127.0.0.1,8885,010,00000347,00000000,00000005,0,hola!"
    mtu = 51
    fragment_list = Router.fragment_IP_packet(packet_1, mtu)
    reassambled_packet = Router.reassemble_IP_packet(fragment_list)
    print(f"Re-ensamble de paquete IP 1 consistente?: {packet_1 == reassambled_packet}")
    print()

if __name__=="__main__":
    # Test de create_packet y parse_packet
    parse_create_packet_test()
    fragment_IP_packet_test()
    reassemble_IP_packet_test()    