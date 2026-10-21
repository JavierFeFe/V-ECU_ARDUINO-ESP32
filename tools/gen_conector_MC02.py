"""Genera docs/conector_MC02.svg: cara de contactos del conector redondo del mazo de la E-ECU.

Dibujado a partir de docs/fotos/conector_MC02_frontal.jpg (vista de frente, escuadra amarilla arriba).
Numeración propia: la cavidad exterior vacía es la referencia (E1) y se cuenta en sentido horario.

Uso:
    python tools/gen_conector_MC02.py docs/conector_MC02.svg
    chrome --headless=new --hide-scrollbars --window-size=1500,960 --screenshot=docs/conector_MC02.png docs/conector_MC02.svg
"""
import math
import sys

W, H = 1500, 960
out = []
a = out.append

# Ángulos medidos en la foto (0° = arriba, sentido horario). La primera exterior es la vacía (referencia).
EXTERIOR = [(233, False), (278, True), (325, True), (12, True), (56, True), (100, True), (144, True), (190, True)]
INTERIOR = [(260, False), (350, True), (80, True), (170, False)]
# Señales confirmadas con el multímetro (continuidad con la clavija de la E-ECU, 2026-10-21)
# (texto, color, posición de la etiqueta)
SENAL = {7: ('CAN H · B1', '#e5c100', (575, 705)), 8: ('CAN L · B2', '#2ca02c', (250, 705))}
CX, CY = 380, 440


def polar(r, ang):
    t = math.radians(ang)
    return CX + r * math.sin(t), CY - r * math.cos(t)


a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">')
a('<defs><radialGradient id="pin" cx="40%" cy="35%" r="70%"><stop offset="0%" stop-color="#fff"/>'
  '<stop offset="60%" stop-color="#c8c8c8"/><stop offset="100%" stop-color="#7d7d7d"/></radialGradient>'
  '<style>.h{font-weight:bold;font-size:15px;fill:#111}.t{font-size:12.5px;fill:#333}.n{font-size:11.5px;fill:#555}'
  '.box{fill:#fff;stroke:#333;stroke-width:1.5}</style></defs>')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')
a('<text x="30" y="36" font-size="21" font-weight="bold" fill="#111">Conector redondo del mazo de la E-ECU (probable MC02) — cara de contactos</text>')
a('<text x="30" y="58" class="n">Dibujado a partir de docs/fotos/conector_MC02_frontal.jpg. Vista de frente, escuadra amarilla arriba. '
  'Numeración propia: <tspan font-weight="bold">E1 = cavidad exterior vacía</tspan>, sentido horario; I1 = interior más cercana a E1.</text>')

# Escuadra y carcasa
a(f'<rect x="{CX - 330}" y="{CY - 345}" width="660" height="70" rx="8" fill="#e8c200" stroke="#6b5800" stroke-width="2"/>')
a(f'<text x="{CX}" y="{CY - 302}" text-anchor="middle" class="t" font-weight="bold">escuadra amarilla (arriba)</text>')
a(f'<circle cx="{CX}" cy="{CY}" r="265" fill="#151515" stroke="#000" stroke-width="4"/>')
a(f'<circle cx="{CX}" cy="{CY}" r="240" fill="#0a0a0a" stroke="#3a3a3a" stroke-width="3"/>')
a(f'<circle cx="{CX}" cy="{CY}" r="205" fill="#232323" stroke="#444" stroke-width="2"/>')

# Anillo exterior (contactos pequeños)
for i, (ang, montado) in enumerate(EXTERIOR, 1):
    x, y = polar(165, ang)
    ref = i == 1
    a(f'<rect x="{x - 27:.0f}" y="{y - 27:.0f}" width="54" height="54" rx="8" fill="#1b1b1b" '
      f'stroke="{"#ff4d4d" if ref else "#8a8a8a"}" stroke-width="{4 if ref else 2}" transform="rotate({ang} {x:.0f} {y:.0f})"/>')
    if montado:
        a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="url(#pin)" stroke="#333"/>')
    else:
        a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#000" stroke="#555"/>')
    lx, ly = polar(224, ang)
    a(f'<text x="{lx:.0f}" y="{ly + 5:.0f}" text-anchor="middle" font-size="15" font-weight="bold" fill="{"#ff6b6b" if ref else "#ffd54a"}">E{i}</text>')
    if i in SENAL:
        nombre, color, (ex, ey) = SENAL[i]
        a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="17" fill="none" stroke="{color}" stroke-width="5"/>')
        a(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="{color}" stroke-width="3"/>')
        a(f'<rect x="{ex - 58:.0f}" y="{ey - 14:.0f}" width="116" height="26" rx="5" fill="{color}"/>')
        a(f'<text x="{ex:.0f}" y="{ey + 5:.0f}" text-anchor="middle" font-size="14" font-weight="bold" fill="#111">{nombre}</text>')

# Flecha de referencia hacia E1
rx, ry = polar(300, 233)
tx, ty = polar(262, 233)
a(f'<line x1="{rx - 60:.0f}" y1="{ry + 40:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" stroke="#d62828" stroke-width="3"/>')
a(f'<text x="{rx - 64:.0f}" y="{ry + 58:.0f}" text-anchor="middle" font-size="13" font-weight="bold" fill="#d62828">REFERENCIA: E1 vacía</text>')

# Anillo interior (contactos grandes)
for i, (ang, montado) in enumerate(INTERIOR, 1):
    x, y = polar(88, ang)
    a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="30" fill="#0e0e0e" stroke="#777" stroke-width="2"/>')
    if montado:
        a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="17" fill="url(#pin)" stroke="#333"/>'
          f'<line x1="{x - 9:.0f}" y1="{y:.0f}" x2="{x + 9:.0f}" y2="{y:.0f}" stroke="#555" stroke-width="2"/>')
    else:
        a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="17" fill="#c9a227" opacity="0.75"/>')
    lx, ly = polar(88, ang)
    dx, dy = {260: (-44, 5), 350: (0, -40), 80: (44, 5), 170: (0, 48)}[ang]
    a(f'<text x="{lx + dx:.0f}" y="{ly + dy:.0f}" text-anchor="middle" font-size="15" font-weight="bold" fill="#7fd4ff">I{i}</text>')

# Llave central
a(f'<circle cx="{CX}" cy="{CY}" r="34" fill="#d6283a" stroke="#7a0f1b" stroke-width="2.5"/>'
  f'<rect x="{CX - 6}" y="{CY - 24}" width="12" height="48" rx="5" fill="#7a0f1b"/>')

# Leyenda
a(f'<g transform="translate(60,{CY + 285})"><rect x="0" y="0" width="640" height="145" class="box" rx="6"/>')
a('<circle cx="24" cy="26" r="9" fill="url(#pin)" stroke="#333"/><text x="42" y="31" class="t">Contacto pequeño montado (anillo exterior E1–E8): 7 de 8</text>')
a('<circle cx="24" cy="54" r="12" fill="url(#pin)" stroke="#333"/><text x="42" y="59" class="t">Contacto grande montado, punta ranurada (anillo interior I1–I4): 2 de 4</text>')
a('<circle cx="24" cy="84" r="10" fill="#000" stroke="#ff4d4d" stroke-width="2"/><circle cx="345" cy="84" r="10" fill="#c9a227" opacity="0.75"/>'
  '<text x="42" y="89" class="t">E1 vacía (referencia)</text><text x="362" y="89" class="t">Vacías con tapón/junta: I1, I4</text>')
a('<circle cx="24" cy="116" r="11" fill="#d6283a" stroke="#7a0f1b"/><text x="42" y="121" class="t">Centro: llave / tapón rojo con ranura (codificación, sin contacto)</text>')
a('</g>')

X0 = 760
# Lo que muestra la foto
a(f'<g transform="translate({X0},90)"><rect x="0" y="0" width="710" height="250" class="box" rx="6"/>')
a('<text x="14" y="26" class="h">Lo que muestra la foto</text>')
lineas = [
    '• 13 posiciones: centro (llave roja) + anillo interior de 4 contactos grandes + anillo exterior de 8 pequeños.',
    '• Montados: <tspan font-weight="bold">9 contactos</tspan> (E2–E8 pequeños; I2, I3 grandes). Vacías: E1 (referencia), I1, I4.',
    '• Lado del mazo de la E-ECU: contactos macho (pines). La pareja del lado máquina lleva hembras.',
    '• Cada contacto pequeño va en un retén cuadrado; los grandes tienen la punta ranurada.',
    '• Marca y serie <tspan font-weight="bold">sin identificar</tspan> (no se ven marcas en la foto).',
    '• Medido (2026-10-21): <tspan font-weight="bold">E7 = CAN H (B1), E8 = CAN L (B2)</tspan>. B4 (emergencia) y',
    '  B9/B10 (masa) <tspan font-weight="bold">no tienen continuidad con ningún contacto</tspan>: llegan por otro lado.',
    '• El esquema SCH02-1 ponía la emergencia en MC02.1: no se cumple en esta máquina',
    '  (o este conector no es MC02). Los otros 7 contactos siguen sin identificar.',
]
for k, l in enumerate(lineas):
    a(f'<text x="14" y="{54 + k * 21}" class="t">{l}</text>')
a('</g>')

# Tabla para rellenar
a(f'<g transform="translate({X0},360)"><rect x="0" y="0" width="710" height="330" class="box" rx="6"/>')
a('<text x="14" y="26" class="h">Tabla para rellenar con el multímetro (llave quitada, E-ECU desenchufada)</text>')
xs = [14, 140, 240, 380, 500]
for x, t in zip(xs, ['Señal', 'Pin E-ECU', 'MC02 (esquema)', 'Posición aquí', 'Comprobación']):
    a(f'<text x="{x}" y="56" class="t" font-weight="bold">{t}</text>')
a('<line x1="10" y1="64" x2="700" y2="64" stroke="#999"/>')
filas = [
    ('CAN H', 'B1', 'MC02.2', 'E7 ✔', '≈2,5 V con contacto', '#fff6cc'),
    ('CAN L', 'B2', 'MC02.3', 'E8 ✔', 'H–L ≈117 Ω / 60 Ω', '#e3f5e3'),
    ('Emergencia', 'B4', '(MC02.1?)', 'no pasa', 'usar interruptor 26 / JA47', '#e3eefc'),
    ('J1587 A', 'B25', 'MC02.4', 'E__ / I__', '(opcional)', '#fff'),
    ('J1587 B', 'B26', 'MC02.5', 'E__ / I__', '(opcional)', '#fff'),
    ('Masa', 'B9/B10', '—', 'no pasa', 'perno de chasis / batería −', '#fde8e8'),
]
for k, f in enumerate(filas):
    y = 90 + k * 34
    a(f'<rect x="10" y="{y - 20}" width="690" height="30" fill="{f[5]}"/>')
    for x, v in zip(xs, f[:5]):
        a(f'<text x="{x}" y="{y}" class="t">{v}</text>')
a('<text x="14" y="306" class="n">Método: una punta en el pin de la clavija de la E-ECU (cara de contactos, desenchufada) y la otra en cada contacto de este conector.</text>')
a('</g>')

# Conexión del SH-C30A
a(f'<g transform="translate({X0},710)"><rect x="0" y="0" width="710" height="220" class="box" rx="6"/>')
a('<text x="14" y="26" class="h">Conexión del SH-C30A sin cortar cables</text>')
lineas = [
    '• Para la captura: <tspan font-weight="bold">E7 = CAN H, E8 = CAN L</tspan> (confirmados) y masa en un perno de chasis/motor',
    '  junto a la E-ECU o en el negativo de batería (este conector no lleva masa, como indica el esquema).',
    '• Con este conector desenchufado de su pareja se puede medir y escuchar en sus pines macho, pero la E-ECU',
    '  queda separada de la cabina: vale para probar la E-ECU sola, no para capturar con la máquina completa.',
    '• Con la máquina completa (enchufado): back-probe por la parte trasera de la pareja, o un',
    '  <tspan font-weight="bold">adaptador en «Y»</tspan> con un conector macho + hembra de esta misma serie (identificar la marca).',
    '• Alternativa sin depender de este conector: clavija libre de la V-ECU (JB14 / JB6), CAPTURA_CAN.md §3c.',
]
for k, l in enumerate(lineas):
    a(f'<text x="14" y="{54 + k * 22}" class="t">{l}</text>')
a('</g>')
a('</svg>')

with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("ok", len(out))
