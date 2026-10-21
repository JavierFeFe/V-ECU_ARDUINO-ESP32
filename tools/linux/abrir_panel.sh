#!/bin/sh
# Lanza uno de los paneles en el navegador con el entorno .venv del proyecto.
# Lo usan los accesos del escritorio (tools/linux/instalar_accesos.sh):
#     sh tools/linux/abrir_panel.sh esp32     panel de la placa (127.0.0.1:8765)
#     sh tools/linux/abrir_panel.sh bus       panel del bus J1939 con el SH-C30A (127.0.0.1:8766)
# Si el panel ya está en marcha, solo abre el navegador. Ctrl+C (o cerrar la ventana) lo para.
cd "$(dirname "$0")/../.." || exit 1
case "$1" in
    esp32) script=tools/panel_esp32.py; titulo="Panel placa ESP32" ;;
    bus)   script=tools/panel_bus.py;   titulo="Panel bus J1939" ;;
    *) echo "Uso: $0 esp32|bus [opciones del panel]"; exit 2 ;;
esac
shift
printf '\033]0;%s\007' "$titulo"
echo "$titulo · cerrar esta ventana o Ctrl+C para pararlo"
.venv/bin/python -u "$script" "$@"
codigo=$?
if [ "$codigo" -ne 0 ] && [ "$codigo" -ne 130 ]; then
    echo
    echo "El panel terminó con error ($codigo). Pulsa Enter para cerrar."
    read -r _
fi
