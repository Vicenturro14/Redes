import sys
import socket
from Router_class import Router

if len(sys.argv) != 4:
    raise Exception(f"El programa requiere recibir 3 argumentos al correrlo sy se recibieron {len(sys.argv) - 1}.")

# Se recibe la dirección IP, el puerto y el nombre de la tabla de rutas
_, ROUTER_IP, ROUTER_PORT, ROUTES_TABLE_FILENAME = sys.argv

# Tests de recepción de parámetros
print(" ===== Tests de recepción de parámetros =====")
print(f"Router IP: {ROUTER_IP}")
print(f"Router port: {ROUTER_PORT}")
print(f"Routs table file name: {ROUTES_TABLE_FILENAME}")
print()

router = Router(ROUTER_IP, int(ROUTER_PORT), ROUTES_TABLE_FILENAME)

# Se reciben paquetes en un loop
while True:
    router.receive_packet()