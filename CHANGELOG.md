# Changelog

Todos los cambios relevantes del proyecto se documentan aquí. Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/); versionado [SemVer](https://semver.org/lang/es/).

## [Unreleased]

### Añadido (hardware disponible)
- `docs/HARDWARE_PLACA_ESP32_RELE.md`: evaluación de la placa ESP32-WROOM-32E con relé y entrada 24 V (LC Technology) que ya tiene el usuario: sirve como cerebro, convertidor y relé de la vía B; lista de comprobaciones (chip del convertidor, GPIO del relé, programación por P4) y qué módulos sobran de la lista de compra.
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
- Fase 0: mediciones en la máquina (bobina, Resistor Box, corriente real en emergencia, resistencia CAN H–L con la V-ECU desenchufada, tensión en B4).
- Firmware Fase 1 (ESP32, PlatformIO): lazo PI de corriente, dither, rampas, relé de seguridad, watchdog, encoder + OLED.
- Firmware Fase 2: TWAI en solo escucha, decodificación EEC1/ET1/DM1, anti-calado (ESSPC).
- Captura del bus J1939 de una EC210B sana para confirmar el mensaje de petición de régimen (Fase 3).
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
