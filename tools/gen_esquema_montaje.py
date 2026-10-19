"""Genera docs/esquema_montaje_ESP32.svg: placa vista por delante (componentes).

Uso:
    python tools/gen_esquema_montaje.py docs/esquema_montaje_ESP32.svg
    chrome --headless=new --hide-scrollbars --window-size=2000,1200         --screenshot=docs/esquema_montaje_ESP32.png docs/esquema_montaje_ESP32.svg
"""
import math
import sys

W, H = 2000, 1200
FONT = "Segoe UI, Arial, Helvetica, sans-serif"
out = []


def a(s):
    out.append(s)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, t, size=13, fill="#1b1b1b", anchor="start", weight="normal", extra=""):
    a(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
      f'font-weight="{weight}" {extra}>{esc(t)}</text>')


C = {
    "24v": "#d62828", "gnd": "#1f1f1f", "3v3": "#f77f00",
    "canh": "#d4a017", "canl": "#2a9d4f", "b4": "#1d4ed8",
    "sda": "#9b5de5", "scl": "#e0459b", "tx": "#0077b6", "rx": "#00a6a6", "slnt": "#6c757d",
    "clk": "#e76f51", "dt": "#43aa8b", "sw": "#577590",
    "ptx": "#4361ee", "prx": "#3aa6d0", "g0": "#8338ec", "opt": "#9a9a9a",
}


def wire(points, color, width=3.6, dash=None, halo=True):
    d = "M " + " L ".join(f"{x} {y}" for x, y in points)
    if halo:
        a(f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="{width + 3.5}" '
          f'stroke-linejoin="round" stroke-linecap="round"/>')
    da = f'stroke-dasharray="{dash}"' if dash else ""
    a(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
      f'stroke-linejoin="round" stroke-linecap="round" {da}/>')


def chip(cx, cy, t, fill=None, w=30, h=16):
    if fill:
        a(f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="3" fill="{fill}" '
          f'stroke="#ffffff" stroke-width="1.2"/>')
        tc = "#ffffff"
    else:
        tc = "#d9f2df"
    text(cx, cy + 4, t, size=10, fill=tc, anchor="middle", weight="bold" if fill else "normal")


def hole(x, y, r=7, square=False):
    if square:
        a(f'<rect x="{x - r - 1}" y="{y - r - 1}" width="{2 * r + 2}" height="{2 * r + 2}" fill="#d8b25a" stroke="#8a6a20"/>')
    else:
        a(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#d8b25a" stroke="#8a6a20" stroke-width="1"/>')
    a(f'<circle cx="{x}" cy="{y}" r="{r * 0.45}" fill="#2b2b2b"/>')


def pad(x, y, color="#d8b25a"):
    a(f'<rect x="{x - 5}" y="{y - 5}" width="10" height="10" rx="1.5" fill="{color}" stroke="#7a5a10" stroke-width="1"/>')


def screw(x, y, r=13):
    a(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#d9d9d9" stroke="#555" stroke-width="1.5"/>')
    a(f'<line x1="{x - r + 5}" y1="{y}" x2="{x + r - 5}" y2="{y}" stroke="#555" stroke-width="2.5"/>')


# ================================================================ lienzo
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
text(30, 34, "Montaje del control de rpm — placa ESP32_Relay X1 V1.2, módulos y máquina", size=22, weight="bold")
text(30, 56, "Placa vista por delante (cara de componentes) · pines con su número de GPIO · ver docs/MONTAJE.md",
     size=13, fill="#555")

# ================================================================ leyenda
lx, ly = 1180, 18
a(f'<rect x="{lx}" y="{ly}" width="800" height="104" rx="8" fill="#f7f7f7" stroke="#d0d0d0"/>')
text(lx + 14, ly + 20, "Colores de cable", size=13, weight="bold")
leg = [
    ("24v", "+24 V / COM del relé"), ("b4", "NO del relé → línea B4"), ("gnd", "GND / masa"),
    ("canh", "CAN H (amarillo)"), ("canl", "CAN L (verde)"), ("tx", "CAN TX / RX → IO17 / IO18"),
    ("slnt", "SLNT del CAN Pal → IO4"), ("sda", "I²C SDA / SCL → IO21 / IO22"), ("clk", "Encoder → IO32 / IO33 / IO27"),
    ("ptx", "Serie del programador"), ("3v3", "3V3 (pin naranja)"),
]
for i, (k, t) in enumerate(leg):
    col, row = i % 3, i // 3
    x0, y0 = lx + 16 + col * 262, ly + 40 + row * 17
    wire([(x0, y0), (x0 + 28, y0)], C[k], halo=False)
    text(x0 + 36, y0 + 4, t, size=12)
x0, y0 = lx + 16 + 2 * 262, ly + 40 + 3 * 17
wire([(x0, y0), (x0 + 28, y0)], C["opt"], width=3, dash="6 5", halo=False)
text(x0 + 36, y0 + 4, "Opcional / sin conectar", size=12)

a('<g transform="translate(0,-100)">')
# ================================================================ placa (vista por delante)
BX, BY, BW, BH = 620, 260, 810, 780
a(f'<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="22" fill="#1f8a43" stroke="#0f4a22" stroke-width="3"/>')
for hx, hy in [(BX + 26, BY + 26), (BX + BW - 26, BY + BH - 26), (BX + 26, BY + BH - 26)]:
    a(f'<circle cx="{hx}" cy="{hy}" r="12" fill="#ffffff" stroke="#c8a35a" stroke-width="3"/>')
text(BX + 70, BY + BH - 18, "LC · ESP32_Relay X1 V1.2 — vista por delante", size=12, fill="#d9f2df")

# Fuente: XL7005, bobina, condensadores, regulador, micro-USB, botón IO0
a('<rect x="738" y="300" width="56" height="34" rx="3" fill="#1b1b1b" stroke="#444"/>')
text(766, 346, "XL7005", size=10, fill="#d9f2df", anchor="middle")
a('<rect x="742" y="594" width="56" height="50" rx="6" fill="#2d2d2d" stroke="#111"/>')
text(770, 624, "470", size=12, fill="#bbbbbb", anchor="middle")
a('<circle cx="846" cy="618" r="20" fill="#222" stroke="#666" stroke-width="2"/>')
a('<circle cx="672" cy="597" r="32" fill="#222" stroke="#777" stroke-width="2"/>')
a('<path d="M 652 575 L 692 575" stroke="#999" stroke-width="3"/>')
a('<rect x="790" y="732" width="62" height="40" rx="3" fill="#1b1b1b" stroke="#444"/>')
text(821, 786, "AMS1117", size=10, fill="#d9f2df", anchor="middle")
a('<rect x="622" y="748" width="58" height="40" rx="4" fill="#c0c0c0" stroke="#777" stroke-width="1.5"/>')
text(628, 738, "micro-USB (solo 5 V)", size=10, fill="#d9f2df")
a('<rect x="786" y="918" width="48" height="48" rx="4" fill="#d0d0d0" stroke="#666"/>')
a('<circle cx="810" cy="942" r="13" fill="#222"/>')
text(810, 986, "botón IO0", size=11, fill="#ffffff", anchor="middle", weight="bold")
a('<rect x="935" y="965" width="14" height="9" fill="#ffffff" stroke="#888"/>')
text(942, 994, "D4", size=10, fill="#d9f2df", anchor="middle")

# Borne de alimentación (− arriba, + abajo)
a('<rect x="604" y="356" width="72" height="128" rx="4" fill="#2fa84f" stroke="#145c2a" stroke-width="2"/>')
screw(640, 384)
screw(640, 456)
text(690, 388, "−  GND", size=13, fill="#ffffff", weight="bold")
text(690, 460, "+  VCC", size=13, fill="#ffffff", weight="bold")
text(690, 476, "7–60 V", size=10, fill="#d9f2df")

# Relé y su borne (NC arriba, COM, NO abajo)
a('<rect x="1005" y="272" width="290" height="200" rx="6" fill="#1f5fbf" stroke="#0d3a7a" stroke-width="2"/>')
text(1150, 330, "SRD-05VDC-SL-C", size=15, fill="#ffffff", anchor="middle", weight="bold")
text(1150, 352, "SONGLE · 10 A 30 VDC", size=12, fill="#dbe7ff", anchor="middle")
text(1150, 380, "relé → IO16 (confirmado)", size=12, fill="#ffffff", anchor="middle", weight="bold")
a('<rect x="928" y="300" width="14" height="9" fill="#ff6b6b" stroke="#888"/>')
text(935, 292, "LED relé", size=10, fill="#ffffff", anchor="middle")
a('<rect x="1318" y="278" width="78" height="208" rx="4" fill="#2fa84f" stroke="#145c2a" stroke-width="2"/>')
for n, y in [("NC", 312), ("COM", 383), ("NO", 456)]:
    screw(1357, y, 14)
    text(1310, y + 4, n, size=12, fill="#ffffff", anchor="end", weight="bold")
text(1310, 326, "(libre)", size=10, fill="#d9f2df", anchor="end")

# P4 (programación) encima del módulo
P4 = [("IO0", 1085), ("GND", 1115), ("GND", 1145), ("RX", 1175), ("TX", 1205), ("5V", 1235)]
a('<rect x="1068" y="530" width="184" height="30" rx="4" fill="#123d1f"/>')
for n, x in P4:
    hole(x, 545, r=8, square=(n == "5V"))
    text(x, 576, n, size=11, fill="#ffffff", anchor="middle", weight="bold")
text(1060, 550, "P4", size=13, fill="#ffffff", anchor="end", weight="bold")

# Módulo ESP32-WROOM-32E (antena abajo)
a('<rect x="1030" y="642" width="266" height="392" rx="6" fill="#bfc4c9" stroke="#80868c" stroke-width="2"/>')
a('<rect x="1046" y="660" width="234" height="290" rx="4" fill="#d6dade" stroke="#9aa0a6"/>')
text(1163, 780, "ESP32-WROOM-32E", size=15, fill="#333", anchor="middle", weight="bold")
text(1163, 800, "ESPRESSIF", size=12, fill="#555", anchor="middle")
a('<rect x="1046" y="958" width="234" height="66" rx="3" fill="#1c1c1c"/>')
a('<path d="M 1066 1006 L 1066 976 L 1096 976 L 1096 1006 L 1126 1006 L 1126 976 L 1156 976 L 1156 1006 L 1186 1006 L 1186 976 L 1216 976 L 1216 1006 L 1260 1006" fill="none" stroke="#d8b25a" stroke-width="3"/>')
text(1163, 1000, "antena", size=10, fill="#bbbbbb", anchor="middle")

# Tiras de pines (2×10). Rango k: 0 arriba (junto a P4), 9 abajo (junto a la antena).
RK = [583 + 43 * k for k in range(10)]
# Tira izquierda (serigrafía "superior"): exterior = fila CLK…, interior = fila 3V3…
IZQ_EXT = ["IO6", "IO8", "IO2", "IO4", "IO17", "IO18", "GND", "IO3", "IO22", "GND"]
IZQ_INT = ["3V3", "IO7", "IO15", "IO0", "IO16", "IO5", "IO19", "IO21", "IO1", "IO23"]
# Tira derecha (serigrafía "inferior"): interior = fila GND…, exterior = fila 5V…
DER_INT = ["GND", "IO11", "IO9", "IO12", "IO27", "IO25", "IO32", "IO34", "IO36", "3V3"]
DER_EXT = ["5V", "IO10", "IO13", "IO14", "IO26", "IO33", "IO35", "IO39", "EN", "GND"]
XI_E, XI_I, XD_I, XD_E = 923, 956, 1340, 1373
hl_ie = {3: C["slnt"], 4: C["tx"], 5: C["rx"], 6: C["gnd"], 8: C["scl"], 9: C["gnd"]}
hl_ii = {0: C["3v3"], 7: C["sda"]}
hl_di = {0: C["gnd"], 4: C["sw"], 6: C["clk"], 9: C["3v3"]}
hl_de = {5: C["dt"], 9: C["gnd"]}
for k, y in enumerate(RK):
    for x in (XI_E, XI_I, XD_I, XD_E):
        hole(x, y, square=(k == 9 and x in (XI_E, XD_E)))
    chip(XI_E - 32, y, IZQ_EXT[k], hl_ie.get(k))
    chip(XI_I + 32, y, IZQ_INT[k], hl_ii.get(k))
    chip(XD_I - 26, y, DER_INT[k], hl_di.get(k), w=26)
    chip(XD_E + 32, y, DER_EXT[k], hl_de.get(k))

# ================================================================ alimentación de la máquina
a('<rect x="300" y="362" width="200" height="44" rx="8" fill="#ececec" stroke="#1f1f1f" stroke-width="1.5"/>')
text(312, 380, "Masa: mismo punto que", size=12, weight="bold")
text(312, 397, "la E-ECU (B9/B10 o perno)", size=10.5, fill="#444")
wire([(500, 384), (627, 384)], C["gnd"])
a('<rect x="300" y="430" width="200" height="50" rx="8" fill="#fde8e8" stroke="#d62828" stroke-width="1.5"/>')
text(312, 450, "+24 V tras la llave", size=13, weight="bold", fill="#9b1c1c")
text(312, 468, "JB7/JB8 o caja de fusibles", size=10.5, fill="#7a2a2a")
wire([(500, 456), (528, 456)], C["24v"])
a('<rect x="528" y="445" width="50" height="22" rx="5" fill="#f4d03f" stroke="#7a6000" stroke-width="1.5"/>')
a('<line x1="534" y1="456" x2="572" y2="456" stroke="#7a6000" stroke-width="2"/>')
text(553, 438, "fusible 3 A", size=11, anchor="middle", weight="bold")
wire([(578, 456), (627, 456)], C["24v"])

# ================================================================ programador USB-C (izquierda)
a('<rect x="40" y="412" width="210" height="160" rx="10" fill="#1c1c1c" stroke="#000" stroke-width="2"/>')
a('<rect x="26" y="470" width="28" height="46" rx="8" fill="#c0c0c0" stroke="#777"/>')
a('<rect x="80" y="470" width="38" height="38" rx="3" fill="#333" stroke="#555"/>')
text(99, 522, "CH9102", size=9, fill="#aaaaaa", anchor="middle")
text(145, 404, "Programador USB-C (COM5)", size=13, anchor="middle", weight="bold")
prog = [("5V", 422), ("3.3V", 438), ("RXD", 470), ("TXD", 490), ("EN", 510), ("G0", 530), ("GND", 550)]
for n, y in prog:
    pad(250, y, "#9a9a9a" if n in ("5V", "3.3V", "EN", "G0") else "#d8b25a")
    text(238, y + 4, n, size=11, fill="#ffffff", anchor="end", weight="bold")
for y in (422, 438):
    a(f'<line x1="258" y1="{y - 5}" x2="268" y2="{y + 5}" stroke="#d62828" stroke-width="2.5"/>')
    a(f'<line x1="258" y1="{y + 5}" x2="268" y2="{y - 5}" stroke="#d62828" stroke-width="2.5"/>')
text(145, 592, "solo para grabar · 3.3V y 5V: no conectar", size=11, fill="#555", anchor="middle")
text(145, 607, "EN y G0 sin conectar: grabar con el botón IO0", size=11, fill="#777", anchor="middle")
# P4 → programador: solo GND y TX/RX cruzados (EN e IO0 sin cablear; se usa el botón IO0)
wire([(1205, 537), (1205, 492), (300, 492), (300, 470), (255, 470)], C["ptx"])   # TX → RXD
wire([(1175, 537), (1175, 504), (290, 504), (290, 490), (255, 490)], C["prx"])   # RX → TXD
wire([(1145, 537), (1145, 516), (265, 516), (265, 550), (255, 550)], C["gnd"])   # GND → GND

# ================================================================ Adafruit CAN Pal (girado 90°: pines a la derecha)
a('<rect x="380" y="640" width="180" height="180" rx="12" fill="#1a1a1a" stroke="#000" stroke-width="2"/>')
for hx, hy in [(398, 658), (398, 802)]:
    a(f'<circle cx="{hx}" cy="{hy}" r="8" fill="#ffffff" stroke="#c8a35a" stroke-width="3"/>')
a('<rect x="420" y="712" width="46" height="56" rx="3" fill="#2b2b2b" stroke="#555"/>')
text(443, 782, "TJA1051T/3", size=9, fill="#c9d1e0", anchor="middle")
# Interruptor Termination (arriba, en OFF)
a('<rect x="412" y="664" width="60" height="18" rx="3" fill="#e6e6e6" stroke="#333"/>')
a('<rect x="446" y="666" width="23" height="14" rx="2" fill="#d4a017"/>')
text(418, 694, "ON", size=9, fill="#aaaaaa")
text(450, 694, "OFF", size=9, fill="#7cff9e", weight="bold")
text(442, 658, "Termination", size=9, fill="#ffffff", anchor="middle")
# Pines (derecha): CANL, CANH, SLNT, TX, RX, GND, Vcc
canp = [("CANL", 680), ("CANH", 696), ("SLNT", 712), ("TX", 728), ("RX", 744), ("GND", 760), ("Vcc", 776)]
for n, y in canp:
    col = {"GND": "#1f1f1f", "Vcc": C["3v3"]}.get(n, "#d8b25a")
    pad(560, y, col)
    lab = n
    text(550, y + 4, lab, size=9.5, fill="#ffffff", anchor="end")
# Bornero (izquierda): H arriba, GND, L abajo
a('<rect x="352" y="672" width="30" height="116" rx="3" fill="#2fa84f" stroke="#145c2a"/>')
for n, y in [("H", 690), ("G", 730), ("L", 770)]:
    screw(367, y, 10)
    text(392, y + 4, n, size=11, fill="#ffffff", weight="bold")
text(470, 838, "Adafruit CAN Pal (girado 90°)", size=13, anchor="middle", weight="bold")
text(470, 854, "Termination: OFF en la máquina", size=11, fill="#2a9d4f", anchor="middle", weight="bold")


# ---------------------------------------------------------------- alimentación de los módulos
def junction(x, y, color):
    a(f'<circle cx="{x}" cy="{y}" r="5" fill="{color}" stroke="#fff" stroke-width="1.5"/>')
# CAN Pal y OLED: GND → GND (IO… fila exterior, rango 6); Vcc → 3V3 (fila interior, rango 0)
wire([(565, 760), (578, 760), (578, 841), (876, 841)], C["gnd"])
wire([(565, 895), (850, 895), (850, 841)], C["gnd"])
junction(850, 841, C["gnd"])
wire([(565, 776), (586, 776), (586, 560), (956, 560), (956, 576)], C["3v3"])
wire([(565, 911), (586, 911), (586, 776)], C["3v3"])
junction(586, 776, C["3v3"])
# Encoder: GND → GND (tira derecha, rango 0); + → 3V3 (tira derecha, rango 9)
wire([(1495, 700), (1480, 700), (1480, 561), (1340, 561), (1340, 576)], C["gnd"])
wire([(1495, 716), (1488, 716), (1488, 992), (1340, 992), (1340, 977)], C["3v3"])

# CAN Pal → tira izquierda
wire([(565, 712), (875, 712)], C["slnt"])                                   # SLNT → IO4
wire([(565, 728), (612, 728), (612, 755), (875, 755)], C["tx"])            # TX → IO17
wire([(565, 744), (594, 744), (594, 798), (875, 798)], C["rx"])            # RX → IO18

# ================================================================ OLED (girada 90°: pines a la derecha)
a('<rect x="352" y="878" width="208" height="110" rx="8" fill="#1d3557" stroke="#0d1b2a" stroke-width="2"/>')
a('<rect x="364" y="890" width="136" height="86" rx="3" fill="#050a14" stroke="#5c6b80"/>')
text(372, 906, "AUTO-RALENTI", size=10, fill="#7fdcff")
text(372, 944, "1900", size=28, fill="#7fdcff", weight="bold")
text(456, 944, "rpm", size=10, fill="#7fdcff")
text(372, 968, "82C B4:ON CAN", size=10, fill="#7fdcff")
oled = [("GND", 895), ("VCC", 911), ("SCL", 927), ("SDA", 943)]
for n, y in oled:
    col = {"GND": "#1f1f1f", "VCC": C["3v3"]}.get(n, "#d8b25a")
    pad(560, y, col)
    text(550, y + 4, n, size=9.5, fill="#ffffff", anchor="end")
text(456, 1004, "OLED SSD1306 0,96\" I²C (0x3C)", size=13, anchor="middle", weight="bold")
wire([(565, 927), (875, 927)], C["scl"])                                    # SCL → IO22
wire([(565, 943), (600, 943), (600, 948.5), (939.5, 948.5), (939.5, 884), (949, 884)], C["sda"])  # SDA → IO21

# ================================================================ conector B de la E-ECU (abajo a la izquierda)
CBX, CBY = 24, 1060
a(f'<rect x="{CBX + 150}" y="{CBY - 16}" width="90" height="18" rx="4" fill="#8c1d1d" stroke="#5a0f0f"/>')
a(f'<rect x="{CBX}" y="{CBY}" width="390" height="170" rx="14" fill="#b32424" stroke="#5a0f0f" stroke-width="3"/>')
a(f'<rect x="{CBX + 14}" y="{CBY + 24}" width="362" height="122" rx="6" fill="#2a2a2a" stroke="#111"/>')
CX = [CBX + 36 + 29 * i for i in range(12)]
RY = [CBY + 48, CBY + 86, CBY + 124]
special = {1: ("canh", "1"), 2: ("canl", "2"), 4: ("b4", "4"), 9: ("gnd", "9"), 10: ("gnd", "10")}
for r, y in enumerate(RY):
    for i, x in enumerate(CX):
        n = r * 12 + i + 1
        if n in special:
            col, lab = special[n]
            a(f'<rect x="{x - 10}" y="{y - 10}" width="20" height="20" rx="3" fill="{C[col]}" stroke="#fff" stroke-width="1.5"/>')
            text(x, y + 4, lab, size=11, fill="#ffffff", anchor="middle", weight="bold")
        else:
            a(f'<rect x="{x - 7}" y="{y - 7}" width="14" height="14" rx="2" fill="#555" stroke="#777"/>')
for lab, y in [("1", RY[0]), ("13", RY[1]), ("25", RY[2])]:
    text(CBX + 20, y + 4, lab, size=9, fill="#ffffff", anchor="end")
text(CBX + 195, CBY + 162, "B1 CAN H · B2 CAN L · B4 emergencia · B9/B10 masa", size=11, fill="#ffffff", anchor="middle", weight="bold")
text(CBX, CBY + 192, "Conector B de la E-ECU (rojo, lado máquina) — vista de frente", size=13, weight="bold")
text(CBX, CBY + 210, "Filas: 1–12 arriba, 13–24 centro, 25–36 abajo (comprobar números moldeados).", size=10.5, fill="#555")
text(CBX, CBY + 226, "B4 ya está cableado al terminal 3 del interruptor 26: no se toca.", size=10.5, fill=C["b4"])
# GND del CAN Pal (borne G) → B10: referencia de masa común con la E-ECU
wire([(357, 730), (335.5, 730), (335.5, RY[0]), (CX[9] + 10, RY[0])], C["gnd"])
# H → B1, L → B2 (par trenzado)
wire([(357, 690), (300, 690), (300, 1022), (CX[0] - 14, 1022), (CX[0] - 14, RY[0]), (CX[0] - 10, RY[0])], C["canh"])
wire([(357, 770), (320, 770), (320, 1032), (CX[1] - 14.5, 1032), (CX[1] - 14.5, RY[0]), (CX[1] - 10, RY[0])], C["canl"])
for y in range(800, 1000, 26):
    a(f'<path d="M 296 {y} C 310 {y + 6}, 310 {y + 6}, 324 {y + 12}" stroke="#555" stroke-width="1.2" fill="none"/>')
text(292, 900, "par trenzado", size=11, fill="#444", anchor="end")
text(292, 914, "< 1 m", size=11, fill="#444", anchor="end")

# ================================================================ interruptor de emergencia 26 (derecha, junto al relé)
a('<rect x="1500" y="272" width="90" height="290" rx="10" fill="#3a3a3a" stroke="#111" stroke-width="2"/>')
text(1545, 420, "26", size=22, fill="#dddddd", anchor="middle", weight="bold")
TABS = [300 + 45 * i for i in range(6)]
for i, y in enumerate(TABS):
    n = i + 1
    stroke = {2: C["24v"], 3: C["b4"]}.get(n, "#7a6000")
    sw = 3 if n in (2, 3) else 1.2
    a(f'<rect x="1478" y="{y - 12}" width="28" height="24" rx="2" fill="#e0b24a" stroke="{stroke}" stroke-width="{sw}"/>')
    text(1492, y + 4, str(n), size=11, fill="#3a2a00", anchor="middle", weight="bold")
text(1606, 290, "Interruptor de régimen", size=13, weight="bold")
text(1606, 307, "de emergencia (26), en RALENTÍ", size=13, weight="bold")
text(1606, 345, "2: +24 V de F24 (cable original)", size=11.5, fill="#444")
text(1606, 390, "3: hacia B4 de la E-ECU (cable original)", size=11.5, fill="#444")
text(1606, 420, "El relé va en paralelo con el contacto 2–3:", size=11.5, fill="#444")
text(1606, 436, "excitado = 1900 rpm; en reposo manda el interruptor.", size=11.5, fill="#444")
wire([(1371, 383), (1440, 383), (1440, 345), (1478, 345)], C["24v"])   # COM ← 2
wire([(1371, 456), (1458, 456), (1458, 390), (1478, 390)], C["b4"])    # NO → 3

# ================================================================ encoder (derecha; girado: pines a la izquierda)
a('<rect x="1500" y="680" width="220" height="190" rx="8" fill="#14532d" stroke="#0b2e19" stroke-width="2"/>')
a('<circle cx="1640" cy="775" r="52" fill="#3a3a3a" stroke="#1a1a1a" stroke-width="2"/>')
a('<circle cx="1640" cy="775" r="38" fill="#9a9a9a" stroke="#555" stroke-width="2"/>')
for i in range(12):
    ang = i * math.pi / 6
    a(f'<line x1="{1640 + 30 * math.cos(ang):.1f}" y1="{775 + 30 * math.sin(ang):.1f}" '
      f'x2="{1640 + 37 * math.cos(ang):.1f}" y2="{775 + 37 * math.sin(ang):.1f}" stroke="#666" stroke-width="2"/>')
a('<rect x="1635" y="749" width="10" height="26" rx="2" fill="#555"/>')
enc = [("GND", 700), ("+", 716), ("SW", 733.5), ("DT", 750), ("CLK", 766)]
for n, y in enc:
    col = {"GND": "#1f1f1f", "+": C["3v3"]}.get(n, "#d8b25a")
    pad(1500, y, col)
    text(1510, y + 4, n, size=9.5, fill="#ffffff")
text(1610, 672, "Encoder rotativo (KY-040)", size=13, anchor="middle", weight="bold")
text(1610, 888, "pulsación larga = REPOSO", size=11, fill="#14532d", anchor="middle", weight="bold")
wire([(1495, 733.5), (1356.5, 733.5), (1356.5, 755), (1347, 755)], C["sw"])            # SW → IO27
wire([(1495, 750), (1440, 750), (1440, 798), (1420, 798)], C["dt"])                     # DT → IO33
wire([(1495, 766), (1465, 766), (1465, 819.5), (1356.5, 819.5), (1356.5, 841), (1347, 841)], C["clk"])  # CLK → IO32

# ================================================================ notas
nx, ny = 460, 1072
a(f'<rect x="{nx}" y="{ny}" width="1520" height="208" rx="8" fill="#fffbea" stroke="#e0c46c"/>')
text(nx + 14, ny + 22, "Notas", size=13, weight="bold")
notas = [
    "1. Placa vista por delante (relé arriba, antena abajo). Cada pin lleva su número de GPIO (en la serigrafía: G17 = IO17; TX0 = IO1, RX0 = IO3, SVP = IO36, SVN = IO39; IO6–IO11 son de la flash: no usar).",
    "2. Las serigrafías están por detrás: cada fila de la tira tiene dos taladros y dos rótulos; comprobar con el multímetro (continuidad a GND / 3V3) qué taladro es cada pin antes de soldar.",
    "3. Alimentación de los módulos (3,3 V) desde la placa: cables naranja a 3V3 y negros a GND. Donde se cruzan, el cable de señal pasa por encima (no hay contacto).",
    "4. Los módulos están girados para simplificar el cableado; el orden de sus pines es el real, leído en el sentido del dibujo. Guiarse siempre por sus rótulos.",
    "5. CAN Pal: Termination en OFF en la máquina (ON solo en el banco con el USB-CAN). SLNT → IO4: el firmware lo deja en alto (silencio por hardware) salvo en el entorno TSC1.",
    "6. Cable de 3 hilos < 1 m: H → B1, L → B2 (trenzados) y GND del CAN Pal → B10 (o B9). La masa de la placa, en el mismo punto. Interruptor 26 en RALENTÍ y selector en MANUAL.",
    "7. Programador solo para grabar, 3 cables: GND y TX/RX cruzados (EN y G0 sin conectar). Mantener pulsado el botón IO0 al dar tensión. No conectar sus 3.3V/5V.",
    "8. Optoacoplador opcional (IO35 / IO39) y dial original (IO34) no dibujados: ver MONTAJE.md §3.",
]
for i, t in enumerate(notas):
    text(nx + 14, ny + 44 + i * 20, t, size=11.5, fill="#3a3a3a")

a("</g>")
a("</svg>")
with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("ok", len(out))
