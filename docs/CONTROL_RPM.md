# Control de rpm del motor — alcance actual del proyecto

> Decisión (2026-10-19): **se aplaza la parte hidráulica** (regulación de la válvula power shift). El objetivo inmediato es **gestionar las rpm del motor D6D** desde un ESP32, usando solo módulos premontados. Esquema: [`esquema_rpm_ESP32.svg`](esquema_rpm_ESP32.svg) · [`.png`](esquema_rpm_ESP32.png).

## 1. Cómo se puede mandar el régimen a esta E-ECU

La E-ECU Volvo 03161983 (LucasVarity, familia EECU D12) solo tiene **dos entradas de régimen**:

| Vía | Qué es | Resolución | Estado |
|---|---|---|---|
| **A. CAN J1939 — petición de régimen** | Lo que hace la V-ECU en modo Auto: "Engine speed (request value)" por el bus de control. Candidato: **TSC1 (PGN 0)** desde la dirección de la V-ECU (0x11), cada 10 ms, modo "speed control", 0,125 rpm/bit. | Continua (800–2000 rpm) | **Probable, no confirmado** en esta E-ECU. Volvo Penta y Deutz EMR2 (misma generación) lo aceptan; falta saber si esta exige además otros mensajes de la V-ECU (llave, estado) o si ignora TSC1 mientras B4 está activo. |
| **B. Pin B4 "Emergency speed control"** | Entrada de dos estados alimentada por F24 a través del interruptor de emergencia 26: **< 4 V = ralentí (800 rpm), > 8 V = alto (1900 rpm)**; los dos valores se ajustan con VCADS Pro. | Dos escalones | **Confirmado** (circuito OEM EC160B–290B y manual Vectro II). |

No hay entrada analógica de acelerador ni PWM: la vía A es la única que da régimen continuo.

## 2. Hardware (solo módulos)

> **Hardware real disponible:** la placa **ESP32_Relay X1 V1.2** (ESP32-WROOM-32E + relé + entrada 24 V) cubre M1, M3 y M5; el encoder y el programador USB-C también están disponibles. Pinout, asignación de GPIO y cableado completos en [`HARDWARE_PLACA_ESP32_RELE.md`](HARDWARE_PLACA_ESP32_RELE.md) y [`MONTAJE.md`](MONTAJE.md).

| Módulo | Para qué | Notas |
|---|---|---|
| **M1** Convertidor DC-DC 24 → 5 V comercial (Traco THN 10-4811WIR o convertidor automoción sellado 9–36 V) | Alimentar el ESP32 | Fusible en línea 3 A, alimentación tras la llave |
| **M2** Módulo CAN 3,3 V: **Adafruit CAN Pal** (TJA1051T/3) | Bus J1939 | **Terminación en OFF** (con un SN65HVD230, quitar su resistencia de 120 Ω); SLNT en GPIO4 para silencio por hardware; cable de 3 hilos < 1 m: H/L trenzados a B1/B2 (o JB14/JB6) y GND a B9/B10 (masa común con la E-ECU) |
| **M3** Módulo relé 1 canal NO/NC, optoacoplado, disparo a nivel alto | Vía B: poner 24 V en la línea B4 | COM ← terminal 2 del interruptor 26 (+24 V de F24); NO → terminal 3 (línea B4). En reposo manda el interruptor original |
| **M4** Módulo optoacoplador 24 V → 3,3 V, 2 canales | Leer el estado real de B4 y la posición del selector Auto/Manual | OUT1 → GPIO35, OUT2 → GPIO39 |
| **M5** Placa **ESP32_Relay X1 V1.2** (ya disponible; integra M1 y M3) | Lógica, CAN, interfaz, relé | G17/G18 CAN + G4 SLNT, **GPIO16 relé (confirmado)**, G21/G22 I²C, G32/G33/G27 encoder · firmware v0.1 en `firmware/esp32/` |
| **M6** Encoder KY-040 + OLED SSD1306 | Mando y pantalla | rpm real, consigna, estado B4, temperatura, códigos DM1 |
| **Herramienta** adaptador USB-CAN para el PC (CANable / candleLight o "USB CAN analyzer") | Capturar el bus y validar TSC1 | Imprescindible antes de transmitir nada |

Caja IP65 con prensaestopas, bornes y faston; masa única al chasis.

## 3. Regla de seguridad con la bomba

Mientras no se regule la válvula power shift, **el selector Auto/Manual se queda en MANUAL**: así la válvula recibe los 340 mA de la Resistor Box (85 % del par de bomba, como de fábrica). **No pasar a AUTO sin V-ECU**: en Auto la válvula se alimenta desde los pines JA32/JA5 de la V-ECU; sin ella queda a 0 mA, la bomba va al máximo y el motor se puede calar bajo carga.

Para la E-ECU, "Manual" no existe como tal: solo ve el pin B4 y lo que llega por CAN. Por eso la prueba clave es si acepta TSC1 **con el selector en Manual**.

## 4. Plan de trabajo

### Fase 1 — Captura del bus (sin transmitir)

Procedimiento paso a paso y script en [`CAPTURA_CAN.md`](CAPTURA_CAN.md) (`tools/captura_can.py`).

1. Conectar el USB-CAN (o el ESP32 en `LISTEN_ONLY`) a B1/B2 a 250 kbit/s con el motor en marcha. Confirmar EEC1 (`0x0CF00400`, rpm), ET1, DM1 y anotar **todos** los IDs y periodos. Comprobar qué DTC publica la E-ECU sin V-ECU (SID 231 / PSID 201).
2. Medir B1–B2 con la máquina apagada: ≈60 Ω = dos terminaciones; ≈120 Ω = solo la de la E-ECU (117 Ω medidos en la E-ECU suelta), el panel no termina el bus → terminación del SH-C30A o del CAN Pal en ON. **No puentear nada en el conector de la V-ECU**: E-ECU, panel y V-ECU van empalmados en el mismo par y JB13/JB5 son mallas ([`CAPTURA_CAN.md`](CAPTURA_CAN.md) §1).
3. **Capturar una EC210B / EC240B / EC290B sana en Auto** (o una V-ECU prestada en esta máquina): mensajes con SA 0x11, periodo, bytes que cambian al mover el dial, mensajes de llave/arranque. Es la única forma de saber qué espera la E-ECU.

### Fase 2 — Prueba de TSC1
4. Máquina parada, palanca de seguridad bloqueada, selector en Manual, interruptor 26 en neutral (800 rpm). Enviar TSC1 `ID 0x0C000011, 10 ms, byte1 0xF1, consigna 900 rpm` y mirar EEC1.
   - Si sigue la consigna → vía A validada; subir por escalones hasta 1900 y comprobar que al cesar TSC1 vuelve a 800.
   - Si no responde: probar byte1 `0xC1` (prioridad máxima), SA 0x03, interruptor 26 en alta, y revisar DM1. Si la E-ECU exige otros mensajes de la V-ECU, replicarlos a partir de la captura del punto 3.
5. Comprobar comportamiento al perder TSC1 (debe volver a B4) y al reiniciar el ESP32.

### Fase 3 — Vía B (siempre disponible)
6. Relé M3 en paralelo con el contacto 2–3 del interruptor 26: el ESP32 conmuta 800/1900 rpm. Lógica útil aunque no exista TSC1: **auto-ralentí** (bajar a 800 rpm tras N segundos sin actividad, detectada por CAN — par del motor en EEC1 — o por los presostatos de pilotaje), **vuelta a 1900 rpm** al mover un mando.

### Fase 4 — Interfaz
7. Encoder: consigna de rpm (vía A) o selección 800/1900 y tiempo de auto-ralentí (vía B). OLED con rpm real, consigna, temperatura, estado B4 y códigos.

## 5. Mensajes CAN de referencia

| Mensaje | ID | Contenido |
|---|---|---|
| **TSC1** (petición) | `0x0C000011` (prio 3, PGN 0, DA 0x00, SA 0x11) | byte 1 = `0xF1` (modo velocidad, resto a 1); bytes 2–3 = rpm / 0,125 little-endian (1500 rpm → `E0 2E`); bytes 4–8 = `0xFF`. Periodo 10 ms |
| **EEC1** (motor) | `0x0CF00400` | bytes 4–5 = rpm × 8 (0,125 rpm/bit); byte 3 = par real % − 125 |
| EEC2 | `0x0CF00300` | byte 3 = % carga |
| ET1 | `0x18FEEE00` | byte 1 = refrigerante °C − 40 |
| DM1 | `0x18FECA00` | DTC activos (SPN/FMI) |
| Request EC1 | `0x18EA0011` datos `E3 FE 00` | pide PGN 65251: ralentí y ralentí alto configurados |

## 6. Lo que queda aparcado

La regulación de la válvula power shift (driver de corriente o amplificador de válvula) y el anti-calado quedan documentados en [`ESQUEMA_CONEXION.md`](ESQUEMA_CONEXION.md) (§1.3 versión modular) y en los esquemas `esquema_modular_ESP32.svg` / `esquema_conexion_ESP32.svg`, para retomarlos más adelante.
