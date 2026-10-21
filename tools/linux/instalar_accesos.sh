#!/bin/sh
# Crea en el escritorio los accesos a los dos paneles (placa ESP32 y bus J1939).
#     sh tools/linux/instalar_accesos.sh
set -e
repo=$(cd "$(dirname "$0")/../.." && pwd)
escritorio=$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")
mkdir -p "$escritorio"

crear() {  # crear <fichero> <nombre> <comentario> <panel> <icono>
    f="$escritorio/$1"
    cat > "$f" <<EOF
[Desktop Entry]
Type=Application
Name=$2
Comment=$3
Exec=sh "$repo/tools/linux/abrir_panel.sh" $4
Path=$repo
Icon=$5
Terminal=true
Categories=Development;Electronics;
EOF
    chmod +x "$f"
    echo "Creado: $f"
}

crear "panel_placa_esp32.desktop" "Panel placa ESP32" \
    "Modos, relé, ajustes y log de la placa V-ECU (127.0.0.1:8765)" esp32 cpu
crear "panel_bus_j1939.desktop" "Panel bus J1939" \
    "Lectura y grabación del bus de la EC210B con el SH-C30A, solo escucha (127.0.0.1:8766)" bus network-wired
