# Investigación: E-ECU Volvo EC210B (D6D, 2002) vs. EECU Volvo D12 "Vectro II / EMS" (LucasVarity)

Fecha: 2026-10-19. Objetivo: verificar si la E-ECU del EC210B (etiqueta "VOLVO — A Product developed in partnership with LucasVarity — 03161983 P03 — 80907C — Made in UK", dos conectores de 36 pines) es el mismo hardware que la EECU de camiones Volvo D12A/B/C, y reunir todo lo útil para emular la V-ECU desde un ESP32.

Escala de fiabilidad: **ALTA** = documento Volvo / norma; **MEDIA** = manual de carrocero, documento de reparación o técnico de terceros reputado; **BAJA** = foro, vendedor, listado de piezas.

Convención: **CONFIRMADO** = respaldado por fuente ALTA o por varias fuentes concordantes; **INFERIDO** = deducción razonable a partir de indicios; **NO ENCONTRADO** = no hallado en fuentes públicas.

---

## 0. Resumen ejecutivo

1. **CONFIRMADO (ALTA):** la E-ECU del EC210B/EC240B/EC290B (D6D) tiene exactamente el mismo pinout de los dos conectores de 36 pines ("Connector A" / "Connector B") que la EECU de camiones Volvo D12B/D12C ("EA" / "EB") documentada por Volvo Trucks North America en el manual *Vectro II* PV776-144528 (2001). Pines críticos idénticos: B1/B2 = J1939 CAN H/L; B25/B26 = J1708/J1587 A/B; B9/B10 = masa; B11/B12 = +batería; B4 = entrada discreta "idle validation" (camión) = "Emergency speed control" (excavadora). Fuentes: manual Vectro II (Volvo, ALTA) y boletín de actualización Volvo CE "UPDATE-EC160B~460B-05-1 EECU Electric Circuit" (Volvo CE Customer Support, 2004, ALTA).
2. **CONFIRMADO (MEDIA/BAJA concordantes):** el mismo hardware se vendió con números 3161962 (D12D en EC460B/L180E/A35D/A40D), 03161983 (D6D/D7D en EC210B/L90E/L120E…), 20577131/20582958/20412506 (D12 camión y D6D/D7D máquinas), 8170700 (D12A/C camión "Lucas", "Made in UK", sufijos P06/P07) y con marca **TRW** en unidades posteriores (20561256 P03, 20814642), coherente con la historia corporativa Lucas → LucasVarity (1996) → TRW (1999). El sufijo "P0x" es una revisión de hardware/producción que Volvo usa en todas estas ECU.
3. **CONFIRMADO (ALTA):** comportamiento de la EECU al perder la V-ECU: pone el código MID 128 SID 231 FMI 12 ("loss of message from the VECU"), pasa a usar J1587/J1708 como respaldo; si fallan ambos enlaces entra en *limp home* y usa la entrada cableada EB4 (idle validation / emergency speed) para decidir entre ralentí y régimen alto. En la excavadora esto es exactamente el modo "Manual" con el interruptor de emergencia (ralentí I2 / alta H) descrito en el manual de operador.
4. **NO ENCONTRADO:** definición pública de los mensajes J1939 propietarios con los que la V-ECU (MID 187 en Volvo CE; MID 144 en camión) pide régimen a la E-ECU. Volvo Trucks dice que el pedal pasa por "J1939" sin nombrar el PGN. Único dato fuerte: la especificación de interfaz eléctrica Volvo Penta EMS/EMS2 acepta **TSC1 desde SA 0x03 (TECU), 0x11 ("OEM controller") y 0xE6 (BBM)** y un mensaje propietario "VP Status" (arranque/paro/acelerador). Hay que sniffar el bus.
5. **NO ENCONTRADO** con fiabilidad: MCU exacta y mapa de memoria de la unidad LucasVarity 1998-2003. Indicios de baja fiabilidad: flash AM29F400 (PLCC), transceptor CAN "A52C251" (= PCA82C251), driver de inyectores de potencia, EEPROM de "data set" (SID 253) y "program memory" flash (SID 240). Reprogramable sólo por línea de programación (pin EB24 "EOL enable / factory programming"); las E-ECU Volvo CE antiguas necesitaron un boletín para añadir una "línea de comunicación" que permitiera reprogramarlas con VCADS Pro.

---

## 1. Familia de hardware: LucasVarity → TRW/Delphi, "EMS"/"Vectro II", números de pieza, conectores

### 1.1 Lo que dice la etiqueta y las fuentes de parte

| Dato | Estado | Fuente | Fiab. |
|---|---|---|---|
| 03161983 = "Controller ECU for Volvo Engine D6D/D7D; EC210B, EC210BLC, EC290B/BLC, L90E, L120E, L110F, L160E, L170F, L190F" | CONFIRMADO (número de la etiqueta coincide con aplicación EC210B/D6D) | https://www.fridayparts.com/controller-ecu-03161983-for-volvo-engine-d6d-excavator-ec210b-ec210blc-ec290blc-wheel-loader-l90e-l120e-l110f-l160e-l190f-l170f | BAJA |
| 3161962 (número hermano, misma serie) = ECU D12D en EC460B, L180E/L180EHL, A35D, A40D; también ECM de camión VED12 1998-2003 | CONFIRMADO (varias fuentes) | https://www.fridayparts.com/ecu-control-unit-voe-3161962-for-volvo-engine-d12d-ved12-excavator-ec460b-wheel-loader-l180e-l180ehl-articulated-hauler-a35d-a40d ; https://www.ebay.com/p/26006017779 ; https://www.autotronics.co.uk/product/volvo-engine-ecu-repair-3161962/ | BAJA/MEDIA |
| 20577131 / 20582958 / 3161962 / 85000846 listados como intercambiables "2D-ECU / D12D1" (camión) y 20577131/20582958 ofrecidos para D6D/D7D (EC240B, EC360B, cargadoras) | CONFIRMADO como solape de numeración entre camión y máquinas | https://www.vtp-uk.com/used-volvo-engine-ecu-20577131-20582958-3161962-548174-85000846-2d-ecud12d1 ; https://ecmrepairusa.com/product/volvo-d6d-d7d-ec240b-ec360b-20577131-20582958-ecm-repair/ ; https://eurodieselecm.com/products/volvo-d12b-d12c-20412506-3161962-20577131-ecm | BAJA |
| 20412508 P01 etiquetado "MOTORSTYRRING D6B 180 EPG 20412508 / 3161965 1 / 20577133" (misma serie 20412xxx / 31619xx / 20577xxx para motor D6B de camión FL) | CONFIRMADO | https://autoline.com/-/sale/control-units/truck/Volvo/ECU-20412508-P01--24021909393063797600 | BAJA |
| 08170700 = ECU D12A/D12C **"LUCAS"** (archivo original de reprogramación: "LUCAS, HW 08170700, SW XXXX3009, Volvo N12 D12C 380hp"; otros SW N12_855C, VXXX39B9, N12_3ABB, N12_41A0, N12_6B33 D12D) | CONFIRMADO que existen ECU D12 marcadas Lucas | https://auto-remap.com/original-files/LUCAS/08170700/XXXX3009 | MEDIA (base de datos de archivos ECU) |
| 08170700 **P06** "Volvo VED12B, made in United Kingdom, requires programming, EEPROM memory"; también 08170700P07 | CONFIRMADO: sufijo P0x y "Made in UK" en la misma familia | https://www.partrequest.com/catalog/engine-computers/volvo?page=7 (resumen de buscador) ; https://heavytruckparts.net/search/Volvo/Ved-12/ECM | BAJA |
| 20561256 **P03** "VOLVO VED D12 ECM ECU EGR Module **TRW**" ; 20814642 "Volvo/TRW ECM", "Country of origin United Kingdom" | CONFIRMADO: generación siguiente marcada TRW (LucasVarity fue comprada por TRW en 1999) | https://www.ebay.com/p/19028108411 ; https://ecmrepairusa.com/product/volvo-d12-ecm-20814642/ | BAJA |
| Historia corporativa: Lucas Industries + Varity = LucasVarity (1996); TRW compra LucasVarity (1999); TRW vende Lucas Diesel Systems a Delphi (ene-2000) → Delphi Diesel Systems (EUI Volvo/Mack/Renault/Penta) | CONFIRMADO | https://en.wikipedia.org/wiki/LucasVarity ; https://dieselnet.com/news/1999/11delphi.php ; https://competition-cases.ec.europa.eu/cases/M.1784 | ALTA/MEDIA |
| Inyectores-bomba (EUI) D12A/B/C de marca LUCAS (315504) y también Bosch; Volvo A40D muestra inyectores "Bosch" y "Delphi" | CONFIRMADO: Lucas/Delphi suministraba los EUI del D12 | https://autoline.com/-/sale/injectors/truck-tractor/Volvo/FH12-FM12-injectors-unit-D12A-D12B-D12C-24V-LUCAS-315504--16041915364436672300 ; https://www.slideshare.net/slideshow/volvo-a40d-engine-control-unit-d12-e-ecu-service-manual-pdf/275267853 | BAJA |
| Afirmaciones contradictorias de vendedores: "Siemens control module" para 1638462 (D12C 1998-2003); "ECM made by Motorola, fuel cooled" (foro) | NO CONFIRMADO; contradicen la etiqueta física LucasVarity y las unidades TRW | https://www.ebay.com/p/1257624796 ; https://www.thetruckersreport.com/truckingindustryforum/threads/1995-volvo-wia64-w-d12-engine-12-sp.160492/ | BAJA |

**Conclusión 1.1 (INFERIDO con base sólida):** el ECU de la etiqueta pertenece a la familia de ECU de motor de Volvo de primera generación (1998-c.2005) desarrollada con Lucas/LucasVarity (electrónica fabricada en Reino Unido), usada como EECU en camiones D12A/B/C/D, D7C y D6B, como E-ECU en Volvo CE (D6D, D7D, D10B, D12C/D) y como ECU "EDC III/EMS" en Volvo Penta D12 (20582963 / 20577134, TAD1240-1242, "Connector 1 black / Connector 2 red"). El software y el dataset cambian por aplicación; el hardware y el pinout son comunes. Volvo nunca la llama "Lucas" en sus manuales; la denomina EECU/E-ECU (MID 128), "Vectro II" en Norteamérica y "EMS" en Volvo CE/Penta.

### 1.2 Pinout = prueba de identidad entre camión D12B/C y excavadora EC210B

Fuente ALTA 1: Volvo Trucks North America, *Vehicle Management System VECTRO II 1998–, Service Manual PV776-144528 (05.2001)*, páginas 24-25 (EECU D12B/D12C conectores EA/EB) — https://www.manualslib.com/manual/1921428/Volvo-Tsi.html?page=24 y ?page=25 ; copia PDF descargada (ver sección Manuales).

Fuente ALTA 2: Volvo Construction Equipment Customer Support, *UPDATE-EC160B~460B-05-1 "EECU Electric Circuit (EC160B/180B/210B/240B/290B)"* (2004) — página 7 del PDF "Volvo EC160B…460B Service Manual" (ver Manuales). Muestra "Connector A" y "Connector B" con los mismos números.

Comparación de los pines relevantes para el emulador:

| Función | Camión D12B/C (Vectro II) | Excavadora EC210B D6D (Volvo CE UPDATE 05-1) | Coincide |
|---|---|---|---|
| J1939 CAN HIGH | EB1 (amarillo, circuito 406) | Connector B pin 1 "J1939_H" | Sí |
| J1939 CAN LOW | EB2 (verde, circuito 407) | B2 "J1939_L" | Sí |
| J1708/J1587 (+) A | EB25 (gris, 400) | B25 "J1708_A" | Sí |
| J1708/J1587 (-) B | EB26 (naranja, 401) | B26 "J1708_B" | Sí |
| Masa (-) | EB9, EB10 | B9, B10 "GND" | Sí |
| Alimentación (+) batería | EB11, EB12 (R/SB) | B11, B12 "24V(+)" ("Power from fuse") | Sí (24 V en máquina; 12 V en camión NA) |
| Entrada discreta "Buffered idle validation switch" | EB4 (rosa) | B4 "Emergency speed control" | Sí (misma entrada, uso distinto) |
| Nivel refrigerante | EB7 (+), EB8 común (-) | B7, B8 | Sí |
| Indicador filtro aire / presión admisión | EB17 | B17 "Inlet press." | Sí |
| Temp. aire ambiente/admisión | EB3 señal, EB13 común | B3 "Inlet temp.", B13 (-) | Sí |
| Relé precalentamiento | EB31 | B31 "Preheat relay" | Sí |
| Programación de fábrica / EOL enable | EB24 (Y/SB) "Factory programming (not used)" | (no rotulado en el esquema CE) | — |
| Sensor cigüeñal (+/-) | EA30 / EA31 | A31 / A30 | Sí |
| Sensor árbol de levas (+/-) | EA7 / EA18 | A7 / A18 | Sí |
| Inyectores cil. 1-3 (-) y común +90 V | EA11, EA22, EA23 / EA12 | A11, A22, A23 / A12 | Sí |
| Inyectores cil. 4-6 (-) y común | EA34, EA35, EA36 / EA24 | (EC360B/460B D12: A34, A35, A36 / A24) | Sí |
| Temp. refrigerante / aceite / combustible | EA25 / EA1 / EA13 | A25 / A1(oil) / A13 | Sí |
| Presión aceite / sobrealimentación / común sensores | EA14 / EA3 / EA4(+) EA5(-) | A14 / A3 / A4(+) A5(-) | Sí |
| Freno motor VCB (sólo D12) | EA33 | (EC360B/460B) | — |
| Ventilador | EB21 | — | — |
| EPG1/EPG2 (freno de escape) | EB35/EB36 | — | — |

**Importante:** Volvo Trucks NO publica un pin de "ignición/llave" en la EECU D12B/C: la posición de llave la recibe la EECU por J1939 desde la VECU ("the VECU passes ignition switch position information to the EECU", Vectro II p.71), y la alimentación EB11/EB12 va a través del relé principal EMS (en la excavadora, relés "EMS"/"DATA" gobernados por la I-ECU, fusible F15 20 A E-ECU). El emulador debe por tanto (a) alimentar la E-ECU por el relé, (b) mantener J1939 vivo y (c) enviar lo que la V-ECU envía.

Tabla completa EA/EB (D12B/D12C) transcrita del manual Vectro II (ALTA):

**Conector EA (lado motor):** 1 temp. aceite; 2 temp. sobrealimentación; 3 presión sobrealimentación; 4 común (+5 V) sensores presión; 5 común (-) sensores; 6 n.u.; 7 sensor posición árbol de levas (+); 8-10 n.u.; 11 inyector cil.1 (-); 12 común inyectores 1-3 (+90 V); 13 temp. combustible (D12C); 14 presión aceite; 15-17 n.u.; 18 árbol de levas (-); 19-21 n.u.; 22 inyector cil.2 (-); 23 inyector cil.3 (-); 24 común inyectores 4-6 (+90 V); 25 temp. refrigerante; 26 n.u.; 27 presión combustible (D12C); 28-29 n.u.; 30 sensor cigüeñal (+); 31 sensor cigüeñal (-); 32 n.u.; 33 retorno solenoide VCB; 34 inyector cil.4 (-); 35 inyector cil.5 (-); 36 inyector cil.6 (-).

**Conector EB (lado vehículo):** 1 J1939 CAN HI; 2 J1939 CAN LO; 3 temp. aire ambiente; 4 buffered idle validation switch; 5 preheat sense 1; 6 n.u.; 7 aviso nivel refrigerante; 8 común filtro aire / nivel; 9 masa; 10 masa; 11 +batería; 12 +batería; 13 común temp. ambiente; 14-15 n.u.; 16 preheat sense 2; 17 indicador filtro de aire; 18-20 n.u.; 21 control ventilador (-); 22-23 n.u.; 24 programación de fábrica / EOL enable; 25 J1708/1587 (+); 26 J1708/1587 (-); 27-30 n.u.; 31 relé precalentamiento (masa bobina); 32-34 n.u.; 35 EPG1; 36 EPG2. (El D7C usa el mismo EB con EB34 = válvula de corte de combustible.)

Valores de comprobación Volvo (Vectro II pp. 18-23): EB11/EB9 y EB12/EB10 = B+; EB1/EB9 ≈ 0-3 V (CAN H), EB25/EB9 y EB26/EB9 ≈ 0-5 V; EB4/EB9 <4 V en ralentí, >8 V fuera de ralentí; EB24/EB9 <6 V = EOL deshabilitado, >9,6 V = EOL habilitado.

### 1.3 Conectores físicos (fabricante, referencias)

- **NO ENCONTRADO** el fabricante ni la referencia del conector de 36 vías. Volvo sólo menciona la herramienta de medición de fuerza de retención de terminales 9998482 y las cajas de medición J-41132 (36 pines, Kent-Moore) / J-43233 (puente 36 pines) / kit Volvo 3917916 (Vectro II pp. 35-36, ALTA).
- Vendedores chinos ofrecen el conector de la E-ECU como "Volvo Controller Engine ECU Connector Plug for EC210/EC240/EC210B ECU 60100000" sin dar fabricante ni cuenta de pines (https://sinocmp.com/products/volvo-controller-connector-plug-for-ec210-ec240-ec210b-ecu-60100000, BAJA). Mazos completos de la E-ECU EC210B: 14512406 / 14512670 / 14513137 (https://wdpart.com/products/14512670-14513137-14512406-ecu-wiring-harness-for-volvo-d6d-d7d-ec210b-ec240b-ec290b, BAJA).
- Volvo Trucks indica que los conectores de carrocero son Delphi/Packard, pero eso no aplica necesariamente a la EECU (https://www.volvotrucks.us/media/vtna/files/shared/body-builder/manuals/2023/maint-1567837-volvo-section-3-vecu4-updates.pdf, ALTA pero para otro conector).
- Numeración de pines: en los esquemas Volvo (camión y CE) el conector se numera 1-36 en matriz 3×12; la posición física de cada cavidad hay que verificarla en la carcasa (los esquemas Volvo CE dibujan la matriz; ver imagen `d12_EC210B_EECU_electric_circuit_EC160B-290B-07.png`).

---

## 2. Pinout EECU D12 camión (A/B = EA/EB) — ver tablas de la sección 1.2

Resumen para el emulador (ALTA, Vectro II PV776-144528):

- **J1939 H/L:** EB1 / EB2 (cables 406 amarillo / 407 verde, 408 pantalla opcional en diseños antiguos). 250 kbit/s. Resistencia terminal de 120 Ω **dentro de la EECU** (el otro terminador está en la caja de fusibles/relés o cerca del ABS). Medida correcta del bus: ≈60 Ω (Vectro II p.47; SB 371-44 "Data links, fault tracing", 12.2004, pp. 8-13).
- **J1708/J1587 A/B:** EB25 / EB26 (cables 400 / 401), 9600 bit/s. Sin terminadores.
- **Batería +:** EB11, EB12. **Masa:** EB9, EB10.
- **Ignición/llave:** no hay pin dedicado en la EECU; la alimentación llega por relé y la información de llave por J1939 (p.71). En la VECU: A13 = alimentación conmutada electrónica (18V), A14 = llave en posición DRIVE (196V).
- **Entradas discretas en la EECU:** EB4 idle validation (buffered, desde VECU B17/555A), EB5/EB16 preheat sense, EB7 nivel refrigerante, EB17 filtro aire, EB3 temp. ambiente, EB24 EOL.
- **Entradas de la VECU relacionadas con régimen (Vectro II pp. 28-29):** Conector A (verde, 30 vías): A1 Cruise/PTO SET(-), A2 Cruise/PTO SET(+), A3 Cruise/PTO ON, A5 freno de servicio, A8 embrague, A12 masa electrónica, A13 alimentación conmutada, A14 llave DR, A20/A21 freno motor medio/bajo, A23 idle validation input (555), A29 PTO switch ON (573), A30 Cruise/PTO RESUME. Conector B (azul, 30 vías): B6 velocidad vehículo, B8 pedal (TPS señal, 553), B10 alimentación TPS (552), B15 "power control from engine ECU" (583), B17 idle validation hacia EECU (555A), B22 retorno TPS (554). Conector C (verde, 5 vías): C1 J1708 (-) 401, C2 J1708 (+) 400, C3 pantalla J1939 408, C4 J1939 CAN H 406, C5 J1939 CAN L 407.

---

## 3. Cómo manda régimen la VECU a la EECU; TSC1; carroceros; pérdida de comunicación

### 3.1 Volvo Trucks (Vectro II, ALTA)

- "The accelerator pedal signals travel first to the VECU and are transferred to the EECU via the J1939 Control Link. If there is a fault in the J1939 Control Link, the accelerator pedal signal travels to the EECU via the J1587/1708 Information Link. The vehicle can also be driven in the 'limp home' mode if there is a fault in both links. In this situation, the idle validation switch is used to determine when the accelerator pedal is pressed; then, the VECU sends a buffered idle validation switch signal (via hard wire) to the EECU." (p.70).
- También por J1939 desde la VECU a la EECU: mandos de crucero/PTO, petición de parada remota, petición de ventilador, posición de llave, límite de régimen con PTO (parámetros VCADS Pro) (pp. 70-72). **El manual no nombra PGN alguno** (no dice si es TSC1 o un PGN propietario). NO ENCONTRADO.
- Pedal por J1587: PID 91 (posición del acelerador) también se transmite por J1587 como respaldo (MID 128 PID 91 FMI 9 = mensaje J1587 ausente; FMI 11 = mensaje J1939 ausente/erróneo; ambos → limp home) (p.105).
- Dirección de origen: las tablas J1939 de Volvo (manual de carrocero 2023, ALTA) muestran SA 0x11 (17) para CCVS y mensajes del VECU; la especificación Volvo Penta llama a 0x11 "OEM controller" y 0xE6 "BBM". En SAE J1939 estándar, 17 = "Cruise Control", 3 = transmisión, 0 = motor. INFERIDO: la VECU Volvo usa SA 0x11.

### 3.2 Volvo Penta EMS / EMS2 (misma generación de ECU D12 en Penta "EDC III"/EMS) — MEDIA/ALTA

- TSC1 (PGN 0) aceptado desde SA **0x03 (TECU), 0x11 (OEM controller), 0xE6 (BBM)**; TSC1 tiene prioridad sobre el pedal del mensaje propietario "VP Status"; el 0x03 tiene prioridad máxima. Tasa esperada 10 ms. (https://www.dieselgeneratortech.com/diesel-engines/More-Available-Control-Functions-of-Volvo-Engine.html ; https://dieselgeneratortechblog.wordpress.com/2018/12/03/volvo-genset-engine-electrical-interface/ ; PDF Volvo Penta 47706587 "OpenCAN install guideline" descargado, pp. 11 y 19, ALTA para EMS2). Documento maestro citado: Volvo Penta 7748665 "Electrical interface specification industrial engines EMS and EMS2" (no localizado en abierto).
- Mensaje propietario "VP Status" (Penta): start, stop, throttle 0-100 %, governor mode, idle, preheat, frequency select, diagnostic request, engine protection override. Equivalentes J1587: PPID 98 (start/stop), PPID 132 (throttle). Conector Penta de 8 pines: 1 CAN H, 2 CAN L, 3 Bat-, 4 Bat+, 5 ignición/stop (energize to run), 6 stop (energize to stop), 7 J1587 A, 8 J1587 B.
- INFERIDO: la V-ECU de Volvo CE usa un mecanismo análogo (mensaje propietario de petición de régimen + posiblemente TSC1). Debe comprobarse con un sniffer antes de emular.

### 3.3 Carroceros (Volvo VN/VHD, documentos modernos, ALTA pero posteriores a la generación D12)

- Body Builder Instructions Section 3 (USA170229709, 04.2023): con parámetro BB_BUS_CONTROL el carrocero puede "issue direct torque and speed commands to the engine using the J1939 TSC1 message, within limits"; las peticiones de velocidad se retransmiten como si procedieran del BBM; límites de velocidad/par se colocan con la SA del carrocero. Con BB_BUS_LISTEN el BBM reenvía ETC1, ETC2, CCVS (VECU), EEC1, EEC2. Advertencia Volvo: "devices affecting engine speed are known to exist on the market", no se debe emitir en el bus principal. (PDF descargado).
- Section 9 PTO (2023): el "remote PTO" se activa por una entrada dedicada de la VECU y "the VECU passes that information to the Engine ECU over the J1939 datalink". No hay documento público de carrocero 2001-2004 para D12 (NO ENCONTRADO).
- Volvo Truck Corporation (Europa) "Body builder instructions – PTO": "an engine speed request can be initiated using the steering-wheel buttons… refer to Engine speed control in the Vehicle…" (PDF descargado, MEDIA/ALTA).

### 3.4 Comportamiento de la EECU al perder la VECU (ALTA, Vectro II pp. 188-189, 105, 187)

- MID 128 SID 231 FMI 2/9/11: enlace J1939 no funciona → la EECU "moves information to the SAE J1587 link"; lámpara ámbar; dejan de funcionar crucero, PTO, precalentamiento, freno motor y segundo puesto de conducción. **El motor sigue funcionando** con el pedal recibido por J1587.
- MID 128 **SID 231 FMI 12 = "Loss of message from the VECU"**: "the EECU has no contact with the VECU"; misma reacción.
- MID 128 **PSID 201 FMI 9** (guías MID 128 posteriores, MEDIA): "MID 144, no communication – abnormal update rate".
- PID 91 FMI 9 + FMI 11 simultáneos → "limp home mode": el régimen lo decide la entrada EB4 (idle validation): <4 V = ralentí, >8 V = acelerado. Volvo no publica el régimen de *limp home* en rpm (NO ENCONTRADO). Para Mack V-MAC III (sistema distinto) un foro cita 900 rpm por defecto (BAJA).
- PID 84 FMI 9+11 (sin velocidad de vehículo) → régimen limitado a 1700 rpm (guía MID 128, MEDIA).
- Volvo CE EC210B: con el interruptor "Auto/Manual" en Manual (bypass de la V-ECU) sólo hay ralentí I2 o alta H y las bombas al ~80 % por banco de resistencias (manual de operador EC210B pp. 71-72, ALTA; foros, BAJA). Códigos CE: ER13-09/11/12 (MID 128 SID 231 FMI 9/11/12) = fallo J1939; ER14 = J1587; MID 187 = V-ECU, MID 140 = I-ECU (Volvo CE UPDATE-EC160B~460B-15, ALTA).
- Volvo CE formación "Electrical System": "In the event of a loss of power in J1939, J1587/J1708 acts as a backup… If both links fail, there is another backup system between VECU and EECU" (= la línea cableada B4) (https://www.scribd.com/document/439922521/Electrical-System, MEDIA, no abierto).

---

## 4. PGN propietarios J1939 y "keep-alive"

- **NO ENCONTRADO** ningún listado público de PGN propietarios (PropA 0xEF00 / PropB 0xFF00-0xFFFF) de la EMS Volvo de primera generación ni de la V-ECU de Volvo CE. Volvo Trucks 2023 sólo publica mensajes estándar "per SAE J1939-71 with exceptions" (ALTA).
- Único indicio: Volvo Penta documenta un PGN propietario "VP Status" (arranque/paro/acelerador) y, en EMS2, VP70 "Accelerator pedal position / Idle speed select" (MEDIA).
- Keep-alive: la EECU vigila el refresco de los mensajes de la VECU (PSID 201 FMI 9 = "abnormal update rate"; SID 231 FMI 9 = "abnormal update rate"). El timeout no se publica; la lámpara se enciende al perder los mensajes y el motor pasa a J1587/limp home. INFERIDO: el emulador debe emitir los mensajes de la V-ECU a su cadencia nominal (TSC1 estándar: 10 ms; mensajes propietarios: típicamente 20-100 ms) tras capturar el tráfico real.
- Foros: "J1939 data link issues are usually related with bad power supply of EECU, VECU or TCU" (https://www.thetruckersreport.com/truckingindustryforum/threads/mid-128-sid-231-fm2-error-code-what-does-it-mean-and-how-to-fix-it.181114/, BAJA).

---

## 5. Ingeniería inversa / reparación / inmovilizador / programación

### 5.1 Hardware interno
- **NO ENCONTRADO** con fiabilidad alta. Indicios (BAJA): página rusa de pinout D12C/D12D (kipdoc.ru, no pudo abrirse; resumen del buscador) cita "procesador 59101520A / 59305837A" (marcado interno, no identifica fabricante), flash **AM29F400 PLCC**, transistor driver de inyectores "L530S" y "CAN decoder A52C251" (= Philips PCA82C251). Taller ruso describe reparaciones con "BGA processor reballing", sustitución de reguladores, MOSFET/IGBT y "BTS drivers", reparación de vías en PCB multicapa, restauración de bootloader y EEPROM (https://auto-elektric.ru/electric-volvo/rem-ecu-fh/, BAJA/MEDIA).
- Volvo (ALTA): memoria de programa flash (SID 240 "Program memory") y memoria de dataset EEPROM (SID 253 "Data set memory EEPROM", checksum erróneo → el motor no arranca); 5 V de sensores por EA4 (SID 232); alimentación de inyectores +90 V (EA12/EA24); la unidad va refrigerada por combustible (serpentín externo desde D12B).
- Fallos típicos (BAJA/MEDIA): sección de alta tensión (90 V) quemada en FH12 1998; supresor de sobretensión "S300" en corto (DRIVE2); no arranca en frío <0 °C porque la ECU no "bootea" (trucksservice.narod.ru); códigos de inyector en los seis cilindros / "resistance too high" por drivers; corrosión; pila/condensador interno (TikTok, BAJA). Reparadores: Autotronics UK (3161962, 20577131), ECM Repair USA, DSL Electronics, ECM Engineering USA, Euro Diesel ECM, td-truck.ru, evoltronic.ru.

### 5.2 Programación y emparejamiento (camión NA)
- Vectro II (ALTA): la **VECU** contiene un dataset único por vehículo (VDA) y no puede intercambiarse sin reprogramar con VCADS Pro (p.69). El procedimiento de sustitución de la EECU (pp. 245-246) es puramente mecánico (desconectar, comprobar fuerza de terminales con 9998482, comprobar sin códigos); el manual no describe emparejamiento EECU↔VECU ni inmovilizador. INFERIDO: en NA 1998-2003 no existe inmovilizador EECU/VECU; sí hace falta cargar software/dataset con VCADS Pro (los vendedores de ECU usadas dicen "must be programmed", BAJA).
- Europa FH12 (BAJA): existe inmovilizador (MID 163 "Immobilizer control unit" en FH versión 2; caja detrás del cuadro); foro ruso: si la ECU donante tiene el inmovilizador activo "el motor no arranca" y hay que reprogramar el VIN; la ECU debe coincidir en motor, freno motor, viscoacoplamiento y tipo de inyectores (https://truck-diagnost.com/viewtopic.php?t=8579, no abierto, resumen de buscador). Autotronics ofrece "FH12 immobiliser transponder recoding" (https://www.autotronics.co.uk/product/volvo-trucks-fh12-immobiliser-transponder-recoding-and-replacement-car-key-service).

### 5.3 Volvo CE (EC210B)
- Volvo CE UPDATE-EC160B~460B-13 "Code Lock (Anti-theft)" (ALTA): el código de 4 dígitos se programa con VCADS Pro y se guarda en la **I-ECU**; al dar llave, la I-ECU pide el código; si la V-ECU falla, la I-ECU "requests EECU to release SHUTDOWN"; con 4 códigos erróneos bloqueo 10 min. Es decir, el antirrobo implica I-ECU/V-ECU/E-ECU vía J1939 ("SHUTDOWN request"), pero es **opcional** (manual de operador EC210B p.58: "The machine can be equipped with theft protection in the form of a code lock… programmed via VCADS Pro"). INFERIDO: sin code lock activado, la E-ECU no exige emparejamiento con la V-ECU.
- Boletín Volvo CE "E-ECU programming update" (Scribd 581311237, no abierto, MEDIA): actualización de software de las E-ECU de excavadoras y cargadoras que "adds a new communication line and software that allows the E-ECU to be reprogrammed with VCADS Pro"; instrucciones para pedir E-ECU nueva o reprogramar según número de serie/fecha. INFERIDO: las E-ECU tempranas (como la de 2002) sólo se programaban en fábrica/EOL (pin B24) y no por VCADS Pro.
- Vendedores: unidades "programmed" por modelo; afirmaciones contradictorias "no programming needed" (BAJA). Manual Volvo CE D12D 2014 (manualslib 1992445, ALTA): el E-ECU se suministra "pre-programmed" o "non-programmed" y se programa con VCADS Pro; se desconectan los conectores "EA and EB".

---

## 6. Identificadores: "VCE56003584", "P03", "E00747373", "80907C"

- **P03**: INFERIDO = revisión de hardware/producción de Volvo. Se ve en 20561256 P03, 20412508 P01, 08170700 P06/P07, 03161952-P01, 20758805-P01, 20814620 P02 (listados de vendedores, BAJA). No hay documento Volvo público que lo defina.
- **VCE56xxxxxx**: INFERIDO = identificador de software/dataset asignado por Volvo CE al programar la unidad (etiqueta de programación con fecha 05.08.02 y motor "D6D EAE2"). Otro ejemplo: V-ECU 14594697 con "VCE56001204 D7D WAE2" (https://machineryline.com/-/sale/control-units/backhoe-loader/Volvo/excavator-ECU-EDC-engine-control-unit-210-BLC-L120E-D6D-Con--17010415043750433400, BAJA). La búsqueda directa de "VCE56" no devuelve documentación Volvo (NO ENCONTRADO). "VCE" es el prefijo WMI de Volvo CE en los PIN de máquina.
- **E00747373**: INFERIDO = número de serie/trazabilidad de la unidad; "EC210 010828 / 10.23.02" = máquina y fecha de programación final en la máquina. **80907C / 00317121 / 2702**: NO ENCONTRADO (probable código de fecha/lote Lucas; "2702" podría ser semana 27 de 2002).
- Volvo Penta DCU muestra "hardware ID, software ID, dataset1 ID, dataset2 ID" como números de pieza separados (manual TAD1241GE, ALTA), coherente con que la etiqueta "VCE56…" sea un ID de dataset/software.

---

## 7. Fuentes adicionales consultadas (no abiertas o sin datos útiles)

- Scribd (bloqueado para lectura automática): 399888990 "Volvo D12 Electrical Wiring Diagram (36-pin ECU connector)"; 582623575 PV776-89130798 "Volvo ECU guide EPA2013"; 439922521 "Electrical System" (formación Volvo CE); 581311237 "E-ECU programming update"; 442981848 "128 PSID 201"; 377827509 "EC210B LC wiring diagram"; 472529957 "EC210B-EC290B Prime manual de serviço"; 262860031 "MID 128 EECU D13A ed.5".
- equipmanual.com "Volvo D12B, D12C, D7C Vectro II ECM Troubleshooting Manual" (de pago, es el mismo PV776-144528).
- JustAnswer (403): hilos sobre pinout ECM D12 2004/2006 — sin datos de pines.
- seetechno.pro "Коды неисправностей EECU": lista pines EA/EB hasta EA56/EB49 — corresponde a la **EMS2** (D12D 2004+/D13, conectores de 62 vías), **no** a la unidad de 36+36; igual que las referencias "EB51/EB55 = J1939" del boletín SB 284-04 D12D y del pinout D16 EPA04. No aplicar al EC210B.

---

## Manuales descargables

Carpeta local: `/home/user/docs/manuales/volvo_trucks_d12/` (96 MB en total, 31 PDF verificados con cabecera %PDF y extraídos con pdftotext). Advertencia: los archivos de pdfmanual4trucks.com / truckmanualshub.com / hhrvresource.com / jimcontent son copias de documentación Volvo con copyright re-alojadas por terceros sin paywall; úsense sólo para referencia técnica. Los de volvotrucks.us, nhtsa.gov, volvoce.com, marinpro.com (Volvo Penta), eatoncummins.com y wincogen.com son publicaciones oficiales o distribuidores.

| Documento | Contenido | Formato / tamaño | Gratis / pago | ¿Abierto? | URL | Ruta local |
|---|---|---|---|---|---|---|
| Volvo Trucks NA, *Vehicle Management System VECTRO II 1998– (D7C, D12B, D12C), PV776-144528, 05.2001* | Pinouts EECU EA/EB (pp.24-27), VECU A/B/C (28-29), esquemas D12B/D12C/D7C/VECU (30-33), enlaces J1939/J1587 (40-48), funciones VECU, códigos MID 128/144, sustitución EECU | PDF 250 p., 4,5 MB | Gratis | Sí (texto y páginas renderizadas) | Visor: https://www.manualslib.com/manual/1921428/Volvo-Tsi.html ; PDF: https://www.pdfmanual4trucks.com/files/sources/truckmanualshub/Volvo%24/Trucks-SM/truckmanualshub.com_Volvo%20TSI%20Vehicle%20Management%20System%20%28VECTRO%20II%2C%20ECU%29%20Service%20Manual.pdf | `Volvo_TSI_Vectro_II_Vehicle_Management_System_PV776-144528.pdf` |
| Volvo CE Customer Support, *UPDATE-EC160B~460B 01…15* (2004) | Arquitectura E-ECU/V-ECU/I-ECU EC-B, "EECU Electric Circuit" EC160B-290B (D6D/D7D) y EC360B/460B (D12) con pines A/B, J1939/J1587, cableado VECU/IECU, Code Lock antirrobo, tabla de códigos ER↔MID/SID | PDF 31 p., 12 MB | Gratis | Sí | https://www.pdfmanual4trucks.com/files/sources/truckmanualshub/Volvo%24/EWD/truckmanualshub.com_Volvo%20EC160B%2C%20180B%2C%20210B%2C%20240B%2C%20290B%2C%20360B%2C%20460B%20Service%20Manual.pdf | `Volvo_EC160B-EC460B_Service_Manual.pdf` |
| Volvo CE, *EC210B Operator's Manual (s/n 14132-)* | Descripción EMS/V-ECU/I-ECU, interruptor Auto/Manual, interruptor de emergencia de régimen, fusibles F13/F15/F24/F25, code lock | PDF 244 p., 6,2 MB (escaneado) | Gratis | Sí | https://www.tractorparts.com/PDFs/VOLVO_EC210B_OPERATIONS_MANUAL.PDF ; visor alternativo https://www.manualslib.com/manual/1664987/Volvo-Ec210b.html | `Volvo_EC210B_Operators_Manual_sn14132-.pdf` |
| Volvo CE, *L120E Electrical System – esquemas Sch01-Sch100 (2002)* | Sch02 alimentación E-ECU/I-ECU/V-ECU, Sch24/31 comunicación ECU J1939/J1708, Sch28/29 sensores E-ECU (pines EA/EB), Sch30 inyectores | PDF 38 p., 0,8 MB | Gratis | Sí | https://www.pdfmanual4trucks.com/files/sources/truckmanualshub/Volvo%24/EWD/truckmanualshub.com_VOLVO%20L120E%20Electrical%20Schematic%20Diagram.pdf | `Volvo_L120E_Electrical_Schematic_Diagram.pdf` |
| Volvo Trucks NA, *SB 371-44 Data links, fault tracing (12.2004)* | Topología J1939/J1587 VN/VHD, terminador dentro de la EECU, comprobaciones de resistencia (60/120 Ω) | PDF 25 p., 0,7 MB | Gratis | Sí | https://truckmanualshub.com/files/17c0db8abc610a66607b4c50cedf08093e64d8fb860fd6c940249e67f43372ec.pdf | `Volvo_J1939_J1708_Datalink_Fault_Tracing.pdf` |
| Volvo Trucks NA, *Service Manual Group 37 Electrical Schematic VN, VHD Version 2 (PV776-20040447, 12.2004)* | Esquemas de chasis VN/VHD V2 (motores Cummins ISX/Volvo); útil para VECU, buses | PDF 208 p., 4,9 MB | Gratis | Sí (sin tabla EECU D12 en texto) | https://hhrvresource.com/sites/default/files/dfiles/PV776-20040447_ElectricalSchematic_V2_1204.pdf | `Volvo_VN_VHD_V2_Electrical_Schematic_PV776-20040447_2004-12.pdf` |
| Volvo Trucks NA, *Group 37 Electrical Schematic VN, VHD V2, VT (PV776-20175317, 06.2005)* | Ídem, edición 06.2005 | PDF 128 p., 2,9 MB | Gratis | Sí | https://hhrvresource.com/sites/default/files/dfiles/PV776-20175317_ElectricalSchematic_V2_0605.pdf | `Volvo_VN_VHD_VT_V2_Electrical_Schematic_PV776-20175317_2005-06.pdf` |
| Volvo Truck Corp., *Wiring diagram FH12, FH16 LHD, Group 37 Version 01 (TSP119544, 09.1998)* | Esquemas FH12 1998 (EECU D12C "Engine ECU, fuel injection, preheating" hoja BL p.9; conectores; componentes) | PDF 128 p., 3,7 MB | Gratis | Sí | https://www.pdfmanual4trucks.com/files/jimdo-recovery-v1/8252730915/89ff4640990ac215d235ac30323d58af0b4b958fc0919125dc2e62c9ae674b77.pdf | `Volvo_FH12_FH16_Electrical_Wiring_Diagrams_Service_Manual.pdf` |
| Volvo Truck Corp., *Wiring diagram FH12/FH16 RHD (11.1998)* | Ídem RHD | PDF 114 p., 3,2 MB | Gratis | Sí | https://www.pdfmanual4trucks.com/files/jimdo-recovery-v1/8252731815/d31fb13b534411579a18b77af06f765d3524654dbc417557799bebab25215192.pdf | `Volvo_FH12_FH16_RHD_Wiring_Diagrams.pdf` |
| Volvo, *D12, D12A, D12B Engines Workshop Manual* | Manual de taller completo D12A/B (709 p.), descripción EECU, EUI, relés de alimentación EECU | PDF 709 p., 18 MB | Gratis | Sí | https://www.pdfmanual4trucks.com/files/sources/truckmanualshub/Volvo%24/Engine/truckmanualshub.com_Volvo%20D12%2C%20D12A%20and%20D12B%20engines%20Workshop%20Manual%20PDF.pdf | `Volvo_D12_D12A_D12B_Engines_Workshop_Manual.pdf` |
| Volvo Trucks NA, *Service Manual Group 250-600 Intake and Exhaust System D12, D12A, D12B, D12C (PV776-TSP144524, 2001)* | Sistema admisión/escape, EPG controlado por la EECU | PDF 48 p., 0,7 MB | Gratis | Sí | https://www.pdfmanual4trucks.com/files/sources/truckmanualshub/Volvo%24/Engine/truckmanualshub.com_Volvo%20D12%2C%20D12A%2C%20D12B%2C%20D12C%20Service%20Manual.pdf | `Volvo_D12_D12A_D12B_D12C_Service_Manual.pdf` |
| Volvo Trucks NA, *Operator's Manual Maintenance and Engine VHD (PV776-TSP20154789, 2004)* | Manual de operador (mantenimiento, motor) | PDF 214 p., 1,4 MB | Gratis | Sí (poco relevante) | https://www.pdfmanual4trucks.com/files/sources/truckmanualshub/Volvo%24/Engine/truckmanualshub.com_Volvo%20D7%2C%20D12%20Engines%20Service%20Manual.pdf | `Volvo_D7_D12_Engines_Service_Manual.pdf` |
| *Volvo D12A Fault Codes* (FH12 D12A, 2007 compilación) | Códigos MID 128 D12A | PDF 40 p., 1 MB | Gratis | Sí | https://www.pdfmanual4trucks.com/files/jimdo-recovery-v1/8252729815/4820e2e7ad797397f712b6d1d298ba0e8eaa9aaab2ebad1a9c048fae833abcf3.pdf | `Volvo_D12A_Fault_Codes.pdf` |
| *MID 128 fault code guide – EECU* (compilación 2018) | PID/PPID/SID/PSID MID 128 incl. PSID 201 | PDF 20 p., 0,2 MB | Gratis | Sí | https://truckmanualshub.com/files/2fa81d65ae20d8b8c2ae1321cfbd73465d30e5c6602f8a559c9fb5eccc643bad.pdf | `Volvo_MID128_EECU_Fault_Code_Guide.pdf` |
| Volvo Trucks NA, *VN, VHD V2, VT – MID 128 Fault Code Guide (2008)* | Códigos MID 128 (EMS2 D11/D13/D16) | PDF 54 p., 0,15 MB | Gratis | Sí | https://truckmanualshub.com/files/c20f9a090588ec103e2d7a655f95aeb942d9b696e3df1d2f04a78f64557c76ae.pdf | `Volvo_VN_VHD_V2_VT_MID128_Fault_Code_Guide.pdf` |
| Volvo Trucks, *Manual de Servicio Grupo 36 Ed.04 – Códigos de error VECU MID 144 VERSION2 (20 025488, 09.2005)* | MID 144 FH/FM versión 2 (en español) incl. PPID 74 alimentación EECU/VECU | PDF 174 p., 1,1 MB | Gratis | Sí | https://truckmanualshub.com/files/ea48aafb6adb771c7ee6f804816ea1f6c7d48a42ccef9f98018b99aeb74adb59.pdf | `Volvo_MID144_VECU_Codigos_Error_ES.pdf` |
| *Volvo FH12 D12A fault codes* (4 p.) | Resumen códigos | PDF 4 p. | Gratis | Sí | https://truckmanualshub.com/files/472bd2037bfe76f4f952964ca7a2cb4c90c48913e35a2d303d1644af4f0fca86.pdf | `Volvo_FH12_D12A_Fault_Codes_truckmanualshub.pdf` |
| Volvo Trucks NA, *VHD2, VN, VT Service Manual (2007)* | Manual de servicio general | PDF 130 p., 0,3 MB | Gratis | Sí | https://www.pdfmanual4trucks.com/files/sources/truckmanualshub/Volvo%24/VN-VHD/truckmanualshub.com_Volvo%20VHD%202%2CVN%2CVT%20Manual.pdf | `Volvo_VHD2_VN_VT_Service_Manual.pdf` |
| Volvo CE, *A35D/A40D folleto técnico (2003)* | Motor D12C ADE2/AAE2, VEB | PDF 8 p. | Gratis | Sí (sin pinout) | https://www.pdfmanual4trucks.com/files/sources/truckmanualshub/Volvo%24/ArticulatedDumpTrucks/truckmanualshub.com_Volvo%20A35_A40D.pdf | `Volvo_A35D_A40D_Manual.pdf` |
| Volvo Trucks NA, *Body Builder Instructions VN/VHD/VAH Section 3 Electrical, ECU (USA170229709, 04.2023)* | Mensajes J1939 Volvo (SA 0x11 VECU), BBM, BB_BUS_CONTROL/TSC1, conector carrocero | PDF 166 p., 8,4 MB | Gratis | Sí | https://www.volvotrucks.us/media/vtna/files/shared/body-builder/manuals/2023/maint-1567837-volvo-section-3-vecu4-updates.pdf | `Volvo_VTNA_BodyBuilder_Sec3_Electrical_VECU4_2023.pdf` |
| Volvo Trucks NA, *Body Builder Instructions Section 9 PTO (VEC4, 2023)* | Control de régimen PTO por VECU/J1939 | PDF 124 p., 7,4 MB | Gratis | Sí | https://www.volvotrucks.us/media/vtna/files/shared/body-builder/manuals/2023/volvo-section-9-vec4-final.pdf | `Volvo_VTNA_BodyBuilder_Sec9_PTO_VEC4_2023.pdf` |
| Volvo Truck Corporation (Europa), *Body builder instructions – Power take-off (2018)* | PTO, petición de régimen, límites | PDF 50 p., 3,6 MB | Gratis | Sí | https://shop1523.hstatic.dk/upload_dir/pics/jo_hydraulics/VOLVO-PTO-Options.pdf | `Volvo_VTC_BodyBuilder_PTO_Options_Europe.pdf` |
| Volvo Trucks NA, *Electrical wiring diagrams (índice/diagramas VN 2017, D-17138-93)* | Esquemas VN modernos (EMS2/EMS3, VECU, BBM) | PDF 147 p., 7,7 MB | Gratis | Sí | https://s7abe6bda7f063e33.jimcontent.com/download/version/1669716763/module/13250381649/name/Volvo%20Trucks%20Electric%20Wiring%20Diagrams.pdf | `Volvo_Trucks_Electric_Wiring_Diagrams_jimcontent.pdf` |
| Volvo Penta, *Marine engines D9/D13/D16 EMS – OpenCAN install guideline / Engine control interface (47706587, 05.2015)* | SA (0x00 EMS, 0x03 TECU, 0x11 OEM, 0xE6 BBM), TSC1, VP70, conector 8 pines | PDF 36 p., 1,3 MB | Gratis | Sí | https://www.marinpro.com/Cms_Data/Contents/powerhouse/Folders/Accessories/AccessoryFiles/~contents/4YD2DR3WYE3MEBNA/OpenCAN_InstallGuideline_rev_1.pdf | `Volvo_Penta_Marine_EMS_OpenCAN_Install_Guideline.pdf` |
| Volvo Penta, *Operator's manual Generating set & industrial engines 12 liter (EDC III) TAD1240-1242GE/VE, TWD1240VE* | Descripción EDC III/EMS D12, CIU, DCU, IDs de hardware/software/dataset | PDF 76 p., 2,9 MB | Gratis | Sí | https://www.wincogen.com/wp-content/uploads/PD/Engines/volvo_tad1241ge_opm.pdf | `Volvo_Penta_TAD1240-1242GE_EDCIII_Operators_Manual.pdf` |
| Volvo CE, *EC210B LC/NLC spec sheet D6D EAE2 (22C4351641, 09.2004)* | Datos máquina | PDF 12 p., 0,4 MB | Gratis | Sí | https://www.volvoce.com/-/media/volvoce/global-site/products-and-services/past-products/documents/07-crawler-excavators/04-volvo-b-prime-series/v-ec210b/v-ec210b-d6d-eae2-22c4351641-2004-09.pdf?v=Gn1HPw | `Volvo_CE_EC210B_Spec_Sheet_2004.pdf` |
| Volvo Trucks NA TSB, *Volvo Chassis – Data Link Diagnostics (NHTSA MC-10125875, 2017)* | Diagnóstico J1939 moderno | PDF 6 p. | Gratis | Sí | https://static.nhtsa.gov/odi/tsbs/2017/MC-10125875-9999.pdf | `Volvo_TSB_DataLink_Diagnostics_NHTSA_MC-10125875.pdf` |
| Volvo/Mack TSB, *SS 1033423 J1939 Fault Code Source Address, SPN (NHTSA MC-10141869, 2018)* | Tabla SA/SPN J1939 | PDF 394 p., 1,2 MB | Gratis | Sí | https://static.nhtsa.gov/odi/tsbs/2018/MC-10141869-9999.pdf | `Volvo_TSB_J1939_SourceAddress_NHTSA_MC-10141869.pdf` |
| Eaton, *TRIG0910 Volvo/Mack BBM & engine configuration (2015)* | Ajustes BBM Volvo, SA 239 multiplex | PDF 32 p., 0,4 MB | Gratis | Sí | https://www.eatoncummins.com/content/dam/eaton-cummins/products/ultrashiftplus/ecjv-automated-transmission-engine-configuration-settings-guide-trig0910-en-us.pdf | `Eaton_TRIG0910_Volvo_Mack_BBM_Engine_Config.pdf` |
| Volvo Reman, *Technical Application Guide (2021)* | Catálogo reman (sin ECU D12) | PDF 49 p., 1,3 MB | Gratis | Sí (irrelevante) | https://www.bergeystruckcenters.com/efs/wp/domains/www.bergeystruckcenters.com/wp-content/uploads/2021/09/Volvo-Reman-Technical-Application-Guide_compressed-1.pdf | `Volvo_Reman_Technical_Application_Guide.pdf` |

**Encontrados pero no descargados (bloqueados, de pago o sin descarga directa):**

| Documento | Contenido | Formato | Gratis/pago | ¿Abierto? | URL |
|---|---|---|---|---|---|
| Volvo CE, *Engine control unit D12 E-ECU, A40D Service Manual* | E-ECU D12 Volvo CE (inyectores Bosch/Delphi) | Slideshare | Gratis (visor) | No (bloqueo) | https://www.slideshare.net/slideshow/volvo-a40d-engine-control-unit-d12-e-ecu-service-manual-pdf/275267853 |
| Volvo CE formación *Electrical System* (E-ECU/V-ECU/I-ECU, backup J1587, terminador en E-ECU) | Handout formación | Scribd | Gratis (visor) | No | https://www.scribd.com/document/439922521/Electrical-System |
| *Volvo D12 Electrical Wiring Diagram – 36-pin ECU connector* | Pinout 36 pines D12 (tercero) | Scribd | Gratis (visor) | No | https://www.scribd.com/document/399888990/Wiring-Diagrams |
| Volvo CE boletín *E-ECU Programming Update* | Línea de comunicación para reprogramar E-ECU con VCADS Pro | Scribd | Gratis (visor) | No | https://www.scribd.com/document/581311237/128sid231 |
| Volvo Trucks NA SB 284-04 *Engine ECU D12D fault tracing (2004)* | Pines EB51/EB55 J1939, EA33/EA34 J1587 (EMS2, no aplica a 36 pines) | pdfcoffee | Gratis (visor) | No (403) | https://pdfcoffee.com/volvo-ecu-d12dpdf-5-pdf-free.html |
| Volvo CE, *EC210B LC wiring diagram* (rangos s/n) | Esquema EC210B | Scribd | Gratis (visor) | No | https://www.scribd.com/document/377827509/1 |
| Volvo CE, *EC210B-EC290B Prime Manual de serviço (PT)* | Manual de servicio completo | Scribd | Gratis (visor) | No | https://www.scribd.com/document/472529957/ESCAVADEIRA-VOLVO-EC210B-EC290B-Prime-Manual-servic-o-1-pdf |
| Volvo Penta, *TAD1240-1242 EDC III Workshop Manual Group 23* | ECU EDC III, esquemas pp.66-69 | Scribd/pdfcoffee/heydownloads | Gratis (visor) / pago | No | https://www.scribd.com/document/748763822/Volvo-Penta-TAD1240-1242-Workshop-Manual ; https://pdfcoffee.com/workshop-manual-volvo-twd1240-pdf-free.html |
| Volvo Penta, *Electrical Interface Specification EMS2.3 (47706487)* | TSC1, SA, VP70 | pdfcoffee/kupdf | Gratis (visor) | No | https://pdfcoffee.com/electrical-interface-specification-ems2347706487en-pdf-free.html |
| Volvo Trucks NA, *VN/VHD US07 schematics*, *MID 144 DTC guide*, *PV776-20014399 Group 37* | Esquemas y códigos | class8truckparts.com | Gratis | No (Cloudflare) | https://class8truckparts.com/media/file/vn-vhd-us07-schmatics-volvo.pdf ; https://class8truckparts.com/media/file/volvo-truck-mid144-dtc-guide.pdf ; https://class8truckparts.com/media/file/PV776-20014399.pdf |
| Volvo CE, *D12D Service Information (A35E), 2014* | E-ECU MID 128, sustitución (EMS2) | manualslib | Gratis (visor) | Sí (visor) | https://www.manualslib.com/manual/1992445/Volvo-D12d.html |
| MDJC, *Manual Error Codes EECU D6B/D7C/D10B/D12C/D16B (ES, 144 p.)* | Códigos MID 128 en español | PDF | Pago 10,89 USD | No | https://mdjc-manuals.com/downloads/manual-error-codes-eecu-volvo-d6b-d7c-d10b-d12c-d16b-engines-2/ |
| equipmanual.com *Volvo D12B/D12C/D7C Vectro II ECM Troubleshooting Manual* | = PV776-144528 | PDF | Pago | No | https://equipmanual.com/dl/volvo-d12b-d12c-d7c-vectro-ii-ecm-troubleshooting-manual/ |
| volvo-club.cz *2003 Volvo FH D12/D12A/D12B workshop manual (17,6 MB)* | Manual de taller | PDF | Gratis con registro | No (login) | https://en.volvo-club.cz/manual_download.php?id=1942 |
| pdfmanual4trucks *Volvo VN VHD Service & Repair Manual 08.1996-11.2002* | Colección completa VN/VHD de la época D12 | RAR 309 MB | Gratis | No descargado (>100 MB) | https://www.pdfmanual4trucks.com/files/Volvo/Volvo%20VN%20VHD%20Trucks%20Service%20%26%20Repair%20Manual%20From%20Aug%201996-Nov%202002%20%5BRAR%2C%20ENG%2C%20316%20MB%5D.rar |

---

## Esquemas extraídos

Carpeta: `/home/user/docs/esquemas/` (ficheros con prefijo `d12_`, PNG a 150 dpi, 130-400 kB cada uno). En la misma carpeta existían ya ficheros con prefijo `ce_` (L120E Sch01-30, EC210B manual de operador, Scribd thumbnails) generados por otro proceso; no se han tocado.

| Fichero | Fuente | Qué muestra |
|---|---|---|
| `d12_VectroII_EECU_connector_EA_pinout_D12B-C-024.png` | PV776-144528 p.24 | Tabla pinout EECU conector EA (lado motor) D12B/D12C, 36 cavidades, colores de cable |
| `d12_VectroII_EECU_connector_EB_pinout_D12B-C-025.png` | PV776-144528 p.25 | Tabla pinout EECU conector EB: J1939 (1,2), J1708 (25,26), masa (9,10), +bat (11,12), idle validation (4), EOL (24), EPG, precalentamiento |
| `d12_VectroII_EECU_connector_EA_pinout_D7C-026.png` / `..._EB_pinout_D7C-027.png` | PV776-144528 pp.26-27 | Mismo hardware en motor D7C (bomba en línea): EB idéntico, EA distinto |
| `d12_VectroII_VECU_connector_A_pinout-028.png` | PV776-144528 p.28 | VECU conector A: crucero/PTO, idle validation, llave, alimentación |
| `d12_VectroII_VECU_connector_B_C_pinout-029.png` | PV776-144528 p.29 | VECU conector B (pedal TPS, idle validation hacia EECU) y C (J1708 400/401, J1939 406/407/408) |
| `d12_VectroII_schematic_D12B_EECU-030.png` | PV776-144528 p.30 | Esquema eléctrico EECU D12B con sensores/inyectores/buses |
| `d12_VectroII_schematic_D12C_EECU-031.png` | PV776-144528 p.31 | Esquema eléctrico EECU D12C |
| `d12_VectroII_schematic_VECU-033.png` | PV776-144528 p.33 | Esquema VECU (entradas, buses hacia EECU) |
| `d12_VectroII_datalink_system_overview-040.png` | PV776-144528 p.40 | Visión general de enlaces J1939/J1587 VECU–EECU–cuadro–diagnóstico |
| `d12_VectroII_J1939_network_terminating_resistors-047.png` | PV776-144528 p.47 | Red J1939 con MIDs (128 EECU, 144 VECU, 130, 136, 232, 234/140) y terminadores (uno dentro de la EECU) |
| `d12_VectroII_EECU_breakout_pin_signals-018/019/020.png` | PV776-144528 pp.18-20 | Tablas de señal/valor esperado por pin EA/EB con caja de medición |
| `d12_EC210B_EECU_electric_circuit_EC160B-290B-07.png` | Volvo CE UPDATE-EC160B~460B-05-1 (PDF EC-B p.7) | **Circuito E-ECU EC210B (D6D)**: Connector A (sensores/inyectores) y Connector B (4 emergency speed, 1/2 J1939 H/L, 25/26 J1708 A/B, 9/10 GND, 11/12 24 V, 7/17/8/3/13 sensores, 31 relé precalentamiento) |
| `d12_EC360B_460B_EECU_electric_circuit-08.png` | UPDATE-EC160B~460B-05-2 (p.8) | Circuito E-ECU EC360B/460B (D12): mismo conector B, inyectores 6 cil. |
| `d12_EC-B_series_system_layout_EECU_VECU_IECU-02.png` | UPDATE-EC160B~460B-01 (p.2) | Cambio de arquitectura: sensores → E-ECU, línea de comunicación hacia V-ECU/I-ECU |
| `d12_EC-B_series_control_system_overview_J1939_J1587-04.png` | UPDATE-EC160B~460B-03 (p.4) | EMS(E-ECU) MID128 – VECU MID187 – IECU MID140 por J1939/J1587; VCADS Pro |
| `d12_EC-B_series_VECU_IECU_J1939_J1587_wiring-10.png` | UPDATE-EC160B~460B-05/07 (p.10) | Cableado V-ECU/I-ECU con J1939 H/L y J1587 A/B |
| `d12_EC-B_series_code_lock_antitheft_IECU_VECU_EECU-17.png` | UPDATE-EC160B~460B-13 (p.17) | Flujo Code Lock: I-ECU/V-ECU/EECU "SHUTDOWN request/release" |
| `d12_EC-B_series_J1939_J1587_fault_codes_ER13_ER14-19.png` | UPDATE-EC160B~460B-15 (p.19) | Tabla ER13/ER14 ↔ MID 128/187 SID 231/250 |
| `d12_VN_J1939_datalink_layout_terminating_resistors_SB371-44-08.png` | SB 371-44 (12.2004) p.8 | Topología J1939 VN: backbone, terminadores, EECU |
| `d12_VN_J1939_terminating_resistor_check_SB371-44-13.png` | SB 371-44 p.13 | Comprobación terminadores (120 Ω cada uno; 60 Ω total; uno dentro de la EECU) |

Imágenes web directas (JPG/PNG) de la EECU D12: no se encontró ninguna imagen de esquema de libre acceso aparte de las contenidas en los PDF anteriores; las de Scribd/Slideshare no pudieron descargarse (bloqueo).

---

## Recomendaciones prácticas para el emulador ESP32 (derivadas de lo anterior)

1. Cablear el ESP32 al conector B de la E-ECU: CAN H/L en B1/B2 (añadir terminador de 120 Ω en el lado emulador si se elimina la V-ECU; la E-ECU ya lleva uno interno), J1708 en B25/B26 opcional (respaldo y PID 91 por J1587), alimentar B11/B12 por el relé EMS y masa B9/B10.
2. Antes de emitir, capturar con la V-ECU original el tráfico J1939 completo (incluye PGN propietarios y cadencias); identificar la SA de la V-ECU (probable 0x11, MID 187 en Volvo CE) y los mensajes periódicos cuya ausencia dispara MID 128 PSID 201 / SID 231 FMI 12.
3. Probar TSC1 (PGN 0, destino 0x00) desde SA 0x03/0x11/0xE6 con "speed control" si el mensaje propietario no se descifra; la generación Penta del mismo hardware lo acepta.
4. Mantener la línea B4 ("Emergency speed control" / idle validation) como respaldo cableado: permite ralentí/alta sin bus.
5. Comprobar si la máquina tiene el Code Lock activado (I-ECU); si lo está, la E-ECU puede recibir una petición de SHUTDOWN por J1939 al no validarse el código.
