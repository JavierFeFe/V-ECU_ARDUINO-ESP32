"""Genera docs/esquema_switches_SH-C30A.svg: cómo configurar el DIP del adaptador SH-C30A.

Asignación sacada del esquema oficial (github.com/dsdtech-official/can-adapters,
SH-C30A-V1.21.SchDoc): SW1 es un DIP de 2 posiciones.
    interruptor 1 (pines 1–4): BOOT0 ↔ +3V3  → ON = modo DFU (actualizar firmware)
    interruptor 2 (pines 2–3): CAN_H ↔ 120 Ω ↔ CAN_L → ON = terminación conectada

Uso:
    python tools/gen_switches_shc30a.py docs/esquema_switches_SH-C30A.svg
    chrome --headless=new --hide-scrollbars --window-size=1500,810 \\
        --screenshot=docs/esquema_switches_SH-C30A.png docs/esquema_switches_SH-C30A.svg
"""
import sys

W, H = 1500, 810
FONT = "Segoe UI, Arial, Helvetica, sans-serif"
out = []


def a(s):
    out.append(s)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, t, size=13, fill="#1b1b1b", anchor="start", weight="normal"):
    a(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
      f'font-weight="{weight}">{esc(t)}</text>')


VERDE, ROJO, GRIS, AZUL = "#2a9d4f", "#d62828", "#6c757d", "#1d4ed8"


def dip(x, y, s1, s2, escala=1.0):
    """DIP de 2 posiciones visto de frente. s1/s2: 'ON', 'OFF' o None (indiferente)."""
    w, h = 150 * escala, 120 * escala
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{6 * escala}" fill="#1b1b1b" stroke="#000" stroke-width="2"/>')
    # Marca ON abajo (comprobado en la unidad real: palanca abajo = ON, arriba = OFF)
    text(x + 12 * escala, y + h - 8 * escala, "ON", size=14 * escala, fill="#ffffff", weight="bold")
    a(f'<path d="M {x + 42 * escala} {y + h - 19 * escala} l {6 * escala} {7 * escala} l {6 * escala} {-7 * escala}" '
      f'fill="none" stroke="#fff" stroke-width="2"/>')
    for i, estado in enumerate((s1, s2)):
        cx = x + (52 + 56 * i) * escala
        top, alto = y + 30 * escala, 66 * escala
        a(f'<rect x="{cx - 17 * escala}" y="{top}" width="{34 * escala}" height="{alto}" rx="3" fill="#3a3a3a"/>')
        if estado is None:
            a(f'<rect x="{cx - 13 * escala}" y="{top + 4 * escala}" width="{26 * escala}" height="{alto - 8 * escala}" '
              f'rx="2" fill="none" stroke="#aaa" stroke-dasharray="4 3"/>')
            text(cx, top + alto / 2 + 5 * escala, "?", size=16 * escala, fill="#aaa", anchor="middle", weight="bold")
        else:
            py = top + alto / 2 if estado == "ON" else top + 4 * escala
            col = VERDE if estado == "ON" else "#eeeeee"
            a(f'<rect x="{cx - 13 * escala}" y="{py}" width="{26 * escala}" height="{alto / 2 - 4 * escala}" rx="2" fill="{col}" stroke="#222"/>')
        text(cx, y + 22 * escala, str(i + 1), size=15 * escala, fill="#ffffff", anchor="middle", weight="bold")


a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
text(30, 38, "SH-C30A — cómo poner los interruptores (DIP SW1)", size=24, weight="bold")
text(30, 62, "Palanca hacia la marca ON (abajo) = ON · hacia arriba = OFF. Cambiarlo siempre con el adaptador DESENCHUFADO del USB.",
     size=13, fill="#555")

# ---------------------------------------------------------------- qué es cada interruptor
a('<rect x="30" y="84" width="1440" height="200" rx="10" fill="#f7f7f7" stroke="#d0d0d0"/>')
dip(60, 120, "OFF", "OFF", escala=1.15)
text(260, 120, "Interruptor 1 — ARRANQUE (BOOT0)", size=17, weight="bold")
text(260, 144, "ON  → el adaptador arranca en modo DFU: solo sirve para actualizar el firmware, NO captura.", size=14)
text(260, 166, "OFF → modo de trabajo. Es su posición normal.", size=14, fill=VERDE, weight="bold")
text(260, 204, "Interruptor 2 — TERMINACIÓN R120", size=17, weight="bold")
text(260, 228, "ON  → conecta 120 Ω entre CAN_H y CAN_L (el adaptador hace de extremo del bus).", size=14)
text(260, 250, "OFF → sin resistencia. Se usa cuando el bus ya tiene sus dos terminaciones.", size=14)
text(260, 272, "Fuente: esquema oficial SH-C30A V1.21 (SW1: pines 1–4 = BOOT0↔3V3; pines 2–3 = CAN_H↔120 Ω↔CAN_L).", size=11.5, fill=GRIS)

# ---------------------------------------------------------------- casos de uso
casos = [
    ("A", "Captura en la máquina", "B1–B2 ≈ 60 Ω (medida 1)", "OFF", "OFF",
     ["El bus ya tiene dos terminaciones", "(E-ECU y panel).", "El adaptador va como derivación."], VERDE),
    ("B", "Captura en la máquina", "B1–B2 ≈ 120 Ω (medida 1)", "OFF", "ON",
     ["Solo termina la E-ECU:", "el adaptador pone la segunda", "terminación."], AZUL),
    ("C", "Prueba de banco", "SH-C30A ↔ ESP32 + CAN Pal", "OFF", "ON",
     ["Dos nodos solos en la mesa:", "R120 ON aquí y Termination ON", "en el CAN Pal (dos extremos)."], "#8338ec"),
    ("D", "Actualizar el firmware", "solo si hace falta", "ON", None,
     ["Poner 1 en ON y luego enchufar:", "aparece como dispositivo DFU.", "Al terminar, 1 en OFF y re-enchufar."], ROJO),
]
for i, (letra, titulo, sub, s1, s2, notas, color) in enumerate(casos):
    x = 30 + i * 362
    a(f'<rect x="{x}" y="304" width="346" height="330" rx="10" fill="#ffffff" stroke="{color}" stroke-width="3"/>')
    a(f'<rect x="{x}" y="304" width="346" height="58" rx="10" fill="{color}"/>')
    a(f'<rect x="{x}" y="340" width="346" height="22" fill="{color}"/>')
    text(x + 16, 332, f"{letra} · {titulo}", size=17, fill="#ffffff", weight="bold")
    text(x + 16, 353, sub, size=13, fill="#ffffff")
    dip(x + 98, 382, s1, s2, escala=1.0)
    text(x + 173, 528, f"1: {s1}   ·   2: {s2 if s2 else 'indiferente'}", size=16, anchor="middle", weight="bold")
    for j, n in enumerate(notas):
        text(x + 173, 566 + j * 22, n, size=13.5, fill="#333", anchor="middle")

# ---------------------------------------------------------------- comprobación
a('<rect x="30" y="654" width="1440" height="136" rx="10" fill="#fffbea" stroke="#e0c46c"/>')
text(46, 682, "Comprobación con el multímetro (adaptador desenchufado y sin cables en el bornero)", size=15, weight="bold")
text(46, 710, "• Resistencia entre los tornillos CAN_H y CAN_L: con el interruptor 2 en ON ≈ 120 Ω; en OFF, circuito abierto (OL).", size=14)
text(46, 736, "• Así se confirma qué interruptor es la terminación antes de ir a la máquina, por si una unidad viniera distinta.", size=14)
text(46, 762, "• En la máquina, conectar el adaptador con la llave QUITADA y repetir la medida 1 (B1–B2) con el interruptor 2 ya puesto:", size=14)
text(62, 782, "el resultado debe ser ≈ 60 Ω (bus con dos terminaciones). Si da ≈ 40 Ω sobra una: poner el interruptor 2 en OFF.", size=14, fill=ROJO)

a("</svg>")
with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("ok", len(out))
