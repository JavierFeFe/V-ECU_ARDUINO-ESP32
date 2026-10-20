#!/bin/sh
# Instala las reglas udev del proyecto (adaptador CAN y programador del ESP32).
# Se ejecuta una vez en el portátil de pruebas:
#     sh tools/linux/instalar_permisos.sh
set -e
dir=$(dirname "$0")

sudo install -m 644 "$dir/70-vecu.rules" /etc/udev/rules.d/70-vecu.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
echo "Reglas instaladas en /etc/udev/rules.d/70-vecu.rules. Desenchufar y volver a enchufar los adaptadores."
