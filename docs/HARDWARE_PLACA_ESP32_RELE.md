# Placa disponible: ESP32-WROOM-32E con relé (LC Technology, 2022-04-22)

![Placa ESP32 con relé](fotos/placa_ESP32_rele_LC_frontal.jpg)

## Qué se ve en la placa

| Elemento | Identificación (por la foto) | Para el proyecto |
|---|---|---|
| Módulo | **ESP32-WROOM-32E** (Espressif) | Tiene controlador CAN (TWAI) interno: solo hace falta el transceptor externo |
| Relé | **Songle SRD-05VDC-SL-C**, 10 A / 30 VDC, contactos **COM / NO / NC** en borne de 3 tornillos, mandado por transistor S8050 ("J3Y") | Sirve tal cual para la **vía B**: poner 24 V en la línea B4 (corriente de mA) |
| Alimentación | Borne de 2 tornillos **+ / −**, convertidor conmutado con bobina 470 µH, diodo SS210 y circuito integrado en SOIC-8 (**XL7005A**, a confirmar en la serigrafía: entrada 5–80 V, 0,4 A) + regulador 3,3 V (AMS1117, U3) | Se alimenta **directamente a 24 V** de la máquina. Si el chip es el XL7005A, aguanta 80 V: margen sobrado frente a los picos del alternador |
| USB micro | Sin chip USB-serie visible (no hay CH340/CP2102) | Probablemente **solo alimentación**: para programar hace falta un **adaptador USB-TTL de 3,3 V** en el conector P4 |
| P4 | Conector de 6 pines con un puente | Cabecera de programación/consola (GND, TX, RX, 5 V/3,3 V, IO0, EN, según modelo). Comprobar la serigrafía del reverso |
| Botón | **IO0** | Entrar en modo de carga de firmware: mantener pulsado al dar tensión |
| Filas de pines | Dos filas de **taladros sin soldar** a ambos lados del módulo | Hay que soldar tiras de pines para sacar los GPIO (CAN, I²C, encoder, optoacoplador) |
| Fecha / marca | 2022-04-22, logotipo LC | Familia "LC Technology ESP32 relay X1" |

## ¿Sirve para el proyecto? Sí

Cubre de golpe tres módulos de la lista de compra: el **ESP32**, el **convertidor 24 → 5 V** y el **relé** de la vía B. Solo hay que añadir:

1. **Módulo transceptor CAN 3,3 V** (SN65HVD230, sin su resistencia de 120 Ω) en dos GPIO libres (p. ej. GPIO5 TX / GPIO4 RX).
2. **Módulo optoacoplador 24 V → 3,3 V** para leer el estado real de B4 y del selector (opcional).
3. **Encoder y OLED** en los GPIO de las filas laterales.
4. **Adaptador USB-TTL 3,3 V** (CP2102 o CH340) para cargar el firmware por P4, si el micro-USB resulta ser solo de alimentación.

Cableado de la vía B con esta placa: **COM ← terminal 2 del interruptor de emergencia (+24 V de F24)**, **NO → terminal 3 (línea B4)**. Relé en reposo = manda el interruptor original; relé excitado = 24 V en B4 = 1900 rpm. El borne + / − de alimentación va a +24 V tras la llave (con fusible de 3 A en línea) y a masa de la máquina.

## Comprobaciones antes de usarla

| # | Qué comprobar | Cómo | Por qué |
|---|---|---|---|
| 1 | Referencia exacta del chip del convertidor (SOIC-8 junto al borne de alimentación) | Leer la serigrafía con lupa | Si es **XL7005A** → entrada hasta 80 V, perfecto. Si fuera otro (p. ej. MP1584/LM2596) el máximo podría ser 28–40 V y haría falta protección |
| 2 | Tensión de entrada admitida | Probar en banco con fuente de laboratorio a 24 V y luego 30 V; medir 5 V y 3,3 V | Confirmar que trabaja con los 27–28 V del alternador |
| 3 | GPIO que gobierna el relé y la salida del LED | Seguir la pista del transistor J3Y hasta el módulo, o cargar un sketch que active pines uno a uno | En las placas LC de 1 relé suele ser **GPIO16**, pero hay variantes |
| 4 | Lógica del relé | Medir con el multímetro COM–NO al poner el GPIO en alto | Para que "sin excitar" = contacto NC (interruptor original manda) |
| 5 | Función del micro-USB y pines de P4 | Mirar el reverso de la placa (serigrafía) y medir continuidad con el módulo | Saber si se programa por USB o por USB-TTL |
| 6 | GPIO libres en las filas laterales | Serigrafía del reverso | Reservar GPIO5/4 (CAN), 21/22 (I²C), 32/33/27 (encoder), 35/39 (opto). Evitar GPIO6–11 |
| 7 | Capacidad del convertidor (0,4 A si es XL7005A) | Medir la tensión de 5 V con WiFi activo | El WiFi del ESP32 tiene picos de ≈0,4 A; si cae la tensión, desactivar WiFi en la instalación o alimentar los módulos externos desde una fuente aparte |

## Programación

- Si P4 lleva RX/TX: adaptador USB-TTL a **3,3 V** (GND–GND, TX↔RX cruzados), mantener **IO0** pulsado al dar alimentación (o puentear IO0 a GND con el jumper si está previsto), cargar con PlatformIO/Arduino IDE a 115200 baud, soltar IO0 y reiniciar.
- Placa en PlatformIO: `board = esp32dev`. Reservar en `config.h` el GPIO del relé que resulte de la comprobación 3.

## Fotos de la máquina guardadas en el repositorio

- `fotos/E-ECU_etiquetas_superior.jpg` — etiquetas de programación (VCE56003584 / D6D EAE2, EC210 010828).
- `fotos/E-ECU_placa_LucasVarity_03161983.jpg` — placa del fabricante (LucasVarity, 03161983 P03).
- `fotos/E-ECU_conectores_36pines.jpg` — los dos conectores de 36 pines.

---

# Otro módulo disponible: driver L298N (doble puente H, MW-095 / HW-095)

![Módulo L298N](fotos/modulo_L298N.jpg)

**Qué es:** doble puente en H L298N (hasta 46 V y 2 A por canal), con 8 diodos de libre circulación (M7), regulador 78M05 con jumper "12 V EN" y condensadores de 220 µF / 35 V. Pensado para motores DC y paso a paso.

**Para el alcance actual (rpm): no hace falta.** La vía B (24 V en B4) la resuelve el relé de la placa ESP32, que da aislamiento galvánico; la vía A es solo CAN.

**Para la fase hidráulica aplazada: sí puede servir** como etapa de potencia de la válvula power shift (≈17,5 Ω, 200–650 mA), en lugar del MOSFET discreto o del amplificador comercial:

- Una salida (OUT1) con PWM en ENA desde el ESP32; caída de ≈2 V en el L298N, sin problema (650 mA × 17,5 Ω ≈ 11,4 V).
- Lleva diodos de libre circulación; el dither se hace por software.
- **Hace falta medir la corriente** (INA226 o la resistencia de "sense" del L298N) para regular en lazo cerrado: el módulo no la regula por sí mismo.
- **Quitar el jumper "12 V EN"** y alimentar la lógica a 5 V aparte: el 78M05 y los condensadores de 35 V quedan muy justos con los 28 V del alternador y sus picos.
- Implica cambiar el cableado de la válvula: el L298N tiene que alimentarla él (OUT1 → válvula + / válvula − → GND o OUT2), por lo que el + que llega del selector en modo Manual debe quedar desconectado de la válvula mientras el L298N la controle, y el relé de seguridad tiene que devolver **ambos** hilos a la configuración de fábrica.

Se deja anotado para retomarlo con la parte hidráulica.
