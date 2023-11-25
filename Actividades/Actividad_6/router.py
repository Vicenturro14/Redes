import sys
from tests import *
from Router_class import Router


if len(sys.argv) != 4:
    raise Exception(f"El programa requiere recibir 3 argumentos al correrlo y se recibieron {len(sys.argv) - 1}.")

# Se recibe la dirección IP, el puerto y el nombre de la tabla de rutas
_, ROUTER_IP, ROUTER_PORT, ROUTES_TABLE_FILENAME = sys.argv

# Test de recepción de parámetros
parameter_reception_test(ROUTER_IP, ROUTER_PORT, ROUTES_TABLE_FILENAME)


router = Router(ROUTER_IP, int(ROUTER_PORT), ROUTES_TABLE_FILENAME)

# Se reciben paquetes en un loop
try:
    while True:
        router.receive_packet()
except KeyboardInterrupt:
    print("\nAdios :)")