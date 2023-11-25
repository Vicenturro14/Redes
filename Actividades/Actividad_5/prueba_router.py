import sys
import socket
from Router_class import Router

if len(sys.argv) != 4:
    raise Exception(f"El programa requiere recibir 3 argumentos al correrlo y se recibieron {len(sys.argv) - 1}.")

# Se reciben los parámetros
_, headers_IP, router_IP, router_port = sys.argv

# Se leen las líneas del archivo
lines_to_send = []
with open("many_lines_file.txt") as file:
    for line in file:
        lines_to_send.append(headers_IP + ',' + line + "\n")
        

# Se utiliza la tabla correspondiende al puerto recibido como parámetro
routes_table_file_name = f"rutas_R{int(router_port)%10}_v3.txt"
router = Router(router_IP, int(router_port), routes_table_file_name)

# Se envían las líneas del
for packet in lines_to_send:
    router.send(packet.encode())
