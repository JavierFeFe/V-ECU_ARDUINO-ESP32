# Lista de compra — Control de rpm del motor (ESP32, solo módulos premontados)

Alcance actual: **gestión de las rpm del motor** por CAN J1939 y por el pin B4 ([`CONTROL_RPM.md`](CONTROL_RPM.md), esquema [`esquema_rpm_ESP32.png`](esquema_rpm_ESP32.png)). La parte hidráulica queda aplazada y **no** está en esta lista. Tampoco están las herramientas que ya tenéis (multímetro, cables, soldador).

Productos localizados en **Amazon España**; precios orientativos (IVA incl., octubre 2026, "según buscador": Amazon no deja leer las fichas de forma automática, así que **comprueba precio y disponibilidad al abrir el enlace**). Enlace: `https://www.amazon.es/dp/ASIN`. Informe completo con alternativas en el [Anexo I](anexos/I_productos_amazon_es.md).

> **Ya disponible:**
> - **Placa ESP32-WROOM-32E con relé y entrada 24 V** (LC Technology; ver [`HARDWARE_PLACA_ESP32_RELE.md`](HARDWARE_PLACA_ESP32_RELE.md)) → sobran **A1/A2** (ESP32 + bornes), **A4** (relé) y **A8** (convertidor).
> - **Encoder rotativo** → sobra **A6**.
>
> Núcleo pendiente de comprar: módulo CAN (A3), **adaptador USB-TTL 3,3 V (A10)** —el micro-USB de la placa es solo de alimentación—, OLED (A7) y optoacoplador (A5, opcional): ≈ 25–35 €.

## Resumen

| Bloque | Coste aprox. |
|---|---|
| A. Núcleo electrónico (ESP32, bornes, CAN, relé, opto, encoder, OLED, DC-DC) | 100–140 € |
| B. Instalación (fusible, caja, prensaestopas, cable, bornes, termorretráctil, back-probe) | 90–130 € |
| C. Diagnóstico (adaptador USB-CAN) | 25–35 € |
| **Total para empezar** | **≈ 215–305 €** |
| Opcionales (Deutsch DT + crimpadora, fuente 24 V de banco) | +70–175 € |

---

## A. Núcleo electrónico

| # | Artículo | Producto en Amazon.es | ASIN | Precio | Cant. | Notas |
|---|---|---|---|---|---|---|
| A1 | **ESP32 DevKit V1 (30 pines) + placa de bornes** | Pack 2 × ESP32 DevKit 30 pines **con 2 placas de expansión de bornes** | [B0D7MGPBD1](https://www.amazon.es/dp/B0D7MGPBD1) | ≈ 20–25 € | 1 pack | Resuelve A1 y A2 de una vez. Alternativa: diymore 3 × ESP32 30 pines [B0BY8J6VVM](https://www.amazon.es/dp/B0BY8J6VVM) |
| A2 | Placa de expansión con bornes para ESP32 de 30 pines (si no se compra el pack) | Breakout ESP32 30 pines bornes | [B0CLCQBX24](https://www.amazon.es/dp/B0CLCQBX24) · [B0CN3YHJYF](https://www.amazon.es/dp/B0CN3YHJYF) | ≈ 8–12 € | 1 | **Ojo:** las placas AZDelivery son de **38 pines**; si se compran, breakout de 38 pines [B0CG8ZW8X5](https://www.amazon.es/dp/B0CG8ZW8X5) |
| A3 | **Módulo transceptor CAN 3,3 V** | Waveshare SN65HVD230 CAN Board | [B00KM6XMXO](https://www.amazon.es/dp/B00KM6XMXO) | ≈ 6–9 € | 2 | 4,7★. **Trae resistencia de 120 Ω soldada: quitarla** (R2). Alternativas: Luckfox [B0CNP17MCH](https://www.amazon.es/dp/B0CNP17MCH); pack 3 Hailege [B0B1WW5XHV](https://www.amazon.es/dp/B0B1WW5XHV) |
| A4 | **Módulo relé 1 canal, optoacoplado, disparo a nivel ALTO, 3 V/3,3 V** (NO/NC, 10 A / 30 VDC) | AYWHP ×6 | [B0DQL4SVN6](https://www.amazon.es/dp/B0DQL4SVN6) | ≈ 8–10 € (6 uds) | 1 pack | Alimentar la bobina (≈120 mA) desde el 3,3 V del ESP32 o desde 5 V según versión, **nunca desde un GPIO**. Alternativa ARCELI ×5 [B0CLTZFWY4](https://www.amazon.es/dp/B0CLTZFWY4). Los módulos "de 24 V" no se disparan con 3,3 V: evitar |
| A5 | **Módulo optoacoplador PC817, 4 canales, entrada 3,6–30 V** | Módulo aislamiento 4 ch 24 V → 3,3/5 V | [B0B7D15YW5](https://www.amazon.es/dp/B0B7D15YW5) | ≈ 6–9 € | 1 | Lee B4 y la posición del selector. Alternativas [B07M78S8LB](https://www.amazon.es/dp/B07M78S8LB), [B07Y8LNQ4M](https://www.amazon.es/dp/B07Y8LNQ4M) (3,3 V ↔ 24 V tipo PLC) |
| A6 | ~~**Encoder rotativo KY-040** con botón~~ **(ya disponible)** | WayinTop ×5 | [B07T3672VK](https://www.amazon.es/dp/B07T3672VK) | ≈ 7–9 € | 1 pack | Con pomo: [B06XQTHDRR](https://www.amazon.es/dp/B06XQTHDRR) |
| A7 | **OLED 0,96" SSD1306 I²C** | AZDelivery 0,96" I²C | [B01L9GC470](https://www.amazon.es/dp/B01L9GC470) | ≈ 7–9 € | 1 | Alternativa ×2 [B07JN2NHT4](https://www.amazon.es/dp/B07JN2NHT4) (comprobar que es SSD1306) |
| A8 | **Convertidor DC-DC 24 → 5 V** | **Opción recomendada en Amazon:** módulo sellado automoción **8–58 V → 5 V 3 A** | [B07WSWMNN8](https://www.amazon.es/dp/B07WSWMNN8) | ≈ 12–16 € | 1 | Entrada hasta 58 V: margen frente a los picos del alternador sin añadir nada. Alternativa carril DIN Mean Well **DDR-15G-5** [B07B6553JY](https://www.amazon.es/dp/B07B6553JY) (≈ 20 €) **pero** su máximo es 36 V: añadir el TVS A9 y el fusible. Industrial fuera de Amazon: **Traco THN 10-4811WIR** (18–75 V, aislado) en RS España ≈ 37 € |
| A9 | TVS SMCJ33A (solo con la Mean Well) | Pack 40 uds | [B0D1QHP3N8](https://www.amazon.es/dp/B0D1QHP3N8) | ≈ 8 € | 1 | O Littelfuse en RS/Farnell (≈ 0,55 €/ud) |
| A10 | **Adaptador USB-TTL a 3,3 V** (programar la placa ESP32 con relé: su micro-USB es solo de alimentación) | **AZDelivery CP2102 HW-598** (3,3 V / 5 V, con cables) | [B082FMFHNP](https://www.amazon.es/dp/B082FMFHNP) | ≈ 8 € | 1 | Alternativas: AZDelivery **FT232RL** con jumper 3,3/5 V [B082FMKG5C](https://www.amazon.es/dp/B082FMKG5C) (≈ 8 €; **mover el jumper a 3,3 V**, viene en 5 V); SATKIT CP2102 con fusible [B06Y42DX3C](https://www.amazon.es/dp/B06Y42DX3C) (≈ 5 €); CH340G AZDelivery [B08T24NML9](https://www.amazon.es/dp/B08T24NML9) (≈ 10 €). Conectar solo **GND, TX→RX, RX→TX** a P4; la placa se alimenta por su micro-USB o su borne, **no** desde el adaptador |

## B. Instalación

| # | Artículo | Producto en Amazon.es | ASIN | Precio | Cant. | Notas |
|---|---|---|---|---|---|---|
| B1 | **Portafusibles en línea ATC** + fusibles | Portafusibles en línea ×5 | [B09HL97VRQ](https://www.amazon.es/dp/B09HL97VRQ) | ≈ 8–10 € | 1 | Estanco: [B0B59P7TXY](https://www.amazon.es/dp/B0B59P7TXY). Kit de fusibles 2–35 A [B0GP66MPRW](https://www.amazon.es/dp/B0GP66MPRW); usar **3 A** |
| B2 | **Caja estanca IP65 ≈ 200×120×75 mm** | Caja ABS IP65 200×120×75 | [B07RQ5TRHK](https://www.amazon.es/dp/B07RQ5TRHK) | ≈ 12–18 € | 1 | Con bisagra, carril DIN y prensaestopas incluidos: [B0BRTMJXW4](https://www.amazon.es/dp/B0BRTMJXW4). Tapa transparente (más grande, 276×150×87): [B0848Q8CQS](https://www.amazon.es/dp/B0848Q8CQS) |
| B3 | **Prensaestopas IP68** M16/M20 | Surtido 32 uds | [B07XF88KP9](https://www.amazon.es/dp/B07XF88KP9) | ≈ 10–12 € | 1 | M16 ×20: [B0CNGD4TT8](https://www.amazon.es/dp/B0CNGD4TT8) |
| B4 | **Cable automoción FLRY-B 0,5 mm²**, 5 colores | Juego 5 colores | [B01FHCER9U](https://www.amazon.es/dp/B01FHCER9U) | ≈ 12–15 € | 1 | Señales, CAN (trenzar a mano amarillo/verde ≈ 1 vuelta cada 2–3 cm) |
| B5 | **Cable FLRY-B 1 mm²** rojo/negro | FLRY-B 1 mm² | [B078ZTPX2L](https://www.amazon.es/dp/B078ZTPX2L) | ≈ 8–12 € | 1 | Alimentación 24 V y masa |
| B6 | **Termorretráctil 3:1 con adhesivo**, surtido | Surtido adhesivo | [B088QK1BG5](https://www.amazon.es/dp/B088QK1BG5) | ≈ 10–14 € | 1 | Alternativa [B0B48C59G7](https://www.amazon.es/dp/B0B48C59G7) |
| B7 | **Funda corrugada abierta 13 mm** | Corrugado abierto | [B00I04AAV2](https://www.amazon.es/dp/B00I04AAV2) | ≈ 1,3 €/m | 5 m | Alternativa Kalitec NW10 [B08M6FDVRN](https://www.amazon.es/dp/B08M6FDVRN) |
| B8 | **Bornes de carril DIN** (UK-2.5 o push-in) | Bornes UK-2.5B | [B07Y7BCRST](https://www.amazon.es/dp/B07Y7BCRST) | ≈ 10–15 € | 1 lote | Push-in: [B0BF9VCML2](https://www.amazon.es/dp/B0BF9VCML2); dobles [B0BJZ8SQFX](https://www.amazon.es/dp/B0BJZ8SQFX) |
| B9 | **Sondas back-probe** (pinchar conectores sin dañarlos) | Kit 92 pzas | [B0DJT9HMGK](https://www.amazon.es/dp/B0DJT9HMGK) | ≈ 25–35 € | 1 | Agujas 2 mm [B0G4LD1FM8](https://www.amazon.es/dp/B0G4LD1FM8); perforadoras [B0CR484WL4](https://www.amazon.es/dp/B0CR484WL4) |
| B10 | Extractores de terminales (76 pzas) | Hossom | [B0C16VB4DG](https://www.amazon.es/dp/B0C16VB4DG) | ≈ 15 € | 1 | Para sacar pines de conectores originales |
| B11 | *Opcional:* relé automoción 24 V 5 pines con base (si se prefiere un relé "de máquina" en la línea B4, gobernado por el módulo A4) | Aiqeer ×3 | [B0CKYHZLTS](https://www.amazon.es/dp/B0CKYHZLTS) | ≈ 12–15 € | 1 | Alternativa Partuto [B0DB2FRNMH](https://www.amazon.es/dp/B0DB2FRNMH) |

## C. Diagnóstico — adaptador USB-CAN (imprescindible)

| # | Producto | ASIN | Precio | Notas |
|---|---|---|---|---|
| C1 | **CANable Pro aislado (ADM3053)** — recomendado | [B0CP29RZRP](https://www.amazon.es/dp/B0CP29RZRP) | ≈ 25–35 € | Firmware candleLight; funciona con SavvyCAN y python-can; aislamiento galvánico |
| C2 | DSD TECH SH-C30A | [B0BQ5G3KLR](https://www.amazon.es/dp/B0BQ5G3KLR) | ≈ 25–30 € | Versiones SH-C30L [B0G387Y3J9](https://www.amazon.es/dp/B0G387Y3J9) y aislada SH-C31G [B0FHHCSZY8](https://www.amazon.es/dp/B0FHHCSZY8) |
| C3 | Innomaker USB2CAN (aislado 3000 V, modo silencioso) | [B0956NV6CM](https://www.amazon.es/dp/B0956NV6CM) | ≈ 33–80 € | Cable USB2CAN-C [B09K3LL93Q](https://www.amazon.es/dp/B09K3LL93Q); doble canal X2 [B09FLQM7QH](https://www.amazon.es/dp/B09FLQM7QH) |
| C4 | CANable V2.0 | [B0DP9N6TB8](https://www.amazon.es/dp/B0DP9N6TB8) | ≈ 20–30 € | No aislado |
| — | PEAK PCAN-USB | — | — | En Amazon solo clones "compatibles" a ≈ 237 €: **no recomendado**; el original se compra fuera de Amazon |

Todos deben trabajar a **250 kbit/s** y en **modo escucha** (listen-only/silent) para la primera captura. Comprobar que el adaptador permite desactivar su terminación de 120 Ω.

## D. Opcionales

| # | Artículo | Producto | ASIN | Precio |
|---|---|---|---|---|
| D1 | Kit conectores **Deutsch DT** con crimpadora | JRready | [B0D942SYV3](https://www.amazon.es/dp/B0D942SYV3) · [B0D2KB2RP6](https://www.amazon.es/dp/B0D2KB2RP6) | 40–70 € |
| D2 | Kit Deutsch DT 188 pzas IWISS | IWISS | [B098SZZX8Z](https://www.amazon.es/dp/B098SZZX8Z) | ≈ 40 € |
| D3 | **Crimpadora de trinquete** terminales abiertos | Engineer PA-21 | [B002L6HJ8W](https://www.amazon.es/dp/B002L6HJ8W) | ≈ 43 € |
| D4 | Crimpadora económica SN-28B | — | [B01A0SAQ3W](https://www.amazon.es/dp/B01A0SAQ3W) | ≈ 20 € |
| D5 | **Fuente 24 V para banco**: Mean Well NDR-120-24 (carril DIN) | — | [B07BFCCPVB](https://www.amazon.es/dp/B07BFCCPVB) | ≈ 28 € |
| D6 | Fuente de laboratorio 30 V / 5 A con limitación de corriente | RUZIZAO | [B0C6K4LDV3](https://www.amazon.es/dp/B0C6K4LDV3) | ≈ 40 € |

## Pedido mínimo para empezar esta semana

1. **A1** pack ESP32 + bornes · **A3** módulo CAN (×2) · **A8** convertidor 24→5 V · **C1** USB-CAN aislado · **B9** back-probe · **B1** portafusibles.
2. Con eso se hace la **captura del bus** de la máquina y las primeras pruebas de lectura (EEC1, rpm) en el banco con una fuente de 24 V.
3. El resto (relé, opto, encoder, OLED, caja, cable) para el montaje definitivo de la vía B y de la interfaz.

## Software (gratuito)

PlatformIO o Arduino IDE 2.x con Arduino-ESP32 3.x · librerías `Adafruit SSD1306` / `Adafruit GFX`, `ESP32Encoder` · TWAI nativo (ESP-IDF) · PC: **SavvyCAN**, **python-can**, **can-j1939** · DBC J1939 genérico (GitHub `J1939-DBC-Database`).
