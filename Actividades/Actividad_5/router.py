import sys
import socket
from utilities import *

if len(sys.argv) != 4:
    print(f"El programa requiere recibir 3 argumentos y se recibieron {len(sys.argv)}.")
else:
    # Se recibe la dirección IP, el puerto y el nombre de la tabla de rutas
    _, ROUTER_IP, ROUTER_PORT, ROUTES_TABLE_FILENAME = sys.argv
    ROUTER_DIR = (ROUTER_IP, int(ROUTER_PORT))

    # Se guarda la tabla de rutas en una lista de diccionarios
    routs_table = []
    with open(ROUTES_TABLE_FILENAME) as file:
        for rout in file:
            rout_dict = {}
            rout_list = rout.split()
            rout_dict["IP_range"] = rout_list[0]
            rout_dict["port_range_first"] = rout_list[1]
            rout_dict["port_range_last"] = rout_list[2]
            rout_dict["IP_to_follow"] = rout_list[3]
            rout_dict["port_to_follow"] = rout_list[4]
            routs_table.append(rout_dict)

    # Tests de recepción de parámetros
    print(" ===== Tests de recepción de parámetros =====")
    print(f"Router IP: {ROUTER_IP}")
    print(f"Router port: {ROUTER_PORT}")
    print(f"Routs table file name: {ROUTES_TABLE_FILENAME}")
    print()

    # Se crea el socket del router
    router_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    router_socket.bind(ROUTER_DIR)

    # Tests de parse_packet y create_packet
    print("===== Test de parse_packet y create_packet =====")
    IP_packet_v1 = "127.0.0.1,8881,hola".encode()
    parsed_IP_packet = parse_packet(IP_packet_v1)
    IP_packet_v2 = create_packet(parsed_IP_packet)
    print(IP_packet_v1)
    print(IP_packet_v2)
    print("IP_packet_v1 == IP_packet_v2 ? {}".format(IP_packet_v1 == IP_packet_v2))
    print()

    # Tests de check_routes
    print("===== Tests de check_routes =====")
    print("Tests R1")
    print(f"Siguiente salto para destino ('127.0.0.1', 8882): {check_routes('rutas_R1_v2.txt', ('127.0.0.1', 8882))}")
    print(f"Siguiente salto para destino ('127.0.0.1', 8883): {check_routes('rutas_R1_v2.txt', ('127.0.0.1', 8883))}")
    print(f"Siguiente salto para destino ('127.0.0.1', 8884): {check_routes('rutas_R1_v2.txt', ('127.0.0.1', 8884))}")
    print()
    print("Tests R2")
    print(f"Siguiente salto para destino ('127.0.0.1', 8881): {check_routes('rutas_R2_v2.txt', ('127.0.0.1', 8881))}")
    print(f"Siguiente salto para destino ('127.0.0.1', 8883): {check_routes('rutas_R2_v2.txt', ('127.0.0.1', 8883))}")
    print(f"Siguiente salto para destino ('127.0.0.1', 8884): {check_routes('rutas_R2_v2.txt', ('127.0.0.1', 8884))}")
    print()
    print("Tests R3")
    print(f"Siguiente salto para destino ('127.0.0.1', 8881): {check_routes('rutas_R3_v2.txt', ('127.0.0.1', 8881))}")
    print(f"Siguiente salto para destino ('127.0.0.1', 8882): {check_routes('rutas_R3_v2.txt', ('127.0.0.1', 8882))}")
    print(f"Siguiente salto para destino ('127.0.0.1', 8884): {check_routes('rutas_R3_v2.txt', ('127.0.0.1', 8884))}")
