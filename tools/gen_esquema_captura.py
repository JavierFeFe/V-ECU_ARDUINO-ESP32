"""Genera docs/esquema_captura_CAN.svg: portátil + SH-C30A + conector B de la E-ECU.

Uso:
    python tools/gen_esquema_captura.py docs/esquema_captura_CAN.svg
    chrome --headless=new --hide-scrollbars --window-size=1800,1100 \\
        --screenshot=docs/esquema_captura_CAN.png docs/esquema_captura_CAN.svg
"""
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
text(30, 36, "Captura del bus J1939 — portátil, adaptador SH-C30A y conector B de la E-ECU", size=22, weight="bold")
text(30, 58, "Solo escucha: el adaptador no transmite ni confirma tramas · ver docs/CAPTURA_CAN.md", size=13, fill="#555")

# ================================================================ portátil
a('<rect x="40" y="110" width="380" height="250" rx="12" fill="#2b2b2b" stroke="#111" stroke-width="2"/>')
a('<rect x="56" y="126" width="348" height="218" rx="4" fill="#0d1117"/>')
term = [
    ("> python tools/captura_can.py capturar", "#c9d1d9"),
    ("    --nombre 03_ralenti --duracion 120", "#c9d1d9"),
    ("Adaptador: candleLight USB to CAN", "#8b949e"),
    ("Modo SOLO ESCUCHA confirmado · 250 kbit/s", "#3fb950"),
    ("Grabando en capturas/..._03_ralenti.log", "#8b949e"),
    ("  42 s ·  4180 tramas · 14 IDs · 802 rpm · 82 °C", "#e3b341"),
    ("interruptor en ALTA        ← nota + Enter", "#79c0ff"),
]
for i, (t, col) in enumerate(term):
    text(66, 150 + i * 26, t, size=12, fill=col, family="Consolas, monospace")
a('<path d="M 20 360 L 440 360 L 470 400 L -10 400 Z" fill="#bdbdbd" stroke="#777" stroke-width="2"/>')
text(230, 388, "Portátil (Windows + Python)", size=13, anchor="middle", weight="bold")
a('<rect x="440" y="366" width="18" height="10" rx="2" fill="#666"/>')

# ================================================================ SH-C30A
a('<rect x="560" y="250" width="230" height="170" rx="10" fill="#1b3a6b" stroke="#0d1f3a" stroke-width="2"/>')
a('<rect x="544" y="300" width="26" height="40" rx="6" fill="#c0c0c0" stroke="#777"/>')
a('<rect x="610" y="270" width="54" height="54" rx="3" fill="#222" stroke="#555"/>')
text(637, 338, "STM32F072", size=9, fill="#c9d1e0", anchor="middle")
interruptor(600, 352, "R120", "OFF")
interruptor(600, 384, "BOOT", "OFF")
a('<rect x="766" y="342" width="34" height="74" rx="3" fill="#2fa84f" stroke="#145c2a" stroke-width="1.5"/>')
for n, y in [("CAN_H", 356), ("CAN_L", 379), ("GND", 402)]:
    screw(783, y, 9)
    text(760, y + 4, n, size=11, fill="#ffffff", anchor="end", weight="bold")
text(675, 242, "DSD TECH SH-C30A (candleLight)", size=14, anchor="middle", weight="bold")
text(675, 440, "comprobar los rótulos del bornero de tu unidad", size=11, fill="#666", anchor="middle")
# USB
wire([(458, 371), (500, 371), (500, 320), (544, 320)], C["usb"], width=6)
text(500, 306, "USB", size=11, fill="#555", anchor="middle", weight="bold")

# ================================================================ E-ECU con conectores B (rojo) y A (negro)
a('<rect x="900" y="110" width="860" height="330" rx="18" fill="#a7a9ac" stroke="#6d6f72" stroke-width="3"/>')
for bx in (930, 1720):
    for by in (130, 410):
        a(f'<circle cx="{bx}" cy="{by}" r="9" fill="#8a8c8f" stroke="#5a5c5e"/>')
text(1330, 140, "E-ECU Volvo 03161983 (LucasVarity) — lado de los conectores", size=14, fill="#2b2b2b", anchor="middle", weight="bold")
# Conector B
BX0, BY0 = 940, 180
a(f'<rect x="{BX0 + 150}" y="{BY0 - 14}" width="90" height="16" rx="4" fill="#8c1d1d"/>')
a(f'<rect x="{BX0}" y="{BY0}" width="380" height="160" rx="12" fill="#b32424" stroke="#5a0f0f" stroke-width="3"/>')
a(f'<rect x="{BX0 + 12}" y="{BY0 + 18}" width="356" height="124" rx="6" fill="#2a2a2a"/>')
CX = [BX0 + 30 + 29 * i for i in range(12)]
RY = [BY0 + 42, BY0 + 80, BY0 + 118]
esp = {1: ("canh", "1"), 2: ("canl", "2"), 9: ("gnd", "9"), 4: ("gris", "4")}
for r, y in enumerate(RY):
    for i, x in enumerate(CX):
        n = r * 12 + i + 1
        if n in esp:
            col, lab = esp[n]
            a(f'<rect x="{x - 10}" y="{y - 10}" width="20" height="20" rx="3" fill="{C[col]}" stroke="#fff" stroke-width="1.5"/>')
            text(x, y + 4, lab, size=10, fill="#fff", anchor="middle", weight="bold")
        else:
            a(f'<rect x="{x - 7}" y="{y - 7}" width="14" height="14" rx="2" fill="#555" stroke="#777"/>')
for lab, y in [("1", RY[0]), ("13", RY[1]), ("25", RY[2])]:
    text(BX0 + 16, y + 4, lab, size=9, fill="#fff", anchor="end")
text(BX0 + 64, BY0 + 178, "Conector B (rojo, lado máquina)", size=13, weight="bold")
text(BX0 + 64, BY0 + 196, "B1 CAN H · B2 CAN L · B9 masa", size=11, fill="#444")
text(BX0 + 64, BY0 + 212, "B4 (gris): no tocar", size=11, fill="#444")
# Conector A (no se usa)
AX0 = 1360
a(f'<rect x="{AX0 + 150}" y="{BY0 - 14}" width="90" height="16" rx="4" fill="#111"/>')
a(f'<rect x="{AX0}" y="{BY0}" width="380" height="160" rx="12" fill="#1c1c1c" stroke="#000" stroke-width="3"/>')
a(f'<rect x="{AX0 + 12}" y="{BY0 + 18}" width="356" height="124" rx="6" fill="#2e2e2e"/>')
for y in RY:
    for i in range(12):
        x = AX0 + 30 + 29 * i
        a(f'<rect x="{x - 7}" y="{y - 7}" width="14" height="14" rx="2" fill="#444" stroke="#5a5a5a"/>')
text(AX0 + 190, BY0 + 178, "Conector A (negro, lado motor): no se toca", size=13, anchor="middle", weight="bold")

# ================================================================ cables y sondas back-probe
def sonda(x, color):
    a(f'<line x1="{x}" y1="{RY[0]}" x2="{x}" y2="356" stroke="#9a9a9a" stroke-width="2"/>')
    a(f'<rect x="{x - 6}" y="356" width="12" height="34" rx="3" fill="{color}" stroke="#333"/>')


# H → B1 (entra por la izquierda de la columna 1), L → B2, GND → B9; por debajo, sin cruces
wire([(792, 356), (870, 356), (870, 400), (CX[0] - 14, 400), (CX[0] - 14, 390)], C["canh"])
wire([(792, 379), (845, 379), (845, 420), (CX[1] - 14.5, 420), (CX[1] - 14.5, 390)], C["canl"])
wire([(792, 402), (820, 402), (820, 440), (CX[8] + 14.5, 440), (CX[8] + 14.5, 390)], C["gnd"])
for x, col in [(CX[0] - 14, C["canh"]), (CX[1] - 14.5, C["canl"]), (CX[8] + 14.5, C["gnd"])]:
    sonda(x, col)
for x, tx in [(CX[0] - 14, CX[0]), (CX[1] - 14.5, CX[1]), (CX[8] + 14.5, CX[8])]:
    a(f'<line x1="{x}" y1="{RY[0]}" x2="{tx - (8 if tx > x else -8)}" y2="{RY[0]}" stroke="#9a9a9a" stroke-width="2"/>')
text(1110, 470, "sondas back-probe por detrás del conector, sin desconectarlo", size=12, fill="#444", anchor="middle")
text(675, 470, "CAN_H → B1 · CAN_L → B2 · GND → B9", size=12, fill="#1b1b1b", anchor="middle", weight="bold")

# ================================================================ medidas con el multímetro
a('<rect x="30" y="510" width="760" height="300" rx="10" fill="#f7f7f7" stroke="#d0d0d0"/>')
text(46, 536, "1 · Antes de capturar: dos medidas con el multímetro en el conector B", size=15, weight="bold")


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
text(190, 602, "Resistencia entre B1 y B2", size=13)
text(190, 628, "≈ 60 Ω → correcto", size=13, fill="#2a9d4f", weight="bold")
text(190, 650, "≈ 120 Ω → bus partido:", size=13, fill="#d62828", weight="bold")
text(190, 670, "puentear JB13↔JB14", size=13, fill="#d62828")
text(190, 690, "y JB5↔JB6 (conector", size=13, fill="#d62828")
text(190, 710, "de la V-ECU)", size=13, fill="#d62828")
multimetro(420, 560, "2.61", "V⎓")
text(560, 580, "Medida 2 — llave en", size=14, weight="bold")
text(560, 598, "CONTACTO, motor parado", size=14, weight="bold")
text(560, 622, "B1 → B9: 2,5–3,5 V", size=13)
text(560, 642, "B2 → B9: 1,5–2,5 V", size=13)
text(560, 666, "(≈ 2,5 V ambas en reposo)", size=12, fill="#555")
text(46, 790, "Punta negra (COM) en B9 para las tensiones. Anotar ambas medidas en el informe.", size=12, fill="#555")

# ================================================================ topología del bus
a('<rect x="810" y="510" width="960" height="300" rx="10" fill="#f7f7f7" stroke="#d0d0d0"/>')
text(826, 536, "2 · Por qué R120 va en OFF: el bus ya tiene sus dos terminaciones", size=15, weight="bold")
YH, YL = 650, 690


def nodo(x, y, w, h, titulo, sub, borde="#333", relleno="#ffffff", dash=None):
    da = f'stroke-dasharray="{dash}"' if dash else ""
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{relleno}" stroke="{borde}" stroke-width="2" {da}/>')
    text(x + w / 2, y + 20, titulo, size=13, anchor="middle", weight="bold")
    if sub:
        text(x + w / 2, y + 38, sub, size=11, fill="#555", anchor="middle")


def resistencia(x):
    a(f'<line x1="{x}" y1="{YH}" x2="{x}" y2="{YL}" stroke="#333" stroke-width="2"/>')
    a(f'<rect x="{x - 7}" y="{YH + 8}" width="14" height="24" rx="2" fill="#fff" stroke="#333" stroke-width="2"/>')
    text(x + 12, YH + 25, "120 Ω", size=11, fill="#333")


# Tramo 1: E-ECU ↔ V-ECU (JB14/JB6); tramo 2: V-ECU (JB13/JB5) ↔ panel
wire([(905, YH), (1180, YH)], C["canh"], halo=False)
wire([(905, YL), (1180, YL)], C["canl"], halo=False)
wire([(1360, YH), (1690, YH)], C["canh"], halo=False)
wire([(1360, YL), (1690, YL)], C["canl"], halo=False)
nodo(830, 560, 150, 60, "E-ECU", "dirección 0x00")
resistencia(905)
a(f'<line x1="905" y1="620" x2="905" y2="{YH}" stroke="#333" stroke-width="2"/>')
nodo(1180, 560, 180, 60, "V-ECU (retirada)", "nodo de paso", borde="#999", relleno="#fafafa", dash="7 5")
for x, lab in [(1180, "JB14/JB6"), (1360, "JB13/JB5")]:
    text(x, YL + 22, lab, size=10, fill="#555", anchor="middle")
a(f'<path d="M 1180 {YH} C 1240 {YH - 30}, 1300 {YH - 30}, 1360 {YH}" fill="none" stroke="{C["canh"]}" stroke-width="2.5" stroke-dasharray="6 5"/>')
a(f'<path d="M 1180 {YL} C 1240 {YL + 30}, 1300 {YL + 30}, 1360 {YL}" fill="none" stroke="{C["canl"]}" stroke-width="2.5" stroke-dasharray="6 5"/>')
text(1270, 740, "puentes solo si B1–B2 ≈ 120 Ω", size=11, fill="#d62828", anchor="middle", weight="bold")
nodo(1600, 560, 150, 60, "Panel I-ECU", "dirección 0x17")
resistencia(1690)
a(f'<line x1="1690" y1="620" x2="1690" y2="{YH}" stroke="#333" stroke-width="2"/>')
# Derivaciones: SH-C30A (ahora) y ESP32 + CAN Pal (después)
a(f'<line x1="1000" y1="{YH}" x2="1000" y2="750" stroke="{C["canh"]}" stroke-width="3"/>')
a(f'<line x1="1012" y1="{YL}" x2="1012" y2="750" stroke="{C["canl"]}" stroke-width="3"/>')
nodo(930, 750, 160, 50, "SH-C30A", "R120 OFF · solo escucha", borde="#1b3a6b")
a(f'<line x1="1480" y1="{YH}" x2="1480" y2="750" stroke="{C["canh"]}" stroke-width="3" stroke-dasharray="6 5"/>')
a(f'<line x1="1492" y1="{YL}" x2="1492" y2="750" stroke="{C["canl"]}" stroke-width="3" stroke-dasharray="6 5"/>')
nodo(1400, 750, 180, 50, "ESP32 + CAN Pal", "más adelante · Termination OFF", borde="#999", dash="7 5")
text(1290, 790, "derivaciones < 1 m, sin resistencia", size=11, fill="#555", anchor="middle")

# ================================================================ seguridad y pasos
a('<rect x="30" y="830" width="1740" height="250" rx="10" fill="#fffbea" stroke="#e0c46c"/>')
text(46, 858, "3 · Seguridad y orden de trabajo", size=15, weight="bold")
izq = [
    "• Máquina estacionada, implementos apoyados, palanca de seguridad BLOQUEADA.",
    "• Selector Auto/Manual en MANUAL. Interruptor 26 en ralentí al empezar.",
    "• Conectar las sondas con la llave QUITADA; después dar contacto.",
    "• SH-C30A: BOOT en OFF (modo trabajo) y R120 en OFF.",
    "• El script se niega a grabar si el adaptador no confirma el modo solo escucha.",
    "• Comprobación previa sin máquina:  capturar --nombre prueba --duracion 5",
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
text(930, 886, "Capturas (python tools/captura_can.py capturar --nombre …):", size=13, weight="bold")
for i, t in enumerate(der):
    text(946, 912 + i * 24, t, size=13, fill="#3a3a3a", family="Consolas, monospace")
text(930, 1064, "Después:  python tools/captura_can.py analizar \"capturas/*.log\" --informe capturas/resumen.md",
     size=13, fill="#1d4ed8", weight="bold")

a("</svg>")
with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("ok", len(out))
