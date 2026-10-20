# Changelog

Todos los cambios relevantes del proyecto se documentan aquí. Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/); versionado [SemVer](https://semver.org/lang/es/).

## [Unreleased]

### Añadido (captura del bus)
- `docs/CAPTURA_CAN.md` y `tools/captura_can.py`: mediciones con el multímetro, captura del bus J1939 con el adaptador **DSD TECH SH-C30A** (comprado) en modo solo escucha verificado, notas durante la captura y análisis automático (IDs, periodos, EEC1 rpm/par, ET1, DM1 incluidas multitrama, TSC1).

### Cambiado (programación)
- Montaje de programación documentado tal como está: programador conectado solo con **GND, TX y RX**; **EN e IO0 sin cablear**, se graba manteniendo pulsado el botón IO0 al dar tensión. Actualizados `MONTAJE.md` (procedimiento paso a paso), `HARDWARE_PLACA_ESP32_RELE.md`, `README.md`, `firmware/README.md` y el diagrama de montaje (se quita el cable G0 → IO0).

### Cambiado (documentación sincronizada con el firmware v0.1)
- `README.md`, `docs/PINOUT_E-ECU.md`, `docs/CONTROL_RPM.md`, `docs/HARDWARE_PLACA_ESP32_RELE.md`, `docs/ESQUEMA_CONEXION.md`, `docs/INVESTIGACION_V-ECU_EC210B.md` y los esquemas `esquema_rpm_ESP32` y `pinout_E-ECU_conector_B_ESP32`: módulo CAN **CAN Pal** (G17/G18, SLNT en G4, terminación OFF, GND a B10), **relé confirmado en GPIO16**, placa ESP32_Relay X1 en lugar de ESP32 DevKit; el esquema de conexión original queda marcado como diseño de la fase hidráulica. Lista de pendientes actualizada.

### Añadido (firmware v0.1)
- `firmware/esp32/`: firmware del control de rpm para la placa ESP32_Relay X1. Modos **Reposo / Alto / Auto-ralentí** sobre el relé de B4 (GPIO16), lectura J1939 en solo escucha (EEC1 rpm y par, ET1 refrigerante, DM1 averías), **TSC1** solo en el entorno `esp32dev_tsc1`, encoder con selección de modo y ajustes, OLED SSD1306 opcional, consola serie, ajustes guardados en flash y watchdog de 500 ms.

- `docs/esquema_montaje_ESP32.svg/.png`: diagrama ilustrado de montaje (placa vista por la serigrafía, programador, CAN, OLED, encoder, conector B de la E-ECU, interruptor 26 y alimentación), enlazado en `README.md` y `docs/MONTAJE.md`.

- Módulo CAN elegido: **Adafruit CAN Pal (TJA1051T/3)**, con interruptor de terminación (OFF en la máquina). Su pin **SLNT va a GPIO4**: el firmware lo pone en alto desde el arranque (transceptor en silencio por hardware) salvo en el entorno `esp32dev_tsc1`.

- Firmware con SLNT grabado en la placa y verificado por la consola serie (Reposo, relé en reposo, CAN en solo escucha).
- `tools/gen_esquema_montaje.py`: script que genera `docs/esquema_montaje_ESP32.svg` (el PNG se exporta con Chrome en modo headless).

### Cambiado
- Masa común con la E-ECU: el borne GND del CAN Pal va a B10 (o B9) junto con CAN H/L (cable de 3 hilos), y la masa de la placa se toma en el mismo punto que la E-ECU. Actualizados el diagrama, `MONTAJE.md` y `CONTROL_RPM.md`.
- Diagrama de montaje redibujado con la placa vista por delante (como en las fotos del fabricante), el número de GPIO de cada pin y el CAN Pal con su forma real.
- `docs/LISTA_COMPRA.md` reducida al control de rpm: quitado lo que ya cubre la placa ESP32_Relay y el programador; pendiente solo módulo CAN, OLED, USB-CAN y material de instalación (≈ 130–180 €).
- `README.md` y `firmware/README.md` actualizados con el estado del banco y el firmware.

### Añadido (pruebas de banco)
- `firmware/pruebas/led` y `firmware/pruebas/rele`: proyectos PlatformIO de prueba. Programación por P4 con el programador USB-C (COM5) verificada: ESP32-D0WD-V3 rev 3.1, flash 4 MB. **Relé confirmado en GPIO16**; el LED de la placa es el indicador del relé (no hay LED en GPIO2).

### Añadido (hardware disponible)
- `docs/HARDWARE_PLACA_ESP32_RELE.md`: evaluación de la placa ESP32-WROOM-32E con relé y entrada 24 V (LC Technology) que ya tiene el usuario: sirve como cerebro, convertidor y relé de la vía B; lista de comprobaciones (chip del convertidor, GPIO del relé, programación por P4) y qué módulos sobran de la lista de compra.
- `docs/MONTAJE.md`: guía de montaje con el hardware real (preparación de la placa, programación con EN opcional explicado, conexión de módulos y a la máquina, primeras pruebas). `CONTROL_RPM.md` y `esquema_rpm_ESP32.svg/.png` actualizados a la placa ESP32_Relay X1 (CAN G17/G18, relé GPIO16 a confirmar, alimentación 24 V integrada).
- Placa identificada como **ESP32_Relay X1 V1.2** (serigrafía del reverso): pinout completo de las dos tiras de taladros, P4 = IO0/GND/GND/RX/TX/5V, conexión del programador y **asignación de GPIO para el control de rpm** (relé GPIO16 a confirmar, CAN 17/18, I²C 21/22, encoder 32/33/27, opto 35/39) en `docs/HARDWARE_PLACA_ESP32_RELE.md`.
- Programador USB-C con auto-descarga (WCH + AMS1117, pines 5V/3.3V/RXD/TXD/EN/G0/GND) disponible: sustituye al adaptador USB-TTL A10; conexión documentada.
- Confirmado que el micro-USB de la placa ESP32 es solo de alimentación: añadido a la lista de compra el **adaptador USB-TTL 3,3 V** (A10, AZDelivery CP2102 HW-598 y alternativas en Amazon.es).
- Módulo de 4 relés de estado sólido disponible: evaluado; **no sirve** (salida de alterna G3MB-202P, no corta en continua).
- Módulo IBT-2 (BTS7960) disponible: evaluado; no necesario para rpm y con poco margen de tensión (27,5 V) para la máquina de 24 V.
- Módulo L298N disponible: evaluado en `docs/HARDWARE_PLACA_ESP32_RELE.md` (no necesario para rpm; posible etapa de potencia de la válvula en la fase hidráulica).
- Encoder rotativo ya disponible: marcado en `docs/LISTA_COMPRA.md` (A6).
- `docs/fotos/`: fotos de la E-ECU (etiquetas, placa LucasVarity, conectores) y de la placa ESP32.

### Cambiado (lista de compra y referencias)
- `docs/LISTA_COMPRA.md` reescrita para el alcance "solo rpm": únicamente componentes (sin herramientas ya disponibles ni material hidráulico), todos **módulos premontados** y con **productos de Amazon España** (ASIN, precio orientativo, alternativas), más adaptador USB-CAN como imprescindible y pedido mínimo para empezar. Informe de búsqueda completo en `docs/anexos/I_productos_amazon_es.md`.
- Corregida la referencia del convertidor Traco: **THN 10-4811WIR** (el sufijo "TEN 10-…WIR" no existe) en documentos y esquemas.

### Cambiado (alcance)
- **El proyecto se centra, por ahora, solo en la gestión de las rpm del motor**; la regulación hidráulica (válvula power shift) se aplaza. Nuevo documento `docs/CONTROL_RPM.md` (dos vías: TSC1 por CAN y relé sobre el pin B4; regla de seguridad con el selector en Manual; plan de captura y pruebas) y esquema `docs/esquema_rpm_ESP32.svg/.png` con solo módulos premontados. README actualizado.

### Añadido
- `docs/PINOUT_E-ECU.md`: tablas completas de los conectores B (máquina) y A (motor) de la E-ECU 03161983, con la función en la excavadora (circuito OEM EC160B–290B), la función de referencia en el camión D12 (Vectro II), colores de cable y la conexión pin a pin al ESP32 con el procedimiento de comprobación.
- `docs/pinout_E-ECU_conector_B_ESP32.svg` / `.png`: diagrama del conector B de 36 pines con código de colores por función y el esquema de conexión al ESP32 (CAN, masa, lectura opcional de B4).
- README: sección 2d con el diagrama del conector B y su explicación.
- `docs/esquema_modular_ESP32.svg` / `.png` y sección 1.3 de `ESQUEMA_CONEXION.md`: **versión modular** del regulador con solo módulos premontados (convertidor DC-DC comercial, amplificador de válvula proporcional 0–10 V, DAC GP8403, INA226, módulo relé NO/NC, módulo CAN, módulo optoacoplador, ESP32 sobre placa de bornes). Pasa a ser la versión recomendada; el circuito discreto queda como alternativa.

### Cambiado
- Alimentación: se sustituye el circuito propio (fusible + polaridad + TVS + DC-DC) por un **convertidor comercial aislado de entrada ancha** (Traco TEN 10-4811WIR) en el esquema, la BOM y la lista de compra.
- `docs/LISTA_COMPRA.md`: lista de compra completa por bloques (medida, electrónica Fase 1, CAN, conectores, protección/caja, banco de pruebas, alternativa Nano), con referencias, cantidades, tiendas, precios orientativos, coste total estimado y orden de compra.

### Pendiente
- Comprar y montar el **CAN Pal**, la **OLED** y el adaptador **USB-CAN** (`docs/LISTA_COMPRA.md`).
- Confirmar el chip del convertidor de la placa (XL7005A, 5–80 V) y probarla en banco a 24–30 V.
- Mediciones en la máquina: resistencia CAN H–L con la V-ECU desenchufada (¿hay que puentear JB13↔JB14 y JB5↔JB6?), tensión en B4 con el interruptor 26 en ralentí y en alta.
- **Captura del bus J1939** de esta máquina (y, si es posible, de una EC210B sana en Auto) con el USB-CAN y con el firmware en solo escucha.
- Validar en la máquina el modo **Auto-ralentí** (umbral de par en EEC1) y, tras la captura, la **vía A (TSC1)** con el entorno `esp32dev_tsc1` y la máquina parada.
- Fase hidráulica (aplazada): driver de la válvula power shift y anti-calado.
- Identificar la familia de los conectores de 36 vías (E-ECU) y JA/JB (V-ECU).

## [0.1.0] — 2026-10-19

Primera publicación: investigación, identificación del hardware y diseño del regulador.

### Añadido
- `README.md` con el planteamiento, el plan por fases y el resumen de lo confirmado.
- `docs/INVESTIGACION_V-ECU_EC210B.md`: documento principal con resumen ejecutivo, arquitectura eléctrica de la EC210B, protocolo J1939/J1587, códigos de fallo, propuesta técnica por fases, plan de verificación y lagunas abiertas; dos actualizaciones con los hallazgos tras identificar la E-ECU.
- `docs/ESQUEMA_CONEXION.md`: puntos de conexión en la máquina (pines E-ECU y V-ECU confirmados por el boletín OEM "UPDATE EC160B~460B"), cableado del selector Auto/Manual, aviso sobre el bus (la V-ECU es nodo de paso), tablas de pines para ESP32 DevKit V1 y Arduino Nano, lista de materiales y secuencia de puesta en marcha.
- `docs/esquema_conexion_ESP32.svg` / `.png`: esquema de conexión completo (alimentación 24 V protegida, driver de corriente con MOSFET low-side + shunt + INA226, relé de seguridad con Resistor Box en NC, transceptor SN65HVD230, encoder, OLED, entradas opcionales).
- `docs/anexos/`: ocho informes de investigación con fuentes y fiabilidad:
  - A. Arquitectura eléctrica, modo de emergencia, bomba, hardware de potencia.
  - B. Protocolos J1939/J1587, TSC1, VP70, mensajes del motor, códigos, ESP32/Arduino CAN.
  - C. Foros: averías típicas de la V-ECU, reparación, clonado, uso prolongado en Manual.
  - D. Familia LucasVarity / Volvo D12 EECU (Vectro II): pinouts de camión, comportamiento sin VECU.
  - E. Volvo Penta EMS/EDC III y Deutz EMR2, controladores de grupos electrógenos.
  - F. L90E/L120E/EW-B con la misma E-ECU, programación con VCADS, saltos de serie.
  - G. Conectores: identificación y dónde comprarlos.
  - H. Deutz EMR2: descripción del sistema, pines F/M, CAN, SERDIA.
- `docs/esquemas/`: 132 imágenes de esquemas (circuitos OEM de la E-ECU y de la V-ECU, bus J1939/J1587, interruptor de emergencia, pinouts EA/EB del D12, red J1939 de camión, Volvo Penta EMS, Deutz EMR2, controladores ComAp/DEIF/Woodward).
- `docs/manuales/README.md`: índice de los 57 manuales consultados, con origen y notas (los PDF no se incluyen en el repositorio).
- `firmware/README.md`: estructura prevista del firmware.

### Hallazgos clave de esta versión
- La referencia "VCE56003584 D6D EAE2" de la etiqueta es un identificador de programación; la pieza es la **E-ECU Volvo 03161983 P03** (LucasVarity, Made in UK), misma familia que la EECU de los camiones Volvo D12.
- El modo de emergencia de fábrica limita la bomba a **340 mA** mediante una Resistor Box de ≈60 Ω; si la máquina "va a tope", probablemente ese circuito está averiado.
- Corrección del pinout CAN de la V-ECU: **CAN H = JB14 / JB13, CAN L = JB6 / JB5** (dos pares; la V-ECU une el tramo de la E-ECU con el del panel).
- El pin **B4** de la E-ECU es una entrada de dos estados (< 4 V ralentí, > 8 V alto): no permite regulación continua de rpm.
- Volvo Penta TAD650VE–760VE **no** comparte centralita (common rail, EMS2); la Deutz EMR2 estándar tampoco (2 × 25 pines), aunque el firmware/datasets pertenecen a la familia "EMR".
