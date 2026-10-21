# Changelog

Todos los cambios relevantes del proyecto se documentan aquí. Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/); versionado [SemVer](https://semver.org/lang/es/).

## [Unreleased]

### Añadido (punto de conexión)
- Diagrama de captura: la pantalla del portátil muestra el **panel del bus** (aplicación propia, 127.0.0.1:8766), con cómo abrirlo (acceso del escritorio o `panel_bus.py`, `--demo`) y el panel de la placa ESP32 por el otro USB. Pasos y análisis desde la guía y el botón Analizar del panel.
- Guía paso a paso del panel del bus (`tools/panel_bus.html`) al día con el punto de conexión real: medidas y conexión en **E7/E8** del conector redondo y masa en un perno de chasis/motor (antes B1/B2/B9 en la clavija de la E-ECU). `docs/CAPTURA_CAN.md` §1 y §3, igual.
- README: sección «Captura del bus con el portátil (pruebas)» con el diagrama de conexión del portátil y el del DIP del SH-C30A.
- `docs/esquema_captura_CAN` rehecho: el SH-C30A va al **conector redondo** (CAN_H → E7, CAN_L → E8) y la masa a un **perno de chasis/motor**; medidas previas sobre E7/E8 y la masa. La clavija de la E-ECU ya no aparece como punto de conexión.
- `docs/CAPTURA_CAN.md` §3b: resultado de la búsqueda de esquemas para el resto de contactos. No hay pinout publicado. La L120E (misma E-ECU) confirma que la masa EB9/EB10 va directa a un punto de masa. Se descartan Deutsch HD10/HD16/HD30. Propuesta [INFERIDA] para I2/I3 y E2–E6, y prueba de continuidad que lo resuelve.
- README: estado del 2026-10-21 (punto de conexión en la máquina), sección 2e con el dibujo del conector redondo y nota en 2d sobre dónde tomar CAN, masa y B4 en la máquina; contenido del repositorio al día (`conector_MC02`, `fotos/`, `gen_conector_MC02.py`).
- `docs/conector_MC02.svg/.png` (`tools/gen_conector_MC02.py`) y `docs/fotos/conector_MC02_frontal.jpg`: dibujo de la cara de contactos del conector redondo del mazo de la E-ECU (13 posiciones, 9 contactos montados; numeración propia con E1 = cavidad exterior vacía como referencia).
- Mediciones en la máquina (`docs/CAPTURA_CAN.md` §3b): **E7 = CAN H (B1)** y **E8 = CAN L (B2)** confirmados; **B4 (emergencia) y B9/B10 (masa) no pasan por este conector**. La masa del SH-C30A se toma de un perno de chasis/motor o del negativo de batería; la vía B sigue en el interruptor 26 o en JA47.

### Corregido (punto de conexión)
- La deducción «MC02.1 = emergencia B4» del esquema SCH02-1 no se cumple en esta máquina: identificación del conector redondo como MC02 rebajada a fiabilidad baja; §3b y §3c al día con E7/E8.
- `docs/CAPTURA_CAN.md` §3: la masa del SH-C30A puede tomarse de cualquier masa buena junto a la E-ECU (perno de chasis/motor o negativo de batería) si B9/B10 no son accesibles; sigue siendo imprescindible junto a CAN H/L.
- `docs/CAPTURA_CAN.md` §3c: la clavija de la E-ECU no sirve (A y B en la misma carcasa). Opciones sin cortar cables: **clavija libre del mazo de la V-ECU** (JB14 CAN H, JB6 CAN L, JA47 emergencia/B4, JB7/JB8 +24 V, JA15/JA63 masa) como opción recomendada, adaptador en "Y" en MC02, back-probe o extracción de contactos; con las comprobaciones previas.
- Conector redondo identificado como probable **MC02** («mazo del EMS») a partir del esquema SCH02-1 de la EC160B–290B: MC02.2 CAN H, MC02.3 CAN L, MC02.4/5 J1587 A/B, MC02.1 línea de emergencia (B4); sin masa. Tabla en `docs/CAPTURA_CAN.md` §3b y ampliación del esquema en `docs/esquemas/`. Pendiente de confirmar con el multímetro.
- `docs/CAPTURA_CAN.md` §3b y `docs/fotos/conector_redondo_mazo_maquina.jpg`: conector redondo del mazo de la E-ECU como posible punto de conexión del CAN (la tapa de la clavija de la E-ECU impide el back-probe). Procedimiento para identificar CAN H/L y masa con el multímetro; conector pendiente de identificar.

### Corregido (SH-C30A)
- DIP del SH-C30A dibujado al revés: en la unidad real la marca **ON está abajo** (palanca abajo = ON, arriba = OFF). Corregidos `esquema_switches_SH-C30A` y el DIP de `esquema_captura_CAN` (generadores y PNG).

### Añadido (SH-C30A)
- `docs/esquema_switches_SH-C30A.svg/.png` (`tools/gen_switches_shc30a.py`): cómo poner el **DIP de 2 interruptores** del SH-C30A para cada caso (captura con 60 Ω o 120 Ω, banco, actualizar firmware). Asignación sacada del esquema oficial: **1 = arranque (BOOT0, ON = DFU)**, **2 = terminación R120**. Diagrama de captura y `CAPTURA_CAN.md` actualizados con el DIP.
- Diagrama de montaje: aviso junto a los cables del programador de que **TX → RXD y RX → TXD van cruzados a propósito** (es lo correcto).

### Corregido
- Diagrama de montaje: en las dos tiras de pines de la placa estaban **intercambiadas la fila interior y la exterior**. Corregido en `tools/gen_esquema_montaje.py` con el cableado rehecho (IO4/IO17/IO18/IO22 y GND en la fila interior de la tira izquierda; IO27/IO32, 3V3 y GND en la exterior de la derecha).
- Revisión del diagrama de montaje: comentarios del generador al día con las filas corregidas, rótulo «AMS1117» legible, programador rotulado como `ttyACM0 / COMx`; en `docs/HARDWARE_PLACA_ESP32_RELE.md`, qué fila de cada tira es la interior y cuál la exterior.

### Añadido (registros y guía)
- **Registro automático de cada sesión** (carpeta `registros/`, fuera de git): el panel del bus guarda `bus_completo.log` (todas las tramas y notas), `motor.csv` (1/s) y `eventos.log` (conexiones, nodos, averías que aparecen/desaparecen, TSC1, V-ECU, grabaciones, notas y resumen cada 10 s); el panel de la placa guarda todo lo que dice la placa, los comandos y un resumen cada 10 s. Se cierran bien también al cerrar la ventana del terminal.
- **Guía paso a paso** en el panel del bus: los 12 pasos de `CAPTURA_CAN.md` con qué hacer, qué debería verse y comprobaciones en directo; las medidas del multímetro se apuntan en la guía y van al registro.

### Añadido (panel del bus)
- Si el SH-C30A arranca en modo DFU (interruptor DIP 1 en ON, aparece como `0483:df11`), el panel lo dice en lugar de «no se encuentra».
- `tools/panel_bus.py` + `panel_bus.html` (127.0.0.1:8766): lectura del bus J1939 con el SH-C30A en solo escucha, en el navegador: rpm, par, carga, temperaturas, aceite, batería y horas; gráficas de rpm y par con notas; averías DM1 (también multitrama) con lámparas; nodos con avisos (V-ECU 0x11, TSC1, E-ECU sola); tabla de mensajes con bytes que cambian; grabación de las 6 pruebas de `CAPTURA_CAN.md` en el formato de `captura_can.py`, con notas y análisis al terminar. Modos `--demo` (E-ECU simulada) y `--reproducir`. Probado en demo; con el SH-C30A sin enchufar avisa y reintenta solo.

- Accesos en el escritorio a los dos paneles: `tools/linux/instalar_accesos.sh` crea «Panel placa ESP32» y «Panel bus J1939», que lanzan `tools/linux/abrir_panel.sh`. Si un panel ya está en marcha, una segunda copia solo abre el navegador (y no toca el adaptador).

### Añadido (panel)
- `tools/panel_esp32.py` + `panel_esp32.html`: panel en el navegador (127.0.0.1:8765) con todas las funciones de la consola serie: modos y relé, ajustes (ralentí, par, consigna TSC1), datos del motor y del bus CAN, log filtrable y descargable, comandos libres y <kbd>Esc</kbd> = Reposo. Abre el puerto en exclusiva y reencuentra el programador si cambia de nombre. Probado con la placa real (2026-10-21). Documentado en `firmware/README.md`.
- Panel: el modo actual se ve en grande y con color propio (Reposo verde, Alto naranja, Auto-ralentí azul, TSC1 morado) en la cabecera fija, en una franja con las rpm objetivo y en el título de la pestaña.

### Pruebas (2026-10-21)
- Encoder soldado y conectado (G32/G33/G27): giro, elección de modo, edición de parámetro y pulsación larga → Reposo verificados con el panel.
- Arranque de la placa sin pulso en el relé: COM–NO no se cierra en varios arranques seguidos (LED apagado, sin clic).
- OLED SSD1306 conectada (IO21/IO22, 3V3): detectada al arrancar y pantallas verificadas (modo, selección `> MODO ?`, edición, `----` rpm sin CAN).
- Panel: la lista de puertos solo muestra puertos USB (en Linux ocultaba el programador entre `ttyS0…ttyS31`).
- Lección del banco: para reiniciar la placa, quitar solo su micro-USB, no el programador (el puerto cambia de nombre); los cables de datos del programador van **cruzados** (TXD → RX, RXD → TX).

### Pruebas (2026-10-20)
- E-ECU suelta en el taller: B1–B2 = 117 Ω, B9–B10 y B11–B12 en continuidad, B11–B9 sin cortocircuito (`docs/PINOUT_E-ECU.md`).
- Placa en la mesa desde el portátil Linux: relé COM–NO / COM–NC verificados en Reposo y Alto; Auto-ralentí sin CAN se mantiene en alto; arranque siempre en Reposo tras quitar tensión (`docs/MONTAJE.md` §5).

### Corregido (bus J1939)
- **La V-ECU no es un nodo de paso.** Revisado el circuito OEM a 300 ppp: E-ECU (EB1/EB2), panel (1/2) y V-ECU (**JB14 H / JB6 L**) van empalmados en el mismo par, y **JB13 / JB5 son las mallas** de los cables J1587 / J1939, no un segundo par CAN. Sin V-ECU el bus no se parte. Retirada en toda la documentación y los esquemas la instrucción de puentear JB13↔JB14 y JB5↔JB6 (habría unido CAN a las mallas).
- **Medida en el taller (2026-10-20):** B1–B2 de la E-ECU suelta = **117 Ω**, terminación interna confirmada. En la máquina, B1–B2 ≈ 60 Ω → R120 / terminación del CAN Pal en OFF; ≈ 120 Ω → el panel MDU no termina el bus y van en ON.
- `docs/CAPTURA_CAN.md`: medidas 0, 1 y 1b, regla del R120 según la medida y aviso de qué hacer si la E-ECU está sola en el bus (nadie confirma sus tramas).
- Diagramas `esquema_captura_CAN` (topología redibujada con la V-ECU como derivación), `esquema_conexion_ESP32`, `esquema_modular_ESP32` y `esquema_rpm_ESP32` corregidos y exportados de nuevo; nota de corrección en los anexos A y G.

### Añadido (repositorio)
- `.gitattributes`: finales de línea LF en todos los ficheros de texto (también al editar en Windows); imágenes y binarios sin conversión.

### Añadido (portátil de pruebas con Linux)
- `tools/requirements.txt`: entorno de Python del proyecto (`.venv`, creado con `uv`) con PlatformIO y las librerías de captura.
- `tools/linux/70-vecu.rules` e `instalar_permisos.sh`: permisos USB sin sudo para el SH-C30A (candleLight, también en modo DFU) y el programador del ESP32 (WCH / CP210x). Instaladas en el portátil.
- `docs/CAPTURA_CAN.md` §2 y `firmware/README.md`: preparación en Linux (Windows queda como alternativa).

### Cambiado (portátil de pruebas con Linux)
- `platformio.ini` (firmware y pruebas de banco): sin `COM5` fijo, el puerto se detecta solo en Windows y en Linux.
- `tools/captura_can.py`: el aviso de adaptador no encontrado indica también la solución en Linux.

### Añadido (captura del bus)
- `docs/esquema_captura_CAN.svg/.png` (generado con `tools/gen_esquema_captura.py`): diagrama de conexiones de la captura — portátil, SH-C30A con su forma real (USB-A directo, bornero CAN_H/GND/CAN_L, R120 y arranque en OFF), sondas a B1/B2/B9, medidas con el multímetro y topología del bus con sus dos terminaciones.
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
