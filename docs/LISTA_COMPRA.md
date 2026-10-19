# Lista de compra — Regulador V-ECU para Volvo EC210B (ESP32)

Todo lo necesario para hacer las mediciones (Fase 0), montar el regulador de la válvula (Fase 1) y dejar preparado el bus CAN (Fases 2 y 3). Los precios son orientativos (IVA incluido, otoño 2026) y las tiendas son las que envían a España; los enlaces concretos están en el [Anexo G](anexos/G_conectores_compra.md). Referencias de pines y esquema: [`ESQUEMA_CONEXION.md`](ESQUEMA_CONEXION.md), [`PINOUT_E-ECU.md`](PINOUT_E-ECU.md).

**Resumen de coste**

| Bloque | Imprescindible | Opcional |
|---|---|---|
| A. Herramientas de medida (Fase 0) | 35–80 € (si no tienes polímetro) | +20–40 € |
| B. Electrónica del regulador (Fase 1) | ≈ 60–80 € | — |
| C. Bus CAN (Fases 2–3) | ≈ 10–15 € | +25–40 € (adaptador USB-CAN) |
| D. Conectores y cableado | ≈ 40–60 € | +150–300 € (pigtails Volvo) |
| E. Alimentación (módulo comercial), protección y caja | ≈ 65–85 € | — |
| F. Banco de pruebas | ≈ 30–45 € | — |
| **Total para empezar (A+B+C+D+E+F sin opcionales)** | **≈ 240–365 €** | |

---

## A. Herramientas de medida (Fase 0) — comprar primero

| # | Artículo | Especificación | Cant. | Dónde | Precio |
|---|---|---|---|---|---|
| A1 | **Multímetro digital** | Escala de corriente continua **≥ 1 A** (mejor 10 A), resistencia con resolución de 0,1 Ω, tensión DC 60 V. Ej.: UNI-T UT139C, Brymen BM235, Fluke 101/115 | 1 | Amazon.es, RS, Leroy Merlin | 35–80 € |
| A2 | Cables de medida con **pinzas de cocodrilo** y puntas finas de aguja (para pinchar en el conector) | juego | 1 | Amazon.es | 8–12 € |
| A3 | *Opcional:* pinza amperimétrica DC (mA) | UNI-T UT210E (mide mA en DC) | 1 | Amazon.es | 30–40 € |
| A4 | *Opcional:* manómetro 0–60 bar con latiguillo y racor para la toma de presión de la válvula | para contrastar la curva mA → presión secundaria del manual | 1 | tienda hidráulica | 20–40 € |

Con A1 y A2 ya puedes hacer todas las mediciones de la Fase 0: bobina (≈17,5 Ω), Resistor Box (≈60 Ω), corriente real en emergencia (≈340 mA), resistencia CAN H–L (≈60 Ω) y tensión en B4.

## B. Electrónica del regulador (Fase 1)

| # | Ref. esquema | Artículo | Especificación | Cant. | Dónde | Precio |
|---|---|---|---|---|---|---|
| B1 | U1 | **ESP32 DevKit V1** (30 pines, chip ESP32-WROOM-32) | con USB; comprar 2 por si acaso | 2 | Amazon.es, AliExpress | 8–12 €/ud |
| B2 | U3 | **Módulo INA226** (medida de corriente I²C) | se usa con shunt externo: **quitar o puentear el shunt de 0,1 Ω del módulo si viene soldado** y conectar IN+/IN− al shunt R3 | 1 | Amazon.es, AliExpress | 4–8 € |
| B3 | R3 | **Resistencia shunt 0,1 Ω, 2–3 W, 1 %** | de película metálica o cerámica | 2 | Mouser, RS, Amazon.es | 1–2 €/ud |
| B4 | Q1 | **MOSFET IRLZ44N** (TO-220, nivel lógico, 55 V, 47 A) | alternativa: IRLB8721 | 3 | Mouser, Amazon.es | 1–2 €/ud |
| B5 | — | Disipador TO-220 pequeño + tornillo + arandela aislante | ≈ 10 K/W | 1 | Amazon.es | 2–3 € |
| B6 | D1 | **Diodo MBR5100** o SB5100 (Schottky 100 V, 5 A) | libre circulación de la válvula | 2 | Mouser, Amazon.es | 0,5–1 €/ud |
| B7 | K1 | **Relé automoción 24 V, 5 pines (30/87/87a/85/86), 20–30 A** con zócalo y cables | contacto conmutado (NC y NA) imprescindible | 1 | Amazon.es, tienda de recambios | 6–10 € |
| B8 | Q2 | Transistor **BC337** (o 2N2222) | driver del relé | 3 | Mouser, Amazon.es | 0,2 €/ud |
| B9 | D2 | Diodo **1N4007** | en paralelo con la bobina del relé | 5 | — | 0,1 €/ud |
| B10 | R1, R2, R4 | Resistencias 100 Ω, 10 kΩ, 1 kΩ (1/4 W) | surtido de resistencias E12 si no tienes | 1 kit | Amazon.es | 8–10 € |
| B11 | R5, R6 | Resistencias 4,7 kΩ (pull-ups I²C) | incluidas en el surtido | 2 | — | — |
| B12 | ENC1 | **Encoder rotativo KY-040** con pulsador y botón de mando | 1–2 | Amazon.es, AliExpress | 2–4 € |
| B13 | U4 | **Pantalla OLED 0,96" SSD1306 I²C** (128×64) | dirección 0x3C | 1 | Amazon.es, AliExpress | 4–6 € |
| B14 | C | Condensadores 100 nF cerámicos (×10), 100 µF/50 V, 220 µF/10 V electrolíticos | surtido | 1 | Amazon.es | 6–8 € |
| B15 | — | Placa de prototipos **perforada** (doble cara, 7×9 cm) o protoboard para las primeras pruebas, cable Dupont, regleta de pines | 1 | Amazon.es | 8–12 € |
| B16 | — | Bornes de tornillo para PCB (5,08 mm) para 24 V, válvula y Resistor Box | 6–8 | Amazon.es | 3–4 € |

## C. Bus CAN J1939 (Fases 2 y 3)

| # | Ref. | Artículo | Especificación | Cant. | Dónde | Precio |
|---|---|---|---|---|---|---|
| C1 | U2 | **Módulo transceptor CAN 3,3 V**: Waveshare **SN65HVD230 CAN Board** (o módulo TJA1051T/3) | **quitar la resistencia de 120 Ω** del módulo (R2 en el Waveshare) | 2 | Waveshare, Tinytronics, Amazon.es | 5–9 €/ud |
| C2 | — | Cable par trenzado apantallado 2×0,5 mm² (CAN) | 2 m | RS, tienda electricidad | 3–5 € |
| C3 | *Opcional pero muy recomendable* | **Adaptador USB-CAN** para el PC: CANable / CANable 2.0 (candleLight, funciona con SavvyCAN y python-can) o PCAN-USB (más caro) | para capturar el bus de tu máquina y de otra EC210B sana | 1 | Amazon.es, AliExpress, canable.io | 25–40 € (CANable) |
| C4 | *Opcional* | Terminación de 120 Ω conmutable para el banco (resistencia 120 Ω 1/4 W + interruptor) | solo para pruebas en banco entre ESP32 y PC; **nunca en la máquina** | 2 | — | 1 € |

## D. Conectores y cableado

| # | Artículo | Especificación | Cant. | Dónde | Precio |
|---|---|---|---|---|---|
| D1 | **Conector de la válvula** (TE Econoseal J Mark II): plug **174352-2** + terminales hembra **173707-1** (×2 + repuestos) + juntas **1-172888-3** (×2 + repuestos) | para hacer un cable en "Y" o un alargador de la válvula sin cortar el mazo | 2 juegos | RS, Farnell, Mouser, Heilind | 3–6 € total |
| D2 | *Para banco:* cap housing **174354-2** + terminales macho **173706-1** (lado válvula) | simula el conector de la válvula en el banco | 1 juego | RS, Farnell | 1–2 € |
| D3 | **Kit conectores Deutsch DT** (2/3/4/6/12 vías, ≈216 piezas, con crimpadora de trinquete para contactos estampados) | entradas/salidas estancas de la caja del regulador | 1 | Amazon.es ("kit Deutsch DT crimpadora") | 35–45 € |
| D4 | **Crimpadora de trinquete** para terminales abiertos 0,5–1,5 mm² (Engineer PA-21, IWISS SN-28B/IWS-2820) | para los terminales Econoseal y faston | 1 | Amazon.es | 25–45 € |
| D5 | Terminales faston 6,3 mm hembra aislados (para el relé y la Resistor Box) + terminales de anillo M6 (masa) | surtido | 1 | Amazon.es | 8–10 € |
| D6 | Cable unipolar automoción FLRY 1 mm² (rojo, negro, marrón) y 0,5 mm² (varios colores) | 5 m de cada | — | tienda de electricidad / Amazon.es | 15–20 € |
| D7 | Tubo termorretráctil con adhesivo (surtido), bridas, funda corrugada ø 10–13 mm | — | 1 kit | Amazon.es | 10–15 € |
| D8 | **Juego de extractores de terminales** (≈76 piezas) | para sacar pines de conectores originales sin dañarlos | 1 | Amazon.es | 15–25 € |
| D9 | *Opcional (Fase 3 / emulación completa):* **pigtail del conector de la V-ECU** (JA 70 + JB 16) "VECU Controller Connector Plug 14518349 14594697" | permite enchufar el regulador en el sitio de la V-ECU sin tocar el mazo | 1 | eBay 384979664114 / 375584859654; Amazon SINOCMP B06W9JF7XT | ≈ 165 US$ + 30 envío |
| D10 | *Opcional:* pigtail de los conectores de la **E-ECU** (par negro + gris, 36 vías) SINOCMP "ECU 60100000 connector plug" | solo si quieres pinchar el CAN en la E-ECU con un adaptador en "Y" en vez de en el mazo de la V-ECU | 1 | sinocmp.com | ≈ 259 US$ |

> Recomendación: **empieza sin D9 ni D10**. Para la Fase 1 basta con intercalar el driver en el cable de la Resistor Box (terminal 6 del selector) con faston/Deutsch, y para el CAN basta con derivar el par en el conector JB del mazo de la V-ECU con pines de prueba. El pigtail de la V-ECU (D9) merece la pena solo cuando se vaya a montar de forma definitiva o a emular la V-ECU completa.

## E. Alimentación, protección y caja

| # | Ref. | Artículo | Especificación | Cant. | Dónde | Precio |
|---|---|---|---|---|---|---|
| E1 | U5 | **Convertidor DC-DC comercial 24 → 5 V, aislado, entrada ancha: Traco TEN 10-4811WIR** (18–75 V → 5 V / 2 A, 10 W, encapsulado, aguanta 100 V/1 s, protección contra polaridad inversa, cortocircuito y sobretensión) | Es la opción "comprar y conectar": no hace falta TVS, diodo ni circuito de protección propio. Alternativas: **Traco TEN 5-4811WI** (1 A, ≈25 €); **Mean Well DDR-15G-5** (carril DIN, 9–36 V, 3 A, ≈20 €) **solo si se le añade un TVS SMCJ33A** en la entrada, porque 36 V no da margen frente a los picos del alternador | 1 | Mouser, RS, TME, Farnell | 35–45 € (TEN 10) |
| E2 | — | *Solo con la alternativa Mean Well:* diodo TVS **SMCJ33A** | en paralelo con la entrada de 24 V del módulo | 2 | Mouser, RS | 0,5–1 €/ud |
| E4 | F1 | **Portafusibles en línea** + fusibles de cuchilla 3 A (×5) | en el cable de +24 V, antes del convertidor | 1 | Amazon.es, recambios | 5–8 € |
| E5 | — | **Caja estanca IP65/IP67** ABS ≈ 200×120×75 mm | con tapa (transparente si quieres ver el OLED) | 1 | Amazon.es, RS (Hammond/Fibox) | 12–20 € |
| E6 | — | Prensaestopas **M16/M20 IP68** (×6) o conector Deutsch DT de brida para la entrada de la caja | | 1 | Amazon.es | 8–10 € |
| E7 | — | Fijaciones: velcro industrial o soportes para la caja, tornillería M4 | | — | — | 5 € |
| E8 | Z1, Z2 | Diodos Zener 3,3 V 0,5 W (protección entradas ADC) y resistencias 100 kΩ / 10 kΩ | | 5 | surtido | — |

## F. Banco de pruebas (antes de tocar la máquina)

| # | Artículo | Especificación | Cant. | Dónde | Precio |
|---|---|---|---|---|---|
| F1 | **Fuente de alimentación 24 V ≥ 2 A** (fuente industrial de carril o de laboratorio) | la de laboratorio con limitación de corriente es la más segura | 1 | Amazon.es | 20–30 € (industrial) · 60–90 € (laboratorio) |
| F2 | **Resistencia de carga 18 Ω / 25–50 W** (aluminio, con disipador) | simula la bobina de la válvula (17,5 Ω) | 2 | Amazon.es, RS | 3–5 €/ud |
| F3 | Resistencia 56–68 Ω / 10 W | simula la Resistor Box | 1 | — | 2 € |
| F4 | Soldador (≥ 40 W, regulable), estaño, flux, tercera mano | si no tienes | 1 | Amazon.es | 25–40 € |
| F5 | Cable USB micro-B (datos) para el ESP32 | | 1 | — | 3 € |

## G. Alternativa Arduino Nano (solo si no usas ESP32)

| # | Artículo | Especificación | Cant. | Precio |
|---|---|---|---|---|
| G1 | Arduino Nano (ATmega328P, CH340) | | 1 | 5–10 € |
| G2 | Módulo **MCP2515 + TJA1050** (CAN, SPI) | comprobar cristal: casi siempre **8 MHz**; quitar la resistencia de 120 Ω (jumper J1) | 1 | 4–7 € |
| G3 | Convertidor de nivel no necesario (todo a 5 V); el INA226 y el OLED funcionan a 5 V | | — | — |

---

## Software (gratuito)

- **PlatformIO** (VS Code) o Arduino IDE 2.x con el core **Arduino-ESP32 3.x**.
- Librerías: `INA226` (Rob Tillaart), `Adafruit SSD1306` + `Adafruit GFX`, `ESP32Encoder` o `AiEsp32RotaryEncoder`; TWAI nativo del ESP-IDF (incluido en el core).
- Para el PC con el adaptador USB-CAN: **SavvyCAN** (gráfico, abre DBC) y **python-can** + **can-j1939**.
- Archivo DBC J1939 genérico para decodificar EEC1/ET1/DM1 (GitHub `J1939-DBC-Database`).

## Orden de compra sugerido

1. **Hoy:** bloque A (medida) + F1/F2 (banco) + B1 (ESP32) + C1 (transceptor) + E1 (convertidor Traco).
2. **Con las mediciones hechas:** resto del bloque B, E y D1–D8.
3. **Cuando la Fase 1 funcione en la máquina:** C3 (USB-CAN) para capturar el bus y, si procede, D9.
