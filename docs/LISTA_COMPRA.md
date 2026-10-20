# Lista de compra — Control de rpm del motor

Alcance actual: **solo la gestión de las rpm del motor**, por CAN J1939 (vía A, TSC1) y por el pin B4 (vía B, relé). Ver [`CONTROL_RPM.md`](CONTROL_RPM.md) y [`MONTAJE.md`](MONTAJE.md). La parte hidráulica (válvula power shift) queda aplazada y **no** está en esta lista. Tampoco las herramientas que ya tenéis (multímetro, cables, soldador).

Productos localizados en **Amazon España**; precios orientativos (IVA incl., octubre 2026, "según buscador": Amazon no deja leer las fichas de forma automática, así que **comprueba precio y disponibilidad al abrir el enlace**). Enlace: `https://www.amazon.es/dp/ASIN`. Informe completo con alternativas en el [Anexo I](anexos/I_productos_amazon_es.md).

## Ya disponible (no comprar)

| Hardware | Sustituye a | Estado |
|---|---|---|
| **Placa ESP32_Relay X1 V1.2** (ESP32-WROOM-32E, relé Songle 10 A, entrada 24 V) | ESP32 DevKit + placa de bornes, módulo relé, convertidor 24 → 5 V (y su TVS) | ✅ Programada y probada: relé en **GPIO16** confirmado ([`HARDWARE_PLACA_ESP32_RELE.md`](HARDWARE_PLACA_ESP32_RELE.md)) |
| **Programador USB-C** con auto-descarga | Adaptador USB-TTL 3,3 V | ✅ Funciona por P4 (COM5) |
| **Encoder rotativo** | Encoder KY-040 | Pendiente de cablear (G32/G33/G27) |

## Resumen de lo que falta

| Bloque | Coste aprox. |
|---|---|
| A. Electrónica (CAN + OLED) | 13–18 € |
| B. Instalación en la máquina | 90–125 € |
| C. Diagnóstico (un adaptador USB-CAN) | 25–35 € |
| **Total** | **≈ 130–180 €** |
| Opcionales (optoacoplador, bornes DIN, fuente de banco…) | +6–120 € |

---

## A. Electrónica

| # | Artículo | Producto en Amazon.es | ASIN | Precio | Cant. | Notas |
|---|---|---|---|---|---|---|
| A3 | ✅ **Elegido: Adafruit CAN Pal (TJA1051T/3, ref. 5708)** | Adafruit CAN Pal TJA1051T/3 5708 | [B0CHT1RP5Y](https://www.amazon.es/dp/B0CHT1RP5Y) | comprobar en la ficha (en [Opencircuit](https://opencircuit.es/producto/adafruit-can-pal-can-bus-transceiver) ≈ 8,50 € + envío) | 1 | **Imprescindible** para leer rpm (EEC1) y para TSC1. **Interruptor de terminación** (2 × 60 Ω): **OFF en la máquina**, ON solo en el banco. Funciona con 3,3 V (bomba de carga interna a 5 V). Pines Vcc / GND / TX / RX / SLNT (hay que soldar la tira) → 3V3 / GND / G17 / G18 / G4; bornero de 3,5 mm con L / GND / H |
| A3b | *Alternativa (hay que desoldar):* **SN65HVD230** | Waveshare SN65HVD230 CAN Board | [B00KM6XMXO](https://www.amazon.es/dp/B00KM6XMXO) | ≈ 6–9 € | 1 | Trae resistencia de 120 Ω soldada (SMD marcada «121», junto a CANH/CANL): **quitarla** y dejar los pads abiertos, nunca puentearlos. No tocar la «103» (10 kΩ). Sin pin de silencio. Otras: Luckfox [B0CNP17MCH](https://www.amazon.es/dp/B0CNP17MCH); pack 3 Hailege [B0B1WW5XHV](https://www.amazon.es/dp/B0B1WW5XHV). Comprar A3 **o** A3b, no los dos |
| A7 | **OLED 0,96" SSD1306 I²C** | AZDelivery 0,96" I²C | [B01L9GC470](https://www.amazon.es/dp/B01L9GC470) | ≈ 7–9 € | 1 | rpm, modo, temperatura y DTC. El firmware funciona sin ella (consola serie). Alternativa ×2 [B07JN2NHT4](https://www.amazon.es/dp/B07JN2NHT4) (comprobar que es SSD1306, no SH1106) |

## B. Instalación en la máquina

| # | Artículo | Producto en Amazon.es | ASIN | Precio | Cant. | Notas |
|---|---|---|---|---|---|---|
| B1 | **Portafusibles en línea ATC** + fusibles | Portafusibles en línea ×5 | [B09HL97VRQ](https://www.amazon.es/dp/B09HL97VRQ) | ≈ 8–10 € | 1 | **3 A** en el +24 V de la placa. Estanco: [B0B59P7TXY](https://www.amazon.es/dp/B0B59P7TXY). Kit de fusibles [B0GP66MPRW](https://www.amazon.es/dp/B0GP66MPRW) |
| B2 | **Caja estanca IP65 ≈ 200×120×75 mm** | Caja ABS IP65 200×120×75 | [B07RQ5TRHK](https://www.amazon.es/dp/B07RQ5TRHK) | ≈ 12–18 € | 1 | Tapa transparente si se quiere ver la OLED sin abrir: [B0848Q8CQS](https://www.amazon.es/dp/B0848Q8CQS) |
| B3 | **Prensaestopas IP68** M16/M20 | Surtido 32 uds | [B07XF88KP9](https://www.amazon.es/dp/B07XF88KP9) | ≈ 10–12 € | 1 | Alimentación, CAN, relé y encoder |
| B4 | **Cable automoción FLRY-B 0,5 mm²**, 5 colores | Juego 5 colores | [B01FHCER9U](https://www.amazon.es/dp/B01FHCER9U) | ≈ 12–15 € | 1 | CAN (trenzar amarillo/verde ≈ 1 vuelta cada 2–3 cm) y línea B4 |
| B5 | **Cable FLRY-B 1 mm²** rojo/negro | FLRY-B 1 mm² | [B078ZTPX2L](https://www.amazon.es/dp/B078ZTPX2L) | ≈ 8–12 € | 1 | Alimentación 24 V y masa |
| B6 | **Termorretráctil 3:1 con adhesivo**, surtido | Surtido adhesivo | [B088QK1BG5](https://www.amazon.es/dp/B088QK1BG5) | ≈ 10–14 € | 1 | |
| B7 | **Funda corrugada abierta 13 mm** | Corrugado abierto | [B00I04AAV2](https://www.amazon.es/dp/B00I04AAV2) | ≈ 1,3 €/m | 5 m | |
| B9 | **Sondas back-probe** | Kit 92 pzas | [B0DJT9HMGK](https://www.amazon.es/dp/B0DJT9HMGK) | ≈ 25–35 € | 1 | Pinchar el interruptor 26 y el CAN (B1/B2 o JB14/JB6) sin cortar cables |

## C. Diagnóstico — adaptador USB-CAN (imprescindible)

Necesario para la **captura del bus** (Fase 1) antes de transmitir nada, y para probar el módulo CAN en el banco.

**Comprar solo uno** de estos tres (son alternativas). Recomendado: **C1**.

| # | Producto | ASIN | Precio | Notas |
|---|---|---|---|---|
| C1 | **CANable Pro aislado (ADM3053)** — recomendado | [B0CP29RZRP](https://www.amazon.es/dp/B0CP29RZRP) | ≈ 25–35 € | Firmware candleLight; SavvyCAN y python-can; aislamiento galvánico |
| C2 | ✅ **Comprado: DSD TECH SH-C30A** (candleLight, interruptor R120) — uso en [`CAPTURA_CAN.md`](CAPTURA_CAN.md) | [B0BQ5G3KLR](https://www.amazon.es/dp/B0BQ5G3KLR) | ≈ 25–30 € | Versión aislada SH-C31G [B0FHHCSZY8](https://www.amazon.es/dp/B0FHHCSZY8) |
| C4 | CANable V2.0 | [B0DP9N6TB8](https://www.amazon.es/dp/B0DP9N6TB8) | ≈ 20–30 € | No aislado |

Debe trabajar a **250 kbit/s**, en **modo escucha** (listen-only) y permitir desactivar su terminación de 120 Ω.

## D. Opcionales

| # | Artículo | Producto | ASIN | Precio | Para qué |
|---|---|---|---|---|---|
| A5 | Módulo optoacoplador PC817 4 canales, entrada 3,6–30 V | Aislamiento 24 V → 3,3 V | [B0B7D15YW5](https://www.amazon.es/dp/B0B7D15YW5) | ≈ 6–9 € | Leer el estado real de B4 y el selector Auto/Manual (firmware: `VECU_OPTO=1`) |
| D6 | **Fuente de laboratorio 30 V / 5 A** | RUZIZAO | [B0C6K4LDV3](https://www.amazon.es/dp/B0C6K4LDV3) | ≈ 40 € | Probar la placa a 24 V y 30 V en el banco ([`MONTAJE.md`](MONTAJE.md) §1.3) |
| D5 | Fuente 24 V carril DIN Mean Well NDR-120-24 | — | [B07BFCCPVB](https://www.amazon.es/dp/B07BFCCPVB) | ≈ 28 € | Alternativa más barata a D6 (sin ajuste) |
| B8 | Bornes de carril DIN | Bornes UK-2.5B | [B07Y7BCRST](https://www.amazon.es/dp/B07Y7BCRST) | ≈ 10–15 € | Ordenar el cableado dentro de la caja |
| B10 | Extractores de terminales | Hossom | [B0C16VB4DG](https://www.amazon.es/dp/B0C16VB4DG) | ≈ 15 € | Sacar pines de conectores originales |

Ya **no** hacen falta (los cubre la placa ESP32_Relay o se aplazan con la parte hidráulica): ESP32 DevKit y placa de bornes, módulo relé, convertidor DC-DC 24 → 5 V y TVS, adaptador USB-TTL, encoder, relé de automoción 24 V, conectores Deutsch y crimpadoras.

## Pedido mínimo

1. **A3** módulo CAN · **C1** USB-CAN · **A7** OLED → con esto se hace la prueba de banco (ESP32 ↔ USB-CAN a 250 kbit/s) y la **captura del bus** de la máquina en solo escucha.
2. **B1, B2, B3, B4, B5, B6, B9** → montaje en la máquina de la vía B (relé sobre B4) y del CAN.

## Software (gratuito)

PlatformIO con Arduino-ESP32 3.x (ya instalado) · librerías `Adafruit SSD1306` / `Adafruit GFX` (las baja PlatformIO) · TWAI nativo (ESP-IDF) · PC: **SavvyCAN**, **python-can**, **can-j1939** · DBC J1939 genérico (GitHub `J1939-DBC-Database`).
