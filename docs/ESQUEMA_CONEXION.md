# Esquema de conexión — Regulador para Volvo EC210B (ESP32 / Arduino Nano)

Esquema gráfico: [`esquema_conexion_ESP32.svg`](esquema_conexion_ESP32.svg) · [`esquema_conexion_ESP32.png`](esquema_conexion_ESP32.png)

> **Documento del diseño original (Fases 1–2, parte hidráulica, aplazadas).** Los puntos de conexión en la máquina (§1) siguen siendo válidos. Para el **control de rpm actual** con la placa ESP32_Relay X1, el CAN Pal y el firmware v0.1, usar [`MONTAJE.md`](MONTAJE.md), [`CONTROL_RPM.md`](CONTROL_RPM.md) y el diagrama [`esquema_montaje_ESP32.png`](esquema_montaje_ESP32.png); las tablas de pines de ESP32 DevKit / Arduino Nano de este documento no se corresponden con esa placa.

Cubre la **Fase 1** (driver de corriente de la válvula power shift con vuelta automática a la Resistor Box) y deja preparado el **bus J1939** para las Fases 2 y 3. La placa recomendada es el **ESP32 DevKit V1**, porque trae controlador CAN. El Arduino Nano sirve para la Fase 1 y, con un módulo MCP2515, también para el CAN.

> Fiabilidad: todos los pines de la E-ECU (conector B) y de la V-ECU (JA/JB) de esta tabla proceden del **boletín OEM Volvo "UPDATE EC160B~460B"**, páginas "EECU Electric Circuit" y **"Control Circuit (EC160B~EC460B)"** (`docs/esquemas/ce_EC-B_UPDATE_p06_control_circuit_300dpi.png` y recortes `…_zoom_*.png`). Es documentación oficial, pero del año 2004: en una máquina de 2002 **medir siempre antes de conectar**.

---

## 1. Puntos de conexión en la máquina

| Señal | Dónde | Pin | Color de cable (según L120E, mismo E-ECU) | Fiab. |
|---|---|---|---|---|
| +24 V hacia la V-ECU | Mazo V-ECU, conector JB | **JB7 / JB8** (unidos, desde fusibles F13/F25) | — | confirmado (boletín) |
| Masa de la V-ECU | Mazo V-ECU, conector JA | **JA15 / JA63** (GND) · JA14 (GND del dial) | — | confirmado (boletín) |
| "VECU operating power" | Mazo V-ECU, conector JB | **JB15 / JB16** → van al **selector Auto/Manual**, **no son masa** (ver §1.1) | — | confirmado (boletín) |
| Llave: START (R2) / ON (ACC) | Mazo V-ECU, conector JB | JB2 / JB9 | — | confirmado |
| CAN H | E-ECU conector B (rojo) | **B1** | amarillo (Y) | confirmado |
| CAN L | E-ECU conector B (rojo) | **B2** | verde (GN) | confirmado |
| CAN, par 1 (hacia panel) | Mazo V-ECU, conector JB | **JB14 = H, JB6 = L** | — | confirmado (boletín) |
| CAN, par 2 (desde E-ECU) | Mazo V-ECU, conector JB | **JB13 = H, JB5 = L** | — | confirmado (boletín) |
| CAN en el panel | Panel I-ECU 21C | 21C1 = H, 21C2 = L | — | confirmado |
| J1587 A / B | Mazo V-ECU JB · E-ECU B | **JB12 = A, JB4 = B** · B25 = A, B26 = B | gris / naranja (E-ECU) | confirmado |
| Interruptor de emergencia (estado alta/baja) | E-ECU conector B | **B4** ← terminal 3 del interruptor ← F24 | — | confirmado |
| Alimentación E-ECU (referencia de masa) | E-ECU conector B | B11/B12 (+ vía relé R3 "EMS power", F15 20 A), B9/B10 (−) | rojo-blanco / negro-blanco | confirmado |
| Válvula power shift (+) | Terminal **3** del selector Auto/Manual, unido a **JA32** "Power shift Signal" | — | — | confirmado |
| Válvula power shift (−) | Terminal **5** del selector | — | — | confirmado |
| Salida low-side de la V-ECU a la válvula | **JA5** "P/Shift Ground" → terminal 4 | — | — | confirmado |
| Resistor Box (≈60 Ω) | Terminal **6** del selector → Resistor Box → masa | — | — | confirmado |
| Dial de régimen | V-ECU | **JB11 (+24 V)**, **JA39 (señal 0,5–4,5 V)**, **JA14 (GND)** | — | confirmado |
| Salida "VECU STATUS" al panel | V-ECU | JA34 → 21C9 del panel | — | confirmado |

### 1.1 Cómo está cableado el selector Auto/Manual (6 terminales)

| Terminal | Conectado a | AUTO | MANU |
|---|---|---|---|
| 1 | JB15 (V-ECU) | 1–2 cerrado | abierto |
| 2 | JB16 (V-ECU) y señal "A/M SW position" al panel | | 2–3 cerrado |
| 3 | Válvula (+) y JA32 "Power shift Signal" | abierto | |
| 4 | JA5 "P/Shift Ground" (low-side de la V-ECU) | 4–5 cerrado | abierto |
| 5 | Válvula (−) | | 5–6 cerrado |
| 6 | Resistor Box → masa | abierto | |

- **AUTO**: la V-ECU alimenta la válvula por JA32 (+) y regula la corriente por **JA5 (lado de masa, PWM)**. Nuestro driver copia exactamente esa topología (MOSFET en lado de masa).
- **MANU**: la válvula recibe +24 V por el nodo JB16/terminal 2 y retorna por **terminal 6 → Resistor Box → masa** (≈340 mA). **Nuestro driver se intercala entre el terminal 6 y masa**, con la Resistor Box en el contacto NC del relé.
- **Para emular la V-ECU en AUTO** más adelante: el emulador debe dar +24 V en JA32 y hacer el PWM low-side en JA5, además de poner 24 V en JB16 (si se confirma que JB16 es salida) y leer JB15.

### 1.2 Aviso importante sobre el bus CAN

La V-ECU recibe el bus en **dos pares** (JB13/JB5 desde la E-ECU y JB14/JB6 hacia el panel): actúa como **nodo de paso**. Con la V-ECU desenchufada, es probable que la E-ECU y el panel queden **separados** y que cada tramo tenga una sola terminación (120 Ω). Antes de conectar el ESP32:

1. Medir CAN H–L en el conector JB con la V-ECU desenchufada: si da ≈120 Ω en cada par, hay que **puentear JB13↔JB14 y JB5↔JB6** en el adaptador (o conectar el ESP32 a los dos pares) para que vuelva a medir ≈60 Ω.
2. La máquina del proyecto (2002) tiene MDU en vez de I-ECU; comprobar si el MDU lleva terminación.

**Pin B4** (dato de los camiones Volvo con la misma centralita): entrada de tensión "idle validation": **< 4 V = ralentí (800 rpm), > 8 V = régimen alto (1900 rpm)**. En la excavadora la alimenta el interruptor de emergencia a través del fusible F24. Es una entrada de dos estados, no analógica.

**Terminación del bus:** las dos resistencias de 120 Ω están **dentro de la E-ECU y del panel** (R702 en el I-ECU según el esquema L120E). El ESP32 **no debe añadir** terminación. Con la V-ECU desconectada, la medida entre CAN H y CAN L (máquina apagada) debe seguir dando ≈60 Ω.

---

## 1.3 Versión MODULAR (recomendada): solo módulos premontados

Esquema: [`esquema_modular_ESP32.svg`](esquema_modular_ESP32.svg) · [`.png`](esquema_modular_ESP32.png). Sustituye el driver discreto (MOSFET + shunt + relé con transistor) por módulos comerciales que se cablean con bornes:

| Módulo | Función | Conexiones |
|---|---|---|
| **M1** Convertidor DC-DC 24 → 5 V (Traco THN 10-4811WIR, 18–75 V, aislado; alternativa Mean Well DDR-15G-5 + TVS) | Alimenta el ESP32 y los módulos de 5 V | +Vin ← 24 V (fusible 3 A) · −Vin ← masa · +Vout → VIN ESP32 · −Vout → GND común |
| **M2** Amplificador de válvula proporcional (24 V, entrada 0–10 V, Imín/Imáx y dither ajustables) | Regula la corriente de la válvula en lazo cerrado, con dither y rampa; incluye el diodo de libre circulación | +24 V · GND · IN ← M3 · SOL+ → válvula (+) *(solo si se alimenta la válvula desde el amplificador; en modo Manual el + ya llega del selector, entonces SOL+ no se usa)* · SOL− → M4 → M5 NO |
| **M3** DAC I²C 0–10 V (DFRobot GP8403) o módulo PWM → 0–10 V | Convierte la consigna del ESP32 en 0–10 V | SDA/SCL · 5 V · OUT0 → IN de M2 |
| **M4** Módulo INA226 (shunt 0,1 Ω integrado, hasta 0,8 A) | Supervisa que la corriente real coincide con la consigna | En serie con SOL− · SDA/SCL · 3,3 V |
| **M5** Módulo relé 1 canal NO/NC, optoacoplado, disparo a nivel alto, compatible 3,3 V | Seguridad: sin excitar conecta la Resistor Box de fábrica | COM ← terminal 6 (retorno válvula) · NC → Resistor Box · NO → SOL− · IN ← GPIO26 · 5 V · GND |
| **M6** Módulo CAN SN65HVD230 (o TJA1051T/3) **sin la resistencia de 120 Ω** | Bus J1939 | CANH ← B1 / JB14 · CANL ← B2 / JB6 · TX ← GPIO5 · RX → GPIO4 · 3,3 V |
| **M7** Módulo optoacoplador 24 V → 3,3 V (2–4 canales) | Lee el estado del interruptor de emergencia (B4) y del selector Auto/Manual (terminal 2) | IN1 ← B4 · IN2 ← terminal 2 · OUT1 → GPIO35 · OUT2 → GPIO39 · VCC 3,3 V |
| **M8** ESP32 DevKit V1 sobre **placa de expansión con bornes de tornillo** | Lógica, consignas, supervisión, watchdog | Ver tabla de pines §2 |
| **M9** Encoder KY-040 + OLED SSD1306 | Interfaz | GPIO32/33/27 · SDA/SCL · 3,3 V |

**Ajuste del amplificador M2:** Imín = 200 mA, Imáx = 650 mA, dither 100–150 Hz, rampa 0,5–1 s. Con esos límites la consigna del ESP32 se calcula como *V = 10 · (I − 200) / 450*: 215 mA ≈ 0,3 V · 250 mA ≈ 1,1 V · 290 mA ≈ 2,0 V · 340 mA ≈ 3,1 V · 450 mA ≈ 5,6 V · 555 mA ≈ 7,9 V. Se calibra con la lectura del M4.

**Cableado de la válvula en modo Manual:** la válvula sigue recibiendo su +24 V por el selector (terminal 2–3). El amplificador M2 solo conmuta el lado de masa: SOL− del M2 **no** se conecta a la válvula directamente, sino que el retorno de la válvula (terminal 6) entra en COM del relé M5; NC va a la Resistor Box y NO va, a través del M4, a SOL− del M2. Si el amplificador elegido exige controlar los dos hilos de la bobina (SOL+ y SOL−), hay que llevar el + de la válvula a SOL+ y dejar el terminal 3 del selector sin conectar; en ese caso el relé debe conmutar también el +. Se decidirá al ver la hoja del amplificador comprado.

## 2. Tabla de pines — ESP32 DevKit V1

| Función | GPIO | Notas |
|---|---|---|
| Alimentación 5 V | VIN | Desde el DC-DC 24→5 V |
| Masa | GND | Masa común con el chasis |
| 3,3 V (salida del regulador de la placa) | 3V3 | Alimenta transceptor CAN, INA226, OLED, encoder (< 150 mA en total) |
| CAN TX | **GPIO5** | → pin D (TXD) del SN65HVD230 |
| CAN RX | **GPIO4** | ← pin R (RXD) del SN65HVD230 |
| PWM válvula | **GPIO25** | → puerta Q1 a través de R1 100 Ω; R2 10 kΩ a masa |
| Relé de seguridad | **GPIO26** | → base Q2 a través de R4 1 kΩ |
| I²C SDA | GPIO21 | INA226 + OLED, pull-ups 4,7 kΩ a 3,3 V |
| I²C SCL | GPIO22 | ídem |
| Encoder A (CLK) | GPIO32 | pull-up interno, 100 nF a masa |
| Encoder B (DT) | GPIO33 | ídem |
| Encoder pulsador (SW) | GPIO27 | ídem |
| LED de estado | GPIO2 | LED azul de la placa |
| ADC dial original (opcional) | GPIO34 | 0,5–4,5 V → divisor 10 k/10 k → 0,25–2,25 V |
| ADC estado Manual/alta (opcional) | GPIO35 | línea de B4 (24 V) → divisor 100 k/10 k + Zener 3,3 V |
| ADC selector Auto/Manual (opcional) | GPIO39 | 24 V → mismo divisor |
| ADC corriente (alternativa analógica) | GPIO36 | si se usa INA180A2 en lugar del INA226 |

- No usar GPIO6–11 (flash interna). GPIO34, 35, 36 y 39 son solo entrada y no tienen pull-up.
- Configuración TWAI: 250 kbit/s, modo `LISTEN_ONLY` hasta validar el bus; `NORMAL` solo para la Fase 3.

## 3. Tabla de pines — alternativa Arduino Nano (ATmega328P, 5 V)

| Función | Pin Nano | Notas |
|---|---|---|
| Alimentación 5 V | 5V | Desde el DC-DC. No usar VIN con 24 V: el regulador de la placa no lo aguanta |
| Masa | GND | Masa común |
| PWM válvula | **D9** | Timer1 configurado a ≈1 kHz (Fast PWM, ICR1); D9 va a R1 100 Ω → puerta Q1 |
| Relé de seguridad | **D7** | → R4 1 kΩ → base Q2 |
| Encoder A / B / SW | D2 / D3 / D4 | D2 y D3 admiten interrupciones |
| I²C SDA / SCL | A4 / A5 | INA226 + OLED (ambos funcionan a 5 V) |
| ADC dial original | A0 | 0,5–4,5 V directo (ADC de 5 V) |
| ADC estado Manual/alta | A1 | 24 V → divisor 100 k/22 k (≈4,3 V) + Zener 5,1 V |
| MCP2515 CS | D10 | módulo MCP2515 + TJA1050 (5 V), **cristal 8 MHz → `MCP_8MHZ`** |
| MCP2515 MOSI / MISO / SCK | D11 / D12 / D13 | SPI |
| MCP2515 INT | D2 *(conflicto con encoder: mover encoder A a D5)* | o sondear sin interrupción |
| LED estado | D13 | compartido con SCK si se usa MCP2515; usar otro LED en D6 |

- El Nano tiene 2 kB de RAM: suficiente para la Fase 1 y para escuchar CAN, justo para una pila J1939 completa.
- Hay que **quitar la resistencia de 120 Ω** del módulo MCP2515 (jumper J1 o resistor marcado "120").

---

## 4. Lista de materiales (BOM) — Fase 1 + CAN

| Ref. | Componente | Valor / referencia | Cant. | Notas |
|---|---|---|---|---|
| U1 | Microcontrolador | ESP32 DevKit V1 (30 pines) | 1 | o Arduino Nano + MCP2515 |
| U2 | Transceptor CAN 3,3 V | SN65HVD230 (módulo) o TJA1051T/3 | 1 | sin terminación |
| U3 | Medidor de corriente I²C | INA226 (módulo) | 1 | shunt externo |
| U4 | Pantalla | OLED 0,96" SSD1306 I²C | 1 | |
| U5 | **Convertidor DC-DC comercial 24 → 5 V**, aislado, entrada ancha | **Traco THN 10-4811WIR** (18–75 V, 5 V / 2 A, aguanta 100 V durante 1 s, EN 50155) | 1 | Incluye protección contra polaridad inversa, transitorios y cortocircuito. Alternativas: Traco TEN 5-4811WI (1 A); Mean Well DDR-15G-5 (9–36 V, carril DIN) **añadiendo un TVS SMCJ33A** en la entrada |
| F1 | Fusible | 3 A, portafusibles en línea | 1 | único componente externo al módulo |
| C2 | Condensador | 220 µF/10 V en la salida de 5 V | 1 | opcional, cerca del ESP32 |
| Q1 | MOSFET nivel lógico | IRLZ44N o IRLB8721 (≥55 V) | 1 | disipador pequeño |
| R1, R2 | Puerta Q1 | 100 Ω · 10 kΩ | 1+1 | |
| D1 | Diodo libre circulación | MBR5100 / SB5100 (100 V, 5 A) | 1 | cátodo al +24 V de la bobina |
| R3 | Shunt | 0,1 Ω, 2 W, 1 % | 1 | 0,6 A → 60 mV |
| K1 | Relé | 24 V automoción, 5 pines (30/87/87a/85/86), 20 A | 1 | con zócalo |
| Q2 | Transistor driver relé | BC337 / 2N2222 o 2N7002 | 1 | |
| R4 | Base Q2 | 1 kΩ | 1 | |
| D2 | Diodo bobina relé | 1N4007 | 1 | |
| ENC1 | Encoder rotativo | KY-040 con pulsador | 1 | + 3 × 100 nF |
| R5, R6 | Pull-ups I²C | 4,7 kΩ | 2 | |
| R7–R10 | Divisores entradas | 10 k, 10 k, 100 k, 10 k | — | opcionales |
| Z1 | Zener | 3,3 V, 0,5 W | 1–2 | protección entradas |
| — | Caja | IP65 con prensaestopas, ≈150×100×70 mm | 1 | |
| — | Cable | 1 mm² (válvula), 0,5 mm² (señales), par trenzado (CAN) | — | |
| — | Conectores | según identificación de los conectores de la máquina (investigación en curso) | — | |

Para pruebas en banco: resistencia de carga **18 Ω / 25 W** y fuente de 24 V ≥ 2 A.

---

## 5. Secuencia de montaje y puesta en marcha

1. **Banco**: montar alimentación + ESP32 + driver con la resistencia de 18 Ω. Comprobar con polímetro en serie que 215 / 340 / 555 mA coinciden con la consigna (±10 mA). Ajustar Kp/Ki.
2. **Relé de seguridad**: cortar la alimentación del ESP32 y verificar que K1 cae a 87a (resistor box) en < 50 ms.
3. **En la máquina, apagada**: identificar y medir los cables de la válvula y de la Resistor Box; medir ≈17,5 Ω (bobina) y ≈60 Ω (caja). Medir CAN H–L ≈60 Ω.
4. Conectar el driver intercalado entre el retorno de la válvula y la Resistor Box. Conectar CAN **solo en escucha**.
5. Arrancar en **Manual + emergencia alta**. Con el encoder en el modo "EMERG" (340 mA) el comportamiento debe ser el de fábrica. Pasar a G (290) y H (250) sin carga, luego con carga, vigilando las rpm en la pantalla.
6. Fase 2: si el EEC1 llega por CAN (rpm en pantalla), activar el anti-calado.
7. Fase 3: solo después de capturar el bus y con la V-ECU desconectada.
