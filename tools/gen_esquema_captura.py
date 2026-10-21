"""Genera docs/esquema_captura_CAN.svg: portátil + SH-C30A + conector redondo del mazo de la E-ECU.

Uso:
    python tools/gen_esquema_captura.py docs/esquema_captura_CAN.svg
    chrome --headless=new --hide-scrollbars --window-size=1800,1100 \\
        --screenshot=docs/esquema_captura_CAN.png docs/esquema_captura_CAN.svg
"""
import math
import sys

W, H = 1800, 1100
FONT = "Segoe UI, Arial, Helvetica, sans-serif"
out = []


def a(s):
    out.append(s)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, t, size=13, fill="#1b1b1b", anchor="start", weight="normal", family=None):
    fam = f'font-family="{family}"' if family else ""
    a(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
      f'font-weight="{weight}" {fam}>{esc(t)}</text>')


C = {"canh": "#d4a017", "canl": "#2a9d4f", "gnd": "#1f1f1f", "usb": "#555555", "b4": "#1d4ed8",
     "rojo": "#d62828", "gris": "#9a9a9a"}


def wire(points, color, width=4, dash=None, halo=True):
    d = "M " + " L ".join(f"{x} {y}" for x, y in points)
    if halo:
        a(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{width + 3.5}" stroke-linejoin="round" stroke-linecap="round"/>')
    da = f'stroke-dasharray="{dash}"' if dash else ""
    a(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round" {da}/>')


def screw(x, y, r=10):
    a(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#d9d9d9" stroke="#555" stroke-width="1.5"/>')
    a(f'<line x1="{x - r + 4}" y1="{y}" x2="{x + r - 4}" y2="{y}" stroke="#555" stroke-width="2.2"/>')


def interruptor(x, y, etiqueta, estado="OFF"):
    a(f'<rect x="{x}" y="{y}" width="46" height="20" rx="3" fill="#e6e6e6" stroke="#333"/>')
    kx = x + 3 if estado == "OFF" else x + 23
    a(f'<rect x="{kx}" y="{y + 3}" width="20" height="14" rx="2" fill="#333"/>')
    text(x + 54, y + 15, f"{etiqueta}: {estado}", size=12, fill="#ffffff", weight="bold")


# ================================================================ lienzo
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
text(30, 36, "Captura del bus J1939 — portátil, adaptador SH-C30A y conector redondo del mazo de la E-ECU", size=22, weight="bold")
text(30, 58, "Solo escucha: el adaptador no transmite ni confirma tramas · ver docs/CAPTURA_CAN.md", size=13, fill="#555")

# ================================================================ portátil
a('<rect x="40" y="110" width="380" height="250" rx="12" fill="#2b2b2b" stroke="#111" stroke-width="2"/>')
# Pantalla: panel del bus en el navegador (tools/panel_bus.py, 127.0.0.1:8766)
a('<rect x="56" y="126" width="348" height="218" rx="4" fill="#f3f4f6"/>')
a('<rect x="56" y="126" width="348" height="24" rx="4" fill="#dfe3e8"/>')
for k, col in enumerate(("#ff5f57", "#febc2e", "#28c840")):
    a(f'<circle cx="{68 + k * 12}" cy="138" r="4" fill="{col}"/>')
a('<rect x="108" y="131" width="286" height="14" rx="7" fill="#ffffff"/>')
text(116, 142, "127.0.0.1:8766 · Panel bus J1939", size=10, fill="#444")
text(64, 170, "Panel bus J1939", size=13, weight="bold")
a('<rect x="296" y="157" width="100" height="18" rx="9" fill="#2a9d4f"/>')
text(346, 170, "SOLO ESCUCHA", size=10, fill="#fff", anchor="middle", weight="bold")
text(64, 188, "Recibiendo · 412 tramas/s · nodos 0x00, 0x17", size=10, fill="#555")
for k, (v, u) in enumerate([("802", "rpm"), ("9 %", "par"), ("82 °C", "refrig.")]):
    x = 64 + k * 112
    a(f'<rect x="{x}" y="196" width="104" height="44" rx="6" fill="#ffffff" stroke="#d5d9de"/>')
    text(x + 52, 220, v, size=16, anchor="middle", weight="bold")
    text(x + 52, 234, u, size=9, fill="#666", anchor="middle")
a('<rect x="64" y="248" width="216" height="58" rx="6" fill="#ffffff" stroke="#d5d9de"/>')
a('<polyline points="70,298 100,298 108,292 116,272 124,268 150,268 158,280 166,286 200,286 214,270 240,268 274,268" '
  'fill="none" stroke="#1d4ed8" stroke-width="2"/>')
text(72, 261, "rpm", size=9, fill="#666")
a('<rect x="288" y="248" width="108" height="58" rx="6" fill="#fff7e0" stroke="#e0c46c"/>')
text(342, 265, "Guía 8/12", size=10, anchor="middle", weight="bold")
text(342, 280, "Captura 3", size=9, fill="#555", anchor="middle")
text(342, 293, "ralentí", size=9, fill="#555", anchor="middle")
a('<rect x="64" y="314" width="156" height="22" rx="5" fill="#d62828"/>')
text(142, 329, "● GRABANDO 03_ralenti", size=10, fill="#fff", anchor="middle", weight="bold")
text(230, 329, "42 s / 120 s", size=10, fill="#555")
a('<path d="M 20 360 L 440 360 L 470 400 L -10 400 Z" fill="#bdbdbd" stroke="#777" stroke-width="2"/>')
text(230, 388, "Portátil de pruebas (Linux, entorno .venv)", size=13, anchor="middle", weight="bold")
a('<rect x="40" y="416" width="420" height="74" rx="8" fill="#f7f7f7" stroke="#d0d0d0"/>')
text(52, 436, "Abrir: acceso del escritorio «Panel bus J1939»", size=12, weight="bold")
text(52, 453, "o  python tools/panel_bus.py   (sin máquina: --demo)", size=11, fill="#444", family="Consolas, monospace")
text(52, 471, "Otro USB (opcional): programador → placa ESP32,", size=11, fill="#555")
text(52, 485, "acceso «Panel placa ESP32» (127.0.0.1:8765)", size=11, fill="#555")
a('<rect x="440" y="366" width="18" height="10" rx="2" fill="#666"/>')

# ================================================================ SH-C30A (enchufado directo por USB-A)
# Conector USB-A metálico entrando en el lateral del portátil
a('<rect x="452" y="346" width="74" height="40" rx="3" fill="#cfd3d6" stroke="#7d8287" stroke-width="2"/>')
for yy in (356, 372):
    a(f'<rect x="462" y="{yy}" width="14" height="6" fill="#7d8287"/>')
# Carcasa roja translúcida en forma de "botella"
a('<path d="M 526 336 L 560 336 Q 580 318 610 314 L 760 314 Q 800 314 800 340 L 800 418 '
  'Q 800 444 760 444 L 610 444 Q 580 440 560 422 L 526 422 Z" fill="#e8484f" fill-opacity="0.85" '
  'stroke="#a01c22" stroke-width="2.5"/>')
# Placa verde interior
a('<rect x="572" y="326" width="196" height="106" rx="6" fill="#1f8a43" stroke="#0f4a22"/>')
a('<rect x="590" y="360" width="40" height="40" rx="2" fill="#222" stroke="#555"/>')
text(610, 414, "STM32", size=9, fill="#d9f2df", anchor="middle")
# DIP SW1 de 2 posiciones junto al bornero: 1 = arranque (BOOT0), 2 = R120
a('<rect x="666" y="332" width="44" height="30" rx="2" fill="#1b1b1b" stroke="#000"/>')
for n, x in [("1", 671), ("2", 691)]:
    a(f'<rect x="{x}" y="336" width="14" height="22" rx="1" fill="#444"/>')
    a(f'<rect x="{x + 2}" y="338" width="10" height="9" rx="1" fill="#eeeeee"/>')   # palanca arriba = OFF (ON está abajo)
    text(x + 7, 330, n, size=9, fill="#ffffff", anchor="middle", weight="bold")
text(668, 372, "ON↓", size=8, fill="#ffffff")
for cx in (608, 628, 648, 668):
    a(f'<rect x="{cx - 3}" y="424" width="6" height="6" fill="#d8b25a"/>')
# Bornero: CAN_H arriba, GND, CAN_L abajo
a('<rect x="772" y="342" width="34" height="74" rx="3" fill="#2fa84f" stroke="#145c2a" stroke-width="1.5"/>')
for n, y in [("CAN_H", 356), ("GND", 379), ("CAN_L", 402)]:
    screw(789, y, 9)
    text(766, y + 4, n, size=10.5, fill="#ffffff", anchor="end", weight="bold")
text(640, 262, "DSD TECH SH-C30A (candleLight)", size=14, anchor="middle", weight="bold")
# Rótulo del DIP
a('<line x1="688" y1="332" x2="690" y2="303" stroke="#a01c22" stroke-width="1.5"/>')
text(610, 285, "DIP 1 (arranque): OFF", size=11, fill="#a01c22", weight="bold")
text(610, 299, "DIP 2 (R120): según medida 1", size=11, fill="#a01c22", weight="bold")
text(640, 462, "se enchufa directo al portátil (o con un alargador USB)", size=11, fill="#666", anchor="middle")

# ================================================================ conector redondo del mazo de la E-ECU + masa de chasis
# La clavija de la E-ECU (A y B en la misma carcasa) no se puede pinchar por detrás: el bus se toma
# en el conector redondo (E7 = CAN H, E8 = CAN L, medido) y la masa en un perno de chasis/motor.
# Geometría y numeración como tools/gen_conector_MC02.py (E1 = cavidad exterior vacía, sentido horario).

RX, RY0 = 1110, 235


def polar(r, ang):
    t = math.radians(ang)
    return RX + r * math.sin(t), RY0 - r * math.cos(t)


a('<rect x="900" y="90" width="860" height="400" rx="14" fill="#f4f4f4" stroke="#cfcfcf" stroke-width="2"/>')
text(1110, 114, "Conector redondo del mazo de la E-ECU (cara de contactos)", size=14, anchor="middle", weight="bold")
a(f'<rect x="{RX - 120}" y="{RY0 - 100}" width="240" height="22" rx="5" fill="#e8c200" stroke="#6b5800"/>')
a(f'<circle cx="{RX}" cy="{RY0}" r="108" fill="#151515" stroke="#000" stroke-width="3"/>')
a(f'<circle cx="{RX}" cy="{RY0}" r="94" fill="#2a2a2a" stroke="#444"/>')
EXT = [(233, False), (278, True), (325, True), (12, True), (56, True), (100, True), (144, True), (190, True)]
INT = [(260, False), (350, True), (80, True), (170, False)]
for ang, montado in INT:
    x, y = polar(44, ang)
    a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="{"#d9d9d9" if montado else "#9c7a1c"}" stroke="#111" stroke-width="2"/>')
for i, (ang, montado) in enumerate(EXT, 1):
    x, y = polar(78, ang)
    borde = "#d62828" if i == 1 else "#555"
    a(f'<rect x="{x - 10:.0f}" y="{y - 10:.0f}" width="20" height="20" rx="4" fill="#1b1b1b" stroke="{borde}" stroke-width="{2.5 if i == 1 else 1.2}"/>')
    a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{"#d9d9d9" if montado else "#000"}"/>')
    lx, ly = polar(100, ang + (16 if i == 8 else 0))   # E8: rótulo apartado del cable de CAN L
    text(f"{lx:.0f}", f"{ly + 4:.0f}", f"E{i}", size=10, fill="#ff6b6b" if i == 1 else "#ffd54a", anchor="middle", weight="bold")
a(f'<circle cx="{RX}" cy="{RY0}" r="14" fill="#d62828" stroke="#7a0f1b" stroke-width="2"/>')
a(f'<rect x="{RX - 3}" y="{RY0 - 9}" width="6" height="18" rx="2" fill="#7a0f1b"/>')
E7 = polar(78, 144)
E8 = polar(78, 190)
for (x, y), col in [(E7, C["canh"]), (E8, C["canl"])]:
    a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="none" stroke="{col}" stroke-width="4"/>')
text(915, 290, "E1 vacía", size=11, fill="#d62828", weight="bold")
text(915, 304, "(referencia)", size=11, fill="#d62828")

# Perno de masa en el chasis / motor
a('<rect x="1330" y="250" width="200" height="70" rx="6" fill="#8d9196" stroke="#555" stroke-width="2"/>')
for k in range(6):
    a(f'<line x1="{1340 + k * 32}" y1="320" x2="{1352 + k * 32}" y2="332" stroke="#555" stroke-width="2"/>')
a('<polygon points="1430,266 1446,275 1446,293 1430,302 1414,293 1414,275" fill="#d9d9d9" stroke="#444" stroke-width="2"/>')
a('<circle cx="1430" cy="284" r="7" fill="#bdbdbd" stroke="#444"/>')
text(1430, 244, "Perno de masa chasis/motor", size=13, anchor="middle", weight="bold")
text(1442, 348, "junto a la E-ECU, o negativo de batería", size=11, fill="#444")

# Notas
a('<rect x="1330" y="118" width="415" height="100" rx="8" fill="#ffffff" stroke="#d0d0d0"/>')
text(1344, 140, "Medido (2026-10-21):", size=12, weight="bold")
text(1344, 158, "E7 = CAN H (B1) · E8 = CAN L (B2)", size=12, fill="#1b1b1b")
text(1344, 176, "B4 y masa B9/B10 NO pasan por este conector", size=12, fill="#d62828", weight="bold")
text(1344, 194, "Clavija de la E-ECU: no se puede pinchar (A y B juntos)", size=11, fill="#555")
text(1344, 210, "Alternativa: clavija libre de la V-ECU, JB14 H / JB6 L", size=11, fill="#555")
text(1550, 380, "Pinzas en E7 / E8:", size=12, anchor="middle", weight="bold")
text(1550, 396, "back-probe por detrás de la pareja", size=11, fill="#444", anchor="middle")
text(1550, 411, "o adaptador en «Y» (conector enchufado)", size=11, fill="#444", anchor="middle")

# ================================================================ cables (con halo: los cruces se leen bien)
wire([(798, 402), (E8[0], 402), (E8[0], E8[1] + 13)], C["canl"])
wire([(798, 379), (835, 379), (835, 450), (1430, 450), (1430, 302)], C["gnd"])
wire([(798, 356), (E7[0], 356), (E7[0], E7[1] + 13)], C["canh"])
text(1180, 474, "masa: borne GND del SH-C30A → perno (imprescindible junto a CAN H/L)", size=11, fill="#444", anchor="middle")
text(640, 484, "CAN_H → E7 · CAN_L → E8 · GND → perno de masa", size=12, fill="#1b1b1b", anchor="middle", weight="bold")

# ================================================================ medidas con el multímetro
a('<rect x="30" y="510" width="760" height="300" rx="10" fill="#f7f7f7" stroke="#d0d0d0"/>')
text(46, 536, "1 · Antes de capturar: dos medidas con el multímetro (E7, E8 y perno de masa)", size=15, weight="bold")


def multimetro(x, y, lectura, modo):
    a(f'<rect x="{x}" y="{y}" width="120" height="190" rx="14" fill="#f2c200" stroke="#7a6000" stroke-width="2"/>')
    a(f'<rect x="{x + 12}" y="{y + 14}" width="96" height="44" rx="4" fill="#cfe3c8" stroke="#555"/>')
    text(x + 60, y + 46, lectura, size=22, fill="#1b1b1b", anchor="middle", weight="bold", family="Consolas, monospace")
    a(f'<circle cx="{x + 60}" cy="{y + 112}" r="30" fill="#333" stroke="#111"/>')
    text(x + 60, y + 117, modo, size=14, fill="#fff", anchor="middle", weight="bold")
    a(f'<circle cx="{x + 38}" cy="{y + 172}" r="7" fill="#111"/>')
    a(f'<circle cx="{x + 82}" cy="{y + 172}" r="7" fill="#d62828"/>')


multimetro(50, 560, "60.2", "Ω")
text(190, 580, "Medida 1 — llave QUITADA", size=14, weight="bold")
text(190, 602, "Resistencia entre E7 y E8", size=13)
text(190, 628, "≈ 60 Ω → DIP 2 (R120) OFF", size=13, fill="#2a9d4f", weight="bold")
text(190, 650, "≈ 120 Ω → DIP 2 (R120) ON", size=13, fill="#d62828", weight="bold")
text(190, 670, "(solo la terminación de", size=13, fill="#555")
text(190, 690, "la E-ECU: 117 Ω medidos)", size=13, fill="#555")
text(190, 710, "No puentear nada en la V-ECU", size=13, fill="#d62828")
multimetro(420, 560, "2.61", "V⎓")
text(560, 580, "Medida 2 — llave en", size=14, weight="bold")
text(560, 598, "CONTACTO, motor parado", size=14, weight="bold")
text(560, 622, "E7 → masa: 2,5–3,5 V", size=13)
text(560, 642, "E8 → masa: 1,5–2,5 V", size=13)
text(560, 666, "(≈ 2,5 V ambas en reposo)", size=12, fill="#555")
text(46, 790, "Punta negra (COM) en el perno de masa para las tensiones (si no dan ≈ 2,5 V, la masa no sirve). Anotar ambas medidas.", size=12, fill="#555")

# ================================================================ topología del bus
a('<rect x="810" y="510" width="960" height="300" rx="10" fill="#f7f7f7" stroke="#d0d0d0"/>')
text(826, 536, "2 · Topología: E-ECU, panel y V-ECU en el mismo par (sin V-ECU sigue unido)", size=15, weight="bold")
YH, YL = 650, 690


def nodo(x, y, w, h, titulo, sub, borde="#333", relleno="#ffffff", dash=None):
    da = f'stroke-dasharray="{dash}"' if dash else ""
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{relleno}" stroke="{borde}" stroke-width="2" {da}/>')
    text(x + w / 2, y + 20, titulo, size=13, anchor="middle", weight="bold")
    if sub:
        text(x + w / 2, y + 38, sub, size=11, fill="#555", anchor="middle")


def resistencia(x, rotulo="120 Ω"):
    a(f'<line x1="{x}" y1="{YH}" x2="{x}" y2="{YL}" stroke="#333" stroke-width="2"/>')
    a(f'<rect x="{x - 7}" y="{YH + 8}" width="14" height="24" rx="2" fill="#fff" stroke="#333" stroke-width="2"/>')
    text(x + 12, YH + 25, rotulo, size=11, fill="#333")


# Un solo par empalmado en el mazo: E-ECU (B1/B2) ↔ panel, con la V-ECU (JB14/JB6) como derivación.
# JB13 / JB5 son las mallas de los cables J1587 / J1939 (circuito OEM EC160B~EC460B).
wire([(905, YH), (1690, YH)], C["canh"], halo=False)
wire([(905, YL), (1690, YL)], C["canl"], halo=False)
nodo(830, 560, 150, 60, "E-ECU", "dirección 0x00")
resistencia(905, "117 Ω ✔")
a(f'<line x1="905" y1="620" x2="905" y2="{YH}" stroke="#333" stroke-width="2"/>')
nodo(1180, 560, 180, 60, "V-ECU (retirada)", "derivación · JB14 H / JB6 L", borde="#999", relleno="#fafafa", dash="7 5")
a(f'<line x1="1264" y1="620" x2="1264" y2="{YH}" stroke="{C["canh"]}" stroke-width="2.5" stroke-dasharray="6 5"/>')
a(f'<line x1="1276" y1="620" x2="1276" y2="{YL}" stroke="{C["canl"]}" stroke-width="2.5" stroke-dasharray="6 5"/>')
text(1270, 718, "JB13 / JB5 = mallas, no CAN: no puentear", size=11, fill="#d62828", anchor="middle", weight="bold")
nodo(1600, 560, 150, 60, "Panel (MDU)", "0x17 · ¿lleva 120 Ω?")
resistencia(1690, "120 Ω ?")
a(f'<line x1="1690" y1="620" x2="1690" y2="{YH}" stroke="#333" stroke-width="2"/>')
# Derivaciones: SH-C30A (ahora) y ESP32 + CAN Pal (después)
a(f'<line x1="1000" y1="{YH}" x2="1000" y2="750" stroke="{C["canh"]}" stroke-width="3"/>')
a(f'<line x1="1012" y1="{YL}" x2="1012" y2="750" stroke="{C["canl"]}" stroke-width="3"/>')
nodo(895, 750, 230, 50, "SH-C30A", "solo escucha · R120 según medida 1", borde="#1b3a6b")
a(f'<line x1="1480" y1="{YH}" x2="1480" y2="750" stroke="{C["canh"]}" stroke-width="3" stroke-dasharray="6 5"/>')
a(f'<line x1="1492" y1="{YL}" x2="1492" y2="750" stroke="{C["canl"]}" stroke-width="3" stroke-dasharray="6 5"/>')
nodo(1385, 750, 210, 50, "ESP32 + CAN Pal", "más adelante · terminación como R120", borde="#999", dash="7 5")
text(1255, 790, "derivaciones < 1 m", size=11, fill="#555", anchor="middle")

# ================================================================ seguridad y pasos
a('<rect x="30" y="830" width="1740" height="250" rx="10" fill="#fffbea" stroke="#e0c46c"/>')
text(46, 858, "3 · Seguridad y orden de trabajo", size=15, weight="bold")
izq = [
    "• Máquina estacionada, implementos apoyados, palanca de seguridad BLOQUEADA.",
    "• Selector Auto/Manual en MANUAL. Interruptor 26 en ralentí al empezar.",
    "• Conectar las sondas con la llave QUITADA; después dar contacto.",
    "• SH-C30A, DIP: 1 (arranque) en OFF; 2 (R120) OFF con 60 Ω, ON con 120 Ω (medida 1).",
    "• El panel abre el adaptador en solo escucha y no graba si no lo confirma.",
    "• Prueba previa en casa: panel con --demo (E-ECU simulada). En la máquina, seguir la guía del panel.",
]
der = [
    "01_contacto · llave en contacto, motor parado (60 s)",
    "02_arranque · empezar a grabar antes de girar la llave (60 s)",
    "03_ralenti  · motor a ralentí (120 s)",
    "04_alta     · interruptor 26 en ALTA (120 s)",
    "05_carga    · en alta moviendo brazo y cuchara (120 s)",
    "06_parada   · vuelta a ralentí y parada (60 s)",
]
for i, t in enumerate(izq):
    text(46, 886 + i * 26, t, size=13, fill="#3a3a3a")
text(930, 886, "Guía del panel (12 pasos) · cada captura tiene su botón de grabar:", size=13, weight="bold")
for i, t in enumerate(der):
    text(946, 912 + i * 24, t, size=13, fill="#3a3a3a", family="Consolas, monospace")
text(930, 1064, "Después: botón Analizar en cada captura · todo queda en capturas/ y registros/bus/",
     size=13, fill="#1d4ed8", weight="bold")

a("</svg>")
with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("ok", len(out))
