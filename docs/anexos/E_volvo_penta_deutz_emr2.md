# Investigación: Volvo Penta EMS / TAD-VE como fuente de documentación para la E-ECU del Volvo D6D EAE2 (EC210B, 2002)

Fecha: 2026-10-19. Fiabilidad: **ALTA** = documento oficial Volvo Penta / Volvo; **MEDIA** = documento técnico de fabricante tercero (ComAp, DEIF…) o copia de manual oficial en sitio tercero (manualslib, krutilvertel…); **BAJA** = foro / vendedor / blog.
Convención de estado: **[CONFIRMADO]** texto leído en la fuente; **[INFERIDO]** deducción razonada; **[NO ENCONTRADO]** se buscó y no apareció.

> Nota: el presupuesto de búsquedas web de esta sesión se agotó (200 búsquedas). Quedaron sin cubrir algunos puntos (ver §9); se pueden continuar en un mensaje posterior.

---

## 0. Hallazgo crítico sobre la premisa (lea esto primero)

**La premisa "TAD650VE/660VE/750VE/760VE = D6D/D7D con la misma ECU que la E-ECU 03161983/20577135" NO se sostiene con la documentación encontrada.**

1. **[CONFIRMADO, ALTA]** El manual de taller oficial *Group 30 Electrical system – Industrial Engines TAD734GE, TAD650VE, TAD660VE, TAD750VE, TAD760VE* (pub. **7747632**, inglés, 03-2007) describe para los TAD650/660/750/760VE un sistema **EMS 2** con **inyección common rail**: "Solenoid controlled proportional valve, high pressure pump – fuel (MPROP)", "Fuel pressure in common rail", "Glow plugs, one for each injector", "Injector common rail #1-6 (SID 1-6)", "Rail pressure (PID 164)", "Rail pressure release valve (PSID 97)", "Internal EGR (PPID 19)". Es decir, son motores base **Volvo D6E/D7E (Deutz TCD 2013 4V common rail, Stage IIIA)**, no el D6D EAE2 de bomba-inyector unitaria (unit pump) de 2002.
   Fuente (demo oficial del manual, 15 pág.): https://krutilvertel.com/pdf/demo/motorist/rukovodstvo-po-remontu-dvigatelja-volvo-tad734ge-demo.pdf ; copia completa (160 pág.) visible en manualslib: https://www.manualslib.com/manual/3858599/Volvo-Tad750ve.html
2. **[CONFIRMADO, MEDIA]** En la hoja de fallos PSID 201 de ese manual, los pines de la unidad EMS 2 son "CAN H-datalink to engine: **B51**, CAN L: **B55**, Ignition: **A58**, Stop: **A27**, J1708A: **A34**, J1708B: **A33**" (https://www.manualslib.com/manual/3858599/Volvo-Tad750ve.html?page=143). Pines numerados > 36 ⇒ los conectores de esa ECU **no son 2×36 pines**; es coherente con una ECU tipo **Bosch EDC7** (conectores de 36 + 89 pines) **[INFERIDO]**.
3. **[BAJA, vendedores]** La ECU **60100001** se vende para TAD650VE/660VE/750VE/760VE/TAD734GE/TAD751GE y "D7E240" (eBay 204445297650, 266220156756, made-in-china 1932911642). La ECU **60100002** se vende como equivalente de **20577135 = VOE03161983** para D6D en EC210B/EC240B/EC290B/L90E-L120E (eBay 387350498892: "ECU Control Unit 20577135 60100002 For Volvo EC210B"; sinocmp.com/products/voe-60100002-volvo-ec210blc-ec210b-ecu). **[INFERIDO]** 60100001 y 60100002 son números consecutivos del catálogo, pero corresponden a hardware distinto (EDC7 common rail vs. ECU D6D unit-pump). Ningún documento confirma que 60100000/60100001 sea la misma caja que 20577135.
4. **¿Cuál es la familia Volvo Penta que SÍ comparte hardware con la E-ECU del D6D?** Dos candidatas:
   - **(A) Volvo Penta "EDC III" / EMS de 1ª generación (D12): TAD1240GE, TAD1241GE/VE, TAD1242GE/VE, TWD1240VE**, ECU **20577134** (= 20582963) [BAJA: fridayparts, Amazon B0F3W8XM68]. La numeración 20577134 (D12 Penta) / 20577135 (D6D/D7D CE) y VOE3161962 (D12D CE) / VOE3161983 (D6D CE) es consecutiva **[INFERIDO]**. Esta ECU D12 tiene **dos conectores de 36 pines** ("red connector"/"black connector" en el manual Penta; "36-Pin ECU Connector A/B" en el diagrama D12 de camión). Los pines de inyector del conector negro (11, 23, 35 = cil. 1, 3, 5 en el manual Penta) coinciden con el conector A del D12 de camión (11/22/23/34/35/36 = INJ 1-6) **[CONFIRMADO en ambas fuentes, MEDIA]**. Esta es, con mucho, la documentación pública más parecida a la E-ECU del D6D, y además está en inglés y gratis en manualslib (ver §1).
   - **(B) Volvo Penta "EDC4" (TAD520/620/720/721/722 GE/VE, TD420-720)**, ECU **20700665** [BAJA: fridayparts]. Según ComAp, **"EDC4 (EMR2)"** = Deutz **EMR2** (ECU Bosch para Deutz) con conector de vehículo **25 pines** ("ECU 25pin F connector": CAN H pin 12, CAN L pin 13, Bat+ 14, Bat– 1) **[CONFIRMADO, MEDIA]**. Son los mismos motores base Deutz 2012/2013 unit-pump que el D6D/D7D, pero **otra ECU**. Nota de prensa Volvo Penta 2003: EDC 4 "en dos variantes: una para CAN J1939 y otra con potenciómetro tradicional" (https://www.volvogroup.com/en/news-and-media/news/2003/may/news-20664.html, ALTA).
   - **[NO CONFIRMADO]** La atribución "desarrollada con LucasVarity" no se pudo verificar en ninguna fuente (Lucas/Delphi sí fue el proveedor de los inyectores EUI del D12C). Develco afirma haber desarrollado electrónica de una ECU para Volvo CE (https://develco.com/cases/volvo/), sin número de parte.

**Conclusión práctica:** para el proyecto ESP32↔E-ECU D6D conviene usar (i) el *Installation Manual EDC III TAD1240-42GE/TWD1240VE* y el *Operator's Manual TAD1240GE* (interfaz CIU/standalone, parámetros, códigos), (ii) la especificación oficial de interfaz CAN Volvo Penta EMS (mensaje propietario **VP70 "VP Status"** y reglas TSC1) como referencia del *estilo* de mensajería Volvo, y (iii) las guías ComAp/DEIF como confirmación independiente de qué se envía por CAN. Nada de esto sustituye una captura CAN real del EC210B: los PGN propietarios de la V-ECU de Volvo CE **no están publicados**.

---

## 1. Manuales Volvo Penta encontrados (instalación / taller / datos técnicos / eléctrico)

### 1.1 TAD650VE / TAD660VE / TAD750VE / TAD760VE (+TAD734GE) — EMS 2 (common rail)
- **Workshop Manual Group 30 Electrical system, pub. 7747632 (03-2007), 160 pág.** — ALTA (oficial) / copia en manualslib (MEDIA).
  - Índice relevante (pág. impresas): EMS 2 descripción 8; CAN 8; CIU 9; DCU 9; Diagnóstico 10; ubicación componentes 11; "Engine control unit EMS 2" 18; soldadura eléctrica 20; cambio/reprogramación ECU 21-23 (VODIA, MID 128 y MID 144); fallos en cables de bus 33; códigos MID 128 34-143; protección motor 144-145; **esquemas**: "Wiring diagram EMS 2: Vehicle harness TAD650-760VE" 146, "Engine harness TAD650-760VE" 147, "Engine harness TAD734GE" 148, "Wiring diagram DCU" 149, "Wiring diagram CIU" 150; datos técnicos 151.
  - URL visualización: https://www.manualslib.com/manual/3858599/Volvo-Tad750ve.html (pág. del visor = pág. impresa + 2). Los esquemas son imágenes; manualslib está detrás de Cloudflare → no fue posible descargarlos (ver §8).
  - Demo oficial gratuita (15 pág., incluye índice, herramientas, ubicación de componentes, protección de motor e índice SPN): https://krutilvertel.com/pdf/demo/motorist/rukovodstvo-po-remontu-dvigatelja-volvo-tad734ge-demo.pdf → descargado.
  - Otras copias (no verificadas/pago): https://en.volvo-club.cz/manual_download.php?id=1976 (devuelve HTML, requiere login); https://pdfcoffee.com/workshop-manual-gp30-volvo-penta-tad760ve-pdf-pdf-free.html (403); https://manualmachine.com/volvo/tad650ve/4535000-service-manual/ (403); https://issuu.com/heydownloads/docs/volvo_penta_tad650ve_tad660ve_tad734ge_tad750ve/s/14035911 (404); obdtotal/sellfy (pago).
- **Contenido eléctrico confirmado [CONFIRMADO, ALTA/MEDIA]:**
  - "EMS 2 is an electronic system with CAN communication… The J1939 CAN link is responsible for all communication between the engine control unit (EMS 2) and CIU/DCU… Diagnostics are managed by the J1708/J1587 link." **Si falla el CAN, el potenciómetro de régimen y los pulsadores arranque/paro pasan por J1708/J1587** (instrumentos y lámparas se apagan). **Si fallan ambos enlaces, el motor va a ralentí y sólo se puede parar con el AUX-STOP.** (visor pág. 10).
  - CIU: enlace CAN 250 kbit/s ("fast") + J1708/J1587 ("slow", diagnóstico/flash codes). DCU: panel digital por CAN; parámetros ajustables desde DCU: **ralentí, límites de alarma temperatura aceite/refrigerante, droop, precalentamiento al dar llave** (visor pág. 11).
  - Comprobación bus CAN: resistencia entre pines **1-2 del conector Deutsch 8 pines en DCU** o **11-12 en CIU** ≈ **60 Ω**; tensión ≈ 2,3-2,7 V (visor pág. 130). Terminación **120 Ω** como componente externo (ítem 26 en esquema CIU, ítem 10 en esquema DCU) ⇒ la ECU EMS 2 lleva la otra terminación integrada **[INFERIDO]**; la espec. marina lo dice explícitamente ("The EMS has built-in terminations").
  - Esquema CIU (leyenda, visor pág. 152): llave 15+, **potenciómetro rpm**, tacómetro, instrumentos, **contacto de ralentí (2 vías)**, **interruptor 1500/1800 rpm**, pulsador arranque, pulsador paro, pulsador diagnóstico, lámparas de alarma, lámpara diagnóstico, bocina, indicación marcha, indicación/contacto precalentamiento, **contacto governor (droop)**, contacto override protección, dos conectores 8 pines interfaz motor, bloque Easy Link, **resistencia terminación 120 Ω**. Cable 0,75 mm² salvo indicación.
  - Protección motor TAD650-760VE (tabla "Derate to engine protection map", pág. 144): derate por T refrigerante 98/101/106 °C, T boost 80/83/90 °C, P boost 340/350/355 kPa, P aceite; "Forced to idle after 5 s", "Forced shutdown after 15 s".
  - **Datos de pines de la ECU** (power/ground/CAN/J1587/entradas analógicas de la unidad EMS 2 de 36+N pines): **sólo** lo indicado en §0.2 (A27, A33, A34, A58, B51, B55). El resto está en las imágenes de los esquemas 146-147, no legibles como texto **[NO ENCONTRADO en texto]**.
- **Hoja de datos TAD734GE 47709301** (oficial, 2 pág.): https://cdn.wajax.com/wp-content/uploads/2018/02/47709301_EN.pdf → descargado. (pubs.volvopenta.com devolvió 503.)
- Catálogo TAD650VE (directindustry): "Fully electronic with Volvo Penta EMS II, both CAN-bus & Stand Alone Interface (optional)", "common rail injection system", Tier 3 / Stage IIIA (https://pdf.directindustry.com/pdf/volvo-penta/tad650ve/34254-343245.html, 403 al abrir; MEDIA por resumen de búsqueda).

### 1.2 TAD1240GE / TAD1241GE-VE / TAD1242GE-VE / TWD1240VE — EDC III (= "EMS 1"), ECU 20577134, 2×36 pines
- **Installation Manual (88 pág.)** — oficial, copia manualslib (MEDIA): https://www.manualslib.com/manual/4542784/Volvo-Penta-Tad1240ge.html . Índice: EDC III (7), Control unit (7), System voltage 24 V (10), **TAD1240-42GE Standalone** (11-20: conexión, arranque/paro, lámparas, conector diagnóstico, sincronización, **esquema** 18, parámetros 19-20), **TAD1240-42GE CIU** (21-33, esquema 31), **TWD1240VE Standalone** (34-44: **pedal acelerador** 36, esquema 41, parámetros 42-44), **TWD1240VE CIU** (45-56), Power Pack (57-61), Fault tracing/códigos (62-86).
- **Operator's Manual TAD1240GE… (76 pág.)**: https://www.manualslib.com/manual/2225156/Volvo-Penta-Tad1240ge.html (también https://www.manualslib.com/manual/1834700/Volvo-Tad1240ge.html). Technical Description: https://www.manualslib.com/manual/1591093/Volvo-Penta-Tad1242ge.html y /2399598/.
- **Workshop Manual Group 23 EDC III "1241 WS4" (76 pág.)** — incluye "limit values, control unit (ECU) and limp-home values": https://manualzilla.com/doc/6022154/1241-ws4 (visor; sólo se pudo leer la pág. de información general). Scribd: https://www.scribd.com/document/461761597/Volvo-TWD1240VE (Group 21, 7741102-3, 02-2006; no es el eléctrico).
- **Hoja de datos TAD1241GE** (oficial): https://rutector.ru/media/4231/33428.pdf → descargada. "Fully electronic with Volvo Penta EDC III – Dual frequency switch 1500/1800 rpm"; "Electronic Unit Injectors". Catálogo: controles conectables por "CAN SAE J1939 interface, CIU or Stand alone connections".
- **Contenido confirmado del Installation Manual [CONFIRMADO, MEDIA]:**
  - "EDC III… electronic system with CAN communication… control unit, six unit injectors, sensors, diagnostic connector… 'Stand alone' interface that connects directly to the engine management unit."
  - **"The starting current for engine system voltage (control unit) is 10 A"** (dimensionar llave/relé). Sistema 24 V, 2 polos; batería máx. 143 Ah/570 A DIN.
  - Standalone GE: arranque NO con retorno, paro NC con retorno; "Stop EMS connected to system voltage: Run/Stop" parametrizable. "Preheating function not used on TAD1240-42GE".
  - **Pedal/potenciómetro conectado directamente a la ECU (TWD1240VE standalone)**: resistencia **0,5-2 kΩ** (opcional máx. 2 kΩ) / 2-10 kΩ según variante; tensión **ralentí 0,3-1,9 V (defecto 1,60 V)**, **plena carga 1,9-4,7 V (defecto 3,75 V)**; si se usa otro pedal, recalibrar con la herramienta de parámetros ("Idling voltage EMS", "Max speed voltage EMS"). Señales: POT+, POT–, POT SIGNAL, IDLE SWITCH. **Contacto de ralentí integrado = "take you home"**: si falla el potenciómetro, pisando el pedal el motor sube a **80 % de régimen máximo**; soltando vuelve a ralentí. [Comparar con espec. marina EMS 2.x: 70 %.]
  - Parámetros ajustables (herramienta PC con pieza en T **874427** y cable **885337**; "Some parameters require special authorization"):
    - GE standalone: **Regulation droop 0-8 % (def. 0 %)**; Over-speed limit 10-20 % (def. 20 %); Over-speed shut off Off/On; **Idling speed 600-1200 rpm (def. 900)**; Stop EMS Run/Stop (def. Run); Primary engine speed 1500/1800; protecciones On/Off (T aire carga, nivel refrig., T refrig., P aceite, T aceite); alarmas 95-101 °C / 120-130 °C; lamp test.
    - VE standalone: **Idling speed 600-1200 (def. 600)**; **Control gradient (droop) 10-127 Nm/rpm (def. 25)**; Idling voltage EMS 0,3-1,9 V (def. 1,6); Max speed voltage EMS 1,9-4,7 V (def. 3,75); Stop EMS (def. Stop); protecciones.
  - Sincronización/reparto de carga GE: sistema GAC con módulo **EAM 122**. "System reset": mantener botón diagnóstico al dar tensión 2-3 s.
  - **Pines citados en los códigos de avería** (únicos datos de pines de esta ECU hallados en texto):
    - **Conector ROJO de la EMS**: **tomas 1 y 2 = CAN hacia la CIU** (código 213/6.4: "contact pressure in sockets 1 and 2 of the red EMS connector"; también "sleeves 11 and 12 in the CIU connector"); **toma 36 = relé de precalentamiento** (código 74).
    - **Conector NEGRO de la EMS**: **tomas 11, 23, 35 = inyectores cil. 1, 3, 5** (códigos 115, 135, 155). Coincide con el diagrama D12 camión: conector A 36 pines **11 INJ1, 22 INJ2, 23 INJ3, 34 INJ4, 35 INJ5, 36 INJ6, 12/24 = común (INJ 123 / INJ 456 VOLT OUT)**, 18 ENG SPD(+), 30 CAM(–), 31 CRK(+) (https://es.scribd.com/document/399888990, MEDIA-BAJA).
    - **Conector standalone "23-pin"** con casquillos por letra: **C = señal potenciómetro**, **E = entrada arranque**, L = lámpara P aceite, N = lámpara nivel refrigerante.
    - CIU: pines **11/12 = CAN**, **22/37 = J1708** (código 173).
  - Reacciones (pág. 63): avería grave que impide el control → **GE: "engine speed is retained"; VE: "engine goes to idle"**.
  - Códigos (lista por número y flash code): **23/24 (2.7) potenciómetro conectado a la EMS** abierto/corto → "Engine goes to idle. If the pedal is first released and then depressed, the engine can be emergency operated by means of the idling switch" (cita "Check pin C and socket C in the 23-pin connector"); **21/22 (2.8)** potenciómetro conectado a la CIU → idem; **213 (6.4) Data link CAN a la CIU** → instrumentos y lámparas dejan de funcionar; **6.5 Data link (CAN) EDC (PPID 231/SPN 639)** "internal fault in the control module… engine not running: cannot be started; engine running: idles and can only be stopped with AUX-stop"; **173 J1708 EMS** → la lámpara sólo muestra fallos internos CIU; 186 memoria EMS → no arranca; 41/42/107 (4.6) relé arranque; 108 (4.7) entrada arranque EMS; 74-76 (5.4) relé precalentamiento; 31 (6.1) T refrig. → paro; 60 (6.2) T aire → potencia 50 %; 183 (5.8) T aceite → limitación.
  - ComAp confirma el comportamiento del standalone: **"If there is a ComAp panel connected via CAN bus during power up the engine will detect this and will be controlled via CAN bus. But if the ComAp panel is dead during power up… and there is a potentiometer on standalone connector the engine will… run in stand alone mode"** (D12 genset) [MEDIA].

### 1.3 TAD620VE / TAD720VE / TAD721-722 — EDC4 (= Deutz EMR2), ECU 20700665
- Nota de prensa 2003 (ALTA): https://www.volvogroup.com/en/news-and-media/news/2003/may/news-20664.html ; 2004 TAD721/722GE: https://www.volvogroup.com/en/news-and-media/news/2004/mar/news-20734.html ("CAN-Bus… or in the traditional manner using a potentiometer").
- Manual de instalación EDC (Scribd, no abrible): https://www.scribd.com/document/729725310/Installation . Manual taller TD520GE/TAD720GE (francés, manualslib): https://www.manualslib.fr/manual/627509/Volvo-Penta-Td520Ge.html . Operator's manual "4-7 liters EDC 4" sólo de pago (sellfy).
- Interfaz según ComAp (MEDIA): capítulo Deutz EMR2 → parámetros Serdia **4400=1 (CAN activation), 4412=1 (activate TSC1a receive), 4470=1 (CAN set point by TSC1a), 4829=8 (enable stop request telegram), 4900=8 (nominal speed input type), 829 FunctEngineStop, 4424 TelStopRequestOn**; conector ECU 25 pines F: **CAN H 12, CAN L 13, Bat+ 14, Bat– 1**; velocidad por **TSC1 (SPN 898)**; "Deutz does not recommend switching off the engine by removing the power supply (fault SPN 536)".

### 1.4 Espec. oficial de interfaz CAN Volvo Penta EMS (la única encontrada abierta): *Electrical Interface Specification – Marine engines D9, D13, D16 – EMS*, pub. **47706587**, 05-2015 (EMS 2.0/2.2) — ALTA
- URL: https://www.marinpro.com/Cms_Data/Contents/powerhouse/Folders/Accessories/AccessoryFiles/~contents/4YD2DR3WYE3MEBNA/OpenCAN_InstallGuideline_rev_1.pdf → descargada (36 pág.). Ver §2 para contenido. Equivalentes industriales/EMS 2.3/2.4 sólo en Scribd/pdfcoffee (no abribles): 47706487 (EMS2.3), 47711360, 47714300 (EMS2.4), 47701853 (D13 EMS install), "EMS2 Installation Manual D16 US" (7748665?).

### 1.5 TAD940-943 (EMS 2, 9 L) — Operator's Manual 47702660 (03-2013) dentro de un PDF de 63 pág. (hoja de datos TAD941GE + manual) — ALTA (oficial), fuente tercera
- https://tech-expo.ru/upload/iblock/043/Volvo-TAD941GE_en.pdf → descargado. Contiene descripción CIU/DCU (pág. 21-23 impresas), arranque/paro, menús DCU y **registro de códigos EMS 2 con SPN/PID/PPID/SID/PSID/flash/FMI** (ver §5).

---

## 2. CIU / DCU y mensajería CAN hacia la ECU EMS (¿TSC1 o propietario?)

### 2.1 Qué hace la CIU [CONFIRMADO]
- "The CIU is a 'translator' between the control unit (EMS) and the customer's own control panel. Two serial links: fast **CAN (250 kbit/s)** — all data related to instruments, indication lamps, contacts and **potentiometers**; slow **J1708/J1587** — diagnostic info, flash codes" (manual 7747632 y manual 47702660, ALTA). La CIU es **MID 144** (códigos "MID 128 / MID 144"). La programación de la CIU se hace con VODIA como "MID 144 ECU".
- Interfaz físico motor↔CIU/OEM: **conector Deutsch 8 pines** (dos en la CIU: pin y toma). Pinout oficial (espec. marina 47706587, igual que la tabla publicada para gensets industriales EMS/EMS2): **1 CAN H (J1939), 2 CAN L, 3 Batería –, 4 Batería +, 5 Ignición (power-up), 6 N/A / stop request (gensets: "energized to stop" por defecto, configurable a "energized to run"), 7 J1708 A/J1587, 8 J1708 B/J1587**. ComAp usa el mismo conector: 1 CAN H, 2 CAN L, 3 Bat–, 4 Bat+, 5 Key switch (salida "ECU PwrRelay"), 6 Stop request (salida inversa "ECUCommError"). **Advertencia ComAp**: "no continuous active stop signal on pin 6… impossible to change parameters/reprogram… The ECU could be damaged when power is removed".
- Terminación: "120 Ω resistors at each end… **The EMS has built-in terminations**" (47706587 pág. 10). En CIU/DCU hay una resistencia 120 Ω externa (manual 7747632).

### 2.2 Cómo se envía la demanda de régimen: **mensaje propietario Volvo "VP Status" (VP70), NO TSC1** [CONFIRMADO para EMS 2.0/2.2 marino e industrial; INFERIDO para EMS 1/EDC III]
- Tabla oficial de funciones (Volvo Penta "Genset engine electrical interface", EMS y EMS2; copia en https://dieselgeneratortechblog.wordpress.com/2018/12/03/volvo-genset-engine-electrical-interface/ y https://medium.com/@dieselgenerator/system-information-throttle-genset-governor-about-volvo-penta-engine-f6483c049ec6 — BAJA como sitio, pero reproduce el documento Volvo): Start/Stop → "VP Status" (J1939) / PPID 98 (J1587) / entradas HW en CIU-DCU; **Throttle 0-100 % → "Throttle in VP Status" / PPID 132 / potenciómetro (CIU)**; Torque/speed override → **TSC1**; Governor mode (iso/droop), Idle request, Preheat request, Frequency select (1500/1800, sólo con motor parado), Engine protection override → todos en **VP Status**. "0 % = idle, 100 % = max speed; genset 50 % = 1500/1800 rpm". "TSC1 overrides the throttle in VP Status. Speed control from gearbox (SA 0x03) always has highest priority."
- Definición exacta del VP70 (47706587, pág. 25-26, ALTA, EMS 2.0/2.2): **PGN 65350 (0xFF46), PDU format 255, PDU specific 70, 8 bytes, prioridad 3, ID 0x0CFF4611 (SA 0x11 = OEM controller), Rx cada 20 ms.** Campos (byte.bit, 2 bits cada uno salvo pedal): Start request 1.1; Stop request 1.3; Governor mode select 1.5 (0 = speed mode, 1 = torque/droop); Idle speed select 1.7 (1 = idle request); Frequency select 2.1 (0 = 1500, 1 = 1800; sólo genset); Preheat request 2.5; Engine restored operation 2.7; **Accelerator pedal position 3.1, 16 bits (0x0000-0x03FF = 0-100 %, factor 100/1023 %/bit; 0xFE00.. error; 0xFFFF N/A)**; Disable fuel 5.1 (genset). "All unused signals must be set to 'Not available' (bits a 1)". Respuesta del motor: **VP71 "VP Engine industry" PGN 65351, ID 0x0CFF4700, Tx 50 ms** (running indication 1.3, buzzer 3.1, restored operation 3.7, OEM fan speed request 7.1, "Engine power down ack" 8.3).
- Mensajes J1939 estándar que transmite la EMS (47706587 pág. 23-24): EEC1 0x0CF00400 **20 ms** (SPN 512/513/190/1675), EEC2 0x0CF00300 50 ms (91, 92), EEC3 250 ms, ET1 0x18FEEE00 1000 ms (110, 175), IC1 500 ms, LFC/LFE 100 ms, HOURS 0x18FEE500 10 s ("deviation from SAE: Tx on request"), VEP1 1000 ms (158), EC1 5 s/on request (188, 528-534, 544), DM1 1000 ms (+TP.CM/TP.DT), **TSC1 Rx desde 0x0C000003 / 0x0C000011 / 0x0C0000E6 / 0x0C0000EA** (SPN 695, 897, 898, 518, 3350; "Rx rate defined in SPN 3349"), Request PGN 0x18EA00xx.
- **Direcciones fuente (47706587 pág. 11)**: EMS 0x00; TECU 0x03; **OEM controller 0x11 (17)**; BBM 0xE6. **TSC1 aceptado sólo desde SA 0x03 (transmisión) y 0x11 (OEM)**; "expected Tx rate 10 ms". DEIF para EMS 2.3: "J1939 message TSC1, default speed control address 3" (https://documentation.deif.com/r/ie-150-agc-150-engine-communication-4189341302-uk/j1939-ecus-and-engines/volvo-penta-%E6%B2%83%E5%B0%94%E6%B2%83%E9%81%8D%E8%BE%BE/volvo-penta-ems-2.3 , MEDIA; el índice padre devolvió 503).
- **ComAp (MEDIA) para "Volvo EDC3 (EMS1) / EMS2"** (ECU-list guide 7.0.0 §3.26 y Electronic Engines Support 2015 pág. 170-178): comandos del controlador a la ECU = **Start Request, Stop Request, Idle Speed Select, Frequency Select, Preheat Request, Governor Mode (0 iso/1 droop), Protection Override, Diagnostic Request, Fuel disable request — todos "Proprietary parameter… contact local Volvo representative"**; demanda de velocidad = **"Accelerator Pedal Position" (propietario)** o **"Requested speed SPN 898" (TSC1)**; procedimiento de cambio 1500↔1800 "in the same way as Volvo Penta's CIU" (power-up → cambiar Frequency select → stop request, todo < 10 s). ComAp agrupa **EDC3 (EMS1, D12) y EMS2 (D9/D16/D734) bajo el mismo fichero ESF "Volvo Singlespeed/Allspeed"** ⇒ **[INFERIDO, fuerte]** la 1ª generación (EDC III, ECU 20577134, hardware hermano de la E-ECU D6D) acepta la misma familia de mensajes propietarios VP Status que EMS 2. **No existe confirmación documental de que la V-ECU del EC210B use exactamente VP70/PGN 65350**; hay que capturarlo en la máquina.
- Volvo CE (apoyo indirecto): código **PID 91 FMI 9 "T-ECU rpm request"** (EW160B): "The E-ECU does not get the rpm request signal through **J1939 or J1587**" (https://www.scribd.com/document/814203409/Error-code , MEDIA-BAJA) ⇒ la petición de rpm va por J1939 con respaldo J1587 (igual que el esquema Penta CIU). Manual Volvo CE: "CAN1/J1939 control link 250 kbit; J1587/J1708 backup; terminal resistors 120 Ω… one is built into the engine control unit" (https://www.scribd.com/document/439922521/Electrical-System , resumen de búsqueda, MEDIA-BAJA).

### 2.3 Lista de PGN soportados ("J1939 compatibility") para TAD-VE 1ª gen. — **[NO ENCONTRADO]** documento específico; la lista oficial encontrada es la de EMS 2.0/2.2 marino (§2.2). ComAp lista para EDC3/EMS1/EMS2 los SPN 190, 513, 512, 91, 92, 94, 98, 100, 101, 109, 111, 110, 174, 175, 183, 102, 105, 106, 173, 158, 97, 987/624/623/1213, 1110/1109, 1081 y propietarios (idle/max speed, lámparas, fusibles 15/30/EMS, estado baterías).

---

## 3. Comportamiento sin CIU/DCU/controlador OEM; aceptación de TSC1 de terceros; rango; timeout

- **Sin mensaje válido de pedal/VP70 → ralentí**: "If no valid VP70 messages are received, engine speed will be set to idle speed… In the case of a pedal signal fault the engine will go to idle… the pedal signal will be considered valid only after a valid zero (0 %) pedal demand" (47706587, ALTA). Genset: valor de pedal **congelado**. "Idle speed select" como **limp home**: 1→0 rampa lenta hasta **70 %** del régimen máximo (EMS 2.x marino) / **80 %** (EDC III TWD1240VE idle switch, instalación; también 80 % en la tabla genset EMS/EMS2).
- **Sin CAN pero con J1587**: potenciómetro y arranque/paro siguen por J1587 (EMS 2 industrial, 7747632). **Sin ambos**: ralentí, paro sólo por AUX-STOP; SID 231 FMI 2 (6.5): "Engine can not be started or if engine is running it can only be stopped by pushing the aux-stop" (7747632 pág. 126/visor 128). PPID 132 FMI 9 "EMS2 is missing the throttle signal" → "Engine goes to idle"; PSID 201 FMI 9 "J1939 communication bus – abnormal updating rate" (MID 128/144).
- **TSC1 de terceros**: aceptado desde **SA 0x03 y 0x11** (y 0xE6/0xEA en la tabla de IDs) en EMS 2.0/2.2; con prioridad sobre VP70; velocidad en SPN 898 (0,125 rpm/bit), modo en SPN 695; Tx esperado **10 ms**; timeout "defined in SPN 3349" (no se da valor en ms) [ALTA para EMS 2.x; **NO CONFIRMADO para EMS 1/EDC III ni para la E-ECU D6D**]. ComAp y DEIF usan TSC1/"Requested speed" también para EDC3/EMS1 (MEDIA). Nota general (Enovation/IQAN, BAJA): la SA aceptada suele ser el problema nº 1; Volvo/Volvo Penta acepta 0x11 (17, "cruise control") y 0x03.
- **Rango de demanda**: VP70 0-100 % (0 % = ralentí, 100 % = máximo); genset 50 % = nominal, ±90 rpm con 0-100 % (47706587). Potenciómetro directo EDC III: 0,3-1,9 V ralentí / 1,9-4,7 V máximo.
- **Power-up/down** (47706587): la EMS arranca < 1 s tras ignición (pin 5); self-hold hasta 10 s tras apagado — no cortar batería antes. Arranque por "Start request" hasta: régimen > límite (≈480 rpm según tabla genset), señal inactiva, stop simultáneo, no arranca, protección térmica del motor de arranque (≈20 s; 30 s genset; luego 80 s de bloqueo según manual TAD1240), batería baja.
- Códigos de comunicación Volvo CE observados en foros (BAJA): EC210BLC "140 SID 231-9" (I-ECU sin comunicación; 60 Ω en el bus con todo conectado, 120 Ω al desconectar I-ECU o E-ECU) https://www.heavyequipmentforums.com/threads/volvo-ec210blc-crank-no-start.91709/ ; EC210CL "PSID 201-09 no communication" + "Engine shutdown" en ralentí bajo, el dial de régimen no actúa en modo manual (el modo manual usa ajustes fijos de alto/bajo ralentí) https://www.heavyequipmentforums.com/threads/volvo-ec210cl-throttle-dial-wont-work-in-manual-code-psid-201-09.122528/ .

---

## 4. Parámetros Volvo Penta (ralentí, emergencia, droop/isócrono, precalentamiento, start/stop por CAN, potenciómetro directo)

| Parámetro | Valor encontrado | Fuente / fiabilidad |
|---|---|---|
| Ralentí | 600-1200 rpm (def. 600 VE, 900 GE) | Install. Manual EDC III pág. 20/43 (MEDIA) |
| Droop | GE: 0-8 % (def. 0 = isócrono); VE: "control gradient" 10-127 Nm/rpm (def. 25) | Install. Manual EDC III |
| Governor mode por CAN | VP70 bit 1.5: 0 = speed mode, 1 = torque/droop; "normally isochronous; droop signal adds droop" | 47706587 (ALTA); tabla genset |
| Sobrevelocidad | aviso 10-20 % (def. 20 %), paro Off/On | Install. Manual EDC III |
| Régimen de emergencia (limp) | 70 % (EMS 2.x) / 80 % (EDC III idle switch) del máximo, por "Idle speed select"/contacto de ralentí | 47706587 / Install. EDC III |
| Precalentamiento | VP70 bit 2.5; sólo con refrigerante frío y motor parado; se corta al arrancar; TAD1240-42GE no lo usa; DCU "Pre-heat on ignition" hasta 50 s | tabla genset, Install. EDC III, Op. Manual |
| Start/Stop por CAN | VP70 bits 1.1/1.3 (+ EEC1 SPN 1675 starter mode como realimentación); también J1587 PPID 98 | 47706587, tabla genset |
| Frecuencia 1500/1800 | VP70 bit 2.1, sólo motor parado; secuencia < 10 s | 47706587, ComAp |
| Potenciómetro directo a la ECU | **Sí** en EDC III "Stand alone": pot 0,5-2 kΩ, 0,3-1,9 V / 1,9-4,7 V, + idle switch; detección automática CAN vs. pot en power-up | Install. EDC III; ComAp |
| Potenciómetro en CIU | pot al CIU → CIU lo envía por CAN (y J1587 como respaldo) | 7747632, 47702660 |
| Tensión/corriente ECU | 24 V, arranque 10 A (control unit); batería secundaria fusible 16 A (marino) | Install. EDC III; 47706587 |
| Herramienta de parámetros | pieza en T 874427 + cable 885337 (EDC III); VODIA (EMS 2) | Install. EDC III; 7747632 |

**[NO ENCONTRADO]**: valores de timeout de TSC1/VP70 en ms; tabla completa de parámetros EMS 2 TAD650-760VE (sólo lista cualitativa DCU).

---

## 5. Códigos de avería MID 128 (y MID 144) relacionados con comunicación / mando

### 5.1 EMS 2 TAD650-760VE/TAD734GE (7747632, ALTA/MEDIA) — índice "MID 128 (engine control unit EMS)": SPN · flash (eléctrico/valor) · PID/PPID/SID/PSID · FMI
- **Communication fault J1939: SPN 639, flash 6.5 (EMS) / 6.4 (CIU), SID 231, FMI 2** — "Engine can not be started or if engine is running it can only be stopped by pushing the aux-stop".
- **J1939 communication bus: SPN 639/1675, PSID 201, FMI 9** (MID 128 / MID 144) — "Abnormal updating rate / Communication error"; aviso en DCU, nada en CIU.
- Throttle input request failure DCU/CIU: **PPID 132, FMI 3/4/9** (9 = "EMS2 is missing the throttle signal") → **"Engine goes to idle"**; flash 2.8.
- Start input CIU: PPID 4 (4.7 EMS / 5.2 CIU) FMI 3/4; Engine stop switch: PPID 6 (SPN 520195/970), 4.8 EMS / 5.3 CIU, FMI 3/4/5; Engine sync acknowledge PPID 98 FMI 9; Controller error SID 254 (9.9/9.8) FMI 3/8/12; Program memory SID 240 (9.9) FMI 2/7/11/14; 5 V supply SID 232/211 (9.3); Battery voltage PID 158 (3.9 EMS / 6.9 CIU); ECU temperature PPID 55 (8.4).
- **[NO ENCONTRADO]** SID 250 (J1708) y PSID 200 en este manual (no aparecen en el índice del 7747632).

### 5.2 EMS 2 TAD940-943 (Operator's Manual 47702660, ALTA): "Fault Code Register" (SPN · PID/PPID/SID/PSID · flash · FMI)
- SAE J1939 Data Link **639 · SID 231 · 6.5 (EMS)/6.4 (CIU) · FMI 2**; SAE J1939 Data Link **608 · PSID 201 · FMI 9**; **SAE J1708 Data Link 608 · SID 250 · 9.2/-**; SAE J1939 Data Link 1231 · SID 232 · FMI 2 y 1231 · SID 229 · FMI 9; Data Link 2017 · PSID 201 · FMI 9; Throttle position 608 · PPID 98 · FMI 9; Throttle calibrated position 608 · PPID 132 · 2.8 · FMI 9; Percent accelerator pedal position 91 · PID 91 · 2.7 (EMS)/2.8 (CIU) · FMI 9; Stop input EMS 970 · PPID 6 · 4.8 · FMI 4; Stop input CIU 520195 · PPID 6 · 5.3; Starter input 520194 · PPID 4 · 4.7/5.2; Frequency select input PPID 113; Diagnostic request switch PPID 259; lámparas PPID 260-264; Program memory 628 · SID 240 · 9.9 · FMI 2/12; Controller error 629 · SID 254 · 9.9/9.8 · FMI 8/12; Calibration memory 630 · SID 253; Main relay 1485 · PPID 5; Starter output 1675/2898/2899 · SID 3/39.
- **PSID 200** no aparece en ninguno de los dos manuales Penta leídos **[NO ENCONTRADO]**; en fuentes de camión Volvo (truckmanualshub, BAJA) PSID 200 = "SAE J1939 open circuit, data link engine ECU" bajo MID 249/130.

### 5.3 EDC III TAD1240-42/TWD1240VE (Operator's/Installation Manual, MEDIA): códigos por flash + SID/SPN
- 6.4 Data link (CAN) CIU · PPID 231/SPN 639; **6.5 Data link (CAN) EDC · PPID 231/SPN 639** (no arranca / ralentí + AUX stop); 9.3 memoria · SID 232/SPN 620; 9.9 alimentación sensores · SID 240/SPN 639; 4.8 stop input EDC · PPID 6/SPN 520195; 5.4 relé precalentamiento · PID 45/SPN 626; 2.6 engine speed · 190; 7.x inyectores SID 1-6/SPN 651-656; códigos numéricos 21-24 (potenciómetro), 173 (J1708), 213 (CAN CIU), 186 (memoria).
- ComAp "Volvo allspeed fault codes" (SPN→texto): 231 J1939Datalink, 608 J1587Datalink, 639 J1939CANBus, 620 5VSupply, 628 ProgramMemory, 629 Controller1, 630 CalibratMemory, 636/637 sensores, 651-656 inyectores, 677 StarterMotor, 1485 ECMMainRelay, etc.

---

## 6. Números de parte de conectores de la ECU (36 pines) — **[mayormente NO ENCONTRADO]**
- Catálogo de piezas Volvo Penta con el housing de 36 polos: **no hallado** en acceso público (requiere VPPN/dealer). Búsquedas "connector housing 36 pole EMS", "60100001 connector" no dieron resultados oficiales.
- Lo que sí hay (BAJA, vendedores): ECU 60100001 / VOE60100001 (TAD650-760VE, TAD734GE, TAD751GE, D7E) ~320-690 USD; 60100002 = 20577135 = VOE03161983 (D6D, EC210B/EC240B/EC290B, L90E-L190F); 20577134 = 20582963 (D12, TAD1241GE/TAD1242GE/TWD1240VE); 20700665 (EDC4: TAD420-722, TD420-720); VOE3161962 (D12D CE); VOE24425461 (TAD940/941GE, TAD1641GE, L150E-L220E); 20814795 (TAD1640GE/1241VE…). Volvo CE "Monitor plug connector of ECU" VOE14390065 / VOE14636301 (EC210/240/290/360, no confirmado que sea el de 36 pines).
- Conectores Bosch EDC7 (aplicables a la EMS 2 de TAD650-760VE si es EDC7 **[INFERIDO]**): eBay "EDC7 89 pin connector 1928404195"; Bosch 36-pin code I **1928406269** / code B **1928406262** (chiefenterprises.com) — **sin verificación** de que sean los de Volvo.
- Interfaz OEM/CIU: **Deutsch 8 pines** (motor) + conector diagnóstico 6 pines J1708/J1587 (marino) — 47706587.
- Herramientas Volvo Penta citadas: 9998482 "Gauge for connector on control unit", 885675 cable adaptador sensores, 9998699 measurebox, 88890016 cable adaptador (7747632).

---

## 7. Proyectos DIY / controladores de grupo que documentan la interfaz Volvo EMS

- **Arduino/ESP32/PLC con Volvo Penta EMS/TAD**: **[NO ENCONTRADO]** ningún proyecto público. Lo más cercano: hilo control.com "TAD1641GE EMS2 → PLC por J1939" (pregunta sin solución técnica) https://control.com/forums/threads/45516 ; caso CSS Electronics de ingeniería inversa de PGN propietarios en motores Volvo Penta marinos (CAN logger + Wireshark) https://csselectronics.com/pages/j1939-reverse-engineering-pgn-spn ; hilos IQAN sobre SA de TSC1 (Volvo camión) https://forum.iqan.se/communities/1/topics/4475-rpm-control-with-tsc1-on-volvo-truck ; guía Enovation/Murphy TSC1 https://support.enovationcontrols.com/hc/en-us/articles/18705454147219-Engine-TSC1-Throttling-and-Emissions-Messaging-Troubleshooting . Volvo Penta "Easy Link" y OpenCAN son las vías oficiales.
- **ComAp** (MEDIA) — la mejor fuente tercera: *Electronic Engines Support – Reference Guide 7.0.0 (2019)* §3.26 Volvo (págs. 219-226 PDF) y *ComAp Electronic Engines Support 08-2015* (págs. 170-179: Volvo EDC3/EMS1/EMS2 single/allspeed, EDC4→EMR2; págs. 61-63 Deutz EMR2; págs. 248-250 textos de códigos). ESF: "Volvo Singlespeed" (id 1, D9/D12/D13/D16 EMSI/EMSII/EMS2.2), "Volvo Allspeed" (id 2, D5-D16 EDC/EMS), "Volvo EDC7 Allspeed KWP2000" (id 114), "Volvo EMS J1587" (id 163). Cableado y comandos: ver §2.2.
- **DEIF** (MEDIA): AGC-150/iE-150 *Engine communication* 4189341302, página "Volvo Penta EMS 2.3": Start/Stop/Speed control/Idle mode/50-60 Hz/Shutdown override, **TSC1, default speed control address 3**. El índice de ECUs (para ver si lista EMS 1/EDC4) devolvió 503 tres veces.
- **Deep Sea (DSE)**: **[NO ENCONTRADO]** documento público con los ajustes "Volvo EMS/EMS2/EDC4" (el PDF jcbgenerators devolvió "bot verification"; la lista de "engine type" está en el DSE Configuration Suite PC Manual, p.ej. 057-172).
- **Woodward easYgen**: sólo una nota de aplicación de speed bias J1939 (FPT MD1), nada Volvo. **Murphy PowerView**: nada específico Volvo.
- Gateways que listan compatibilidad J1939 Tx de Volvo Penta EDC4/EMS/EMS2/EDC III (Maretron J2K100 KB id 544; Yacht Devices YDEG-04, manual descargado — menciona EDC III/EDC IV, "P1682 Communication problem — EMS message missing").

---

## 8. Esquemas extraídos (/home/user/docs/esquemas/)

No fue posible obtener las imágenes de los esquemas de manualslib (TAD750VE pág. 146-150; TAD1240 pág. 16/29/39/51) porque el sitio sirve las páginas como imágenes tras un desafío Cloudflare ("Just a moment…"), y no se intentó eludirlo. Scribd/pdfcoffee tampoco entregan contenido. Los esquemas obtenidos proceden de los PDF descargados (renderizados con pdftoppm 150 dpi):

| Imagen | Fuente (PDF, pág.) | Qué muestra |
|---|---|---|
| penta_EMS_47706587_p06_CAN_bus_interface.png | 47706587 p.6 (impresa 4) | Topología EMS ↔ sistema de control OEM: conector motor 8 pines, conector diagnóstico 6 pines J1708/J1587, módulo de potencia |
| penta_EMS_47706587_p07_OEM_interface_electrical_connectors.png | 47706587 p.7 (5) | **Pinout conector A Deutsch 8 pines: 1 CAN H, 2 CAN L, 3 Bat–, 4 Bat+, 5 Ignición, 6 N/A, 7 J1708A, 8 J1708B** + conector B seguridad |
| penta_EMS_47706587_p08_OEM_interface_power_connector.png | 47706587 p.8 (6) | Conector batería secundaria (fusible 16 A) y paro externo NO/NC |
| penta_EMS_47706587_p09/p10/p11_*_engine_connectors_OEM_8pin.png | 47706587 p.9-11 (7-9) | Ubicación de conectores en motores D9/D13/D16 (EMS 2.x) |
| penta_EMS_47706587_p12_CAN_bus_termination.png | 47706587 p.12 (10) | Terminación 120 Ω: EMS con terminación integrada + terminación en el dispositivo OEM |
| penta_EMS_47706587_p18_speed_control_VP70_TSC1_schematic.png | 47706587 p.18 (16) | Diagrama de selección de fuente de régimen: VP70 pedal vs. TSC1 (SA 0x03/0x11) |
| penta_EMS_47706587_p21_TSC1_control_source_addresses.png | 47706587 p.21 (19) | TSC1: SA aceptadas, tasa 10 ms, señales |
| penta_EMS_47706587_p27_VP70_VP_Status_message_definition.png | 47706587 p.27 (25) | Definición VP70 PGN 65350 / 0x0CFF4611 bits |
| penta_EMS_47706587_p28_VP70_accelerator_pedal_position.png | 47706587 p.28 (26) | Campo pedal 0-1023 = 0-100 % |
| penta_ComAp_ECUlist_p18_J1939_8pin_diagnostic_connector.png | ComAp ECU list 7.0.0 p.18 | Conector diagnóstico 8 pines J1939 (layout) |
| penta_ComAp_ECUlist_p222_Volvo_EMS_recommended_wiring.png | ComAp ECU list 7.0.0 p.222 | Cableado recomendado controlador ↔ Volvo EDC3/EMS1/EMS2 (8 pines), advertencia pin 6 |
| penta_ComAp2015_p174_Volvo_EDC3_EMS2_recommended_wiring.png | ComAp 2015 p.174 | Idem (versión 2015) + procedimiento 1500/1800 |
| penta_ComAp2015_p62_Deutz_EMR2_VolvoEDC4_wiring_Serdia_params.png | ComAp 2015 p.62 | Deutz EMR2 (= Volvo EDC4): conector 25 pines F (CAN H 12, CAN L 13, Bat+ 14, Bat– 1), parámetros Serdia TSC1 |
| penta_TAD941GE_OpManual_EMS2_p16_CIU_description.png | 47702660 p.16 (21) | Descripción CIU (CAN + J1708) e instrumentos Easy Link |
| penta_TAD941GE_OpManual_EMS2_p18_DCU_description.png | 47702660 p.18 | DCU |
| penta_TAD941GE_OpManual_EMS2_p32/p33/p34_fault_code_table_*.png | 47702660 p.32-34 (37-39) | Registro de códigos EMS 2 con SID 231 / PSID 201 / SID 250 / PPID 132 |

---

## 9. Manuales descargables (y enlaces de visualización)

Carpeta local: **/home/user/docs/manuales/volvo_penta_tad/** (todos verificados como `%PDF`; total ≈ 21 MB).

| Título | Nº pub. | Contenido | Formato/tamaño | Gratis/pago | ¿Abierto? | URL | Ruta local |
|---|---|---|---|---|---|---|---|
| Electrical Interface Specification – Marine engines D9/D13/D16 – EMS (2.0/2.2) | 47706587 (05-2015) | Interfaz OEM 8 pines, SA, VP70/VP71, TSC1, lista PGN, J1587 PM | PDF 36 p., 1,3 MB | Gratis | Sí (pdftotext) | https://www.marinpro.com/Cms_Data/Contents/powerhouse/Folders/Accessories/AccessoryFiles/~contents/4YD2DR3WYE3MEBNA/OpenCAN_InstallGuideline_rev_1.pdf | /home/user/docs/manuales/volvo_penta_tad/VolvoPenta_Marine_D9_D13_D16_EMS_Electrical_Interface_Specification_47706587.pdf |
| Workshop Manual Group 30 Electrical – TAD734GE, TAD650/660/750/760VE (DEMO 15 p.) | 7747632 (03-2007) | Índice completo, herramientas, ubicación componentes, reprogramación, protección motor, índice SPN/SID | PDF 15 p., 0,4 MB | Gratis (demo) | Sí | https://krutilvertel.com/pdf/demo/motorist/rukovodstvo-po-remontu-dvigatelja-volvo-tad734ge-demo.pdf | …/VolvoPenta_TAD734GE_TAD650-760VE_Group30_Electrical_Workshop_Manual_7747632_DEMO.pdf |
| Workshop Manual Group 30 – TAD750VE (completo, 160 p.) | 7747632 | Esquemas EMS 2/DCU/CIU, códigos MID 128 | visor web | Gratis (visor; descarga con captcha) | Visor sí; descarga no | https://www.manualslib.com/manual/3858599/Volvo-Tad750ve.html | — |
| Installation Manual EDC III – TAD1240GE/1241GE-VE/1242GE-VE/TWD1240VE | (no visible) | Standalone/CIU/Power Pack, pedal, parámetros, códigos | visor web 88 p. | Gratis (visor) | Visor sí | https://www.manualslib.com/manual/4542784/Volvo-Penta-Tad1240ge.html | — |
| Operator's Manual TAD1240GE… TWD1240VE (EDC III) | — | CIU/DCU, arranque, códigos con SID/SPN | visor 76 p. | Gratis (visor) | Visor sí | https://www.manualslib.com/manual/2225156/Volvo-Penta-Tad1240ge.html | — |
| Technical Description TAD1240-42GE | — | datos técnicos | visor 61-62 p. | Gratis | No abierto | https://www.manualslib.com/manual/1591093/Volvo-Penta-Tad1242ge.html | — |
| Workshop Manual Group 23 EDC III "1241 WS4" | — | límites, ECU, limp-home | visor 76 p. | Gratis (visor) | Parcial | https://manualzilla.com/doc/6022154/1241-ws4 | — |
| Hoja de datos TAD1241GE (EDC III) | — | ficha oficial | PDF 2 p. | Gratis | Sí | https://rutector.ru/media/4231/33428.pdf | …/VolvoPenta_TAD1241GE_Datasheet_EDCIII.pdf |
| Hoja de datos TAD734GE | 47709301 | ficha oficial EMS 2 | PDF 2 p. | Gratis | Sí | https://cdn.wajax.com/wp-content/uploads/2018/02/47709301_EN.pdf | …/VolvoPenta_TAD734GE_Datasheet_47709301.pdf |
| Hoja de datos TAD941GE + **Operator's Manual 9 L EMS 2** | 47702660 (03-2013) | CIU/DCU, códigos EMS 2 completos | PDF 63 p., 3,7 MB | Gratis | Sí | https://tech-expo.ru/upload/iblock/043/Volvo-TAD941GE_en.pdf | …/VolvoPenta_TAD941GE_Datasheet_plus_OperatorsManual_9L_EMS2.pdf |
| Hojas de datos TAD941GE (2 p.) / TAD1641GE | — | fichas | PDF | Gratis | Sí | https://rutector.ru/media/4237/33427.pdf ; https://rutector.ru/media/5770/33431.pdf | …/VolvoPenta_TAD941GE_Datasheet_2p.pdf ; …/VolvoPenta_TAD1641GE_Datasheet.pdf |
| ComAp – Electronic Engines Support Reference Guide 7.0.0 (ECU list) | r3, 2019 | §3.26 Volvo EDC3/EMS1/EMS2 single/allspeed, cableado, códigos | PDF 419 p., 5 MB | Gratis | Sí | http://generator-info.com/ComAp/Control%20Panels/ECU-list-7-0-0-Global-Guide_r3.pdf | …/ComAp_ECU_List_7-0-0_Global_Guide_r3.pdf |
| ComAp – Electronic Engines Support 08-2015 r2 | — | Volvo EDC/EDC3/EMS2/EDC4(EMR2), Deutz EMR2, textos de códigos | PDF 254 p., 6,9 MB | Gratis | Sí | https://grupofeynsa.wordpress.com/wp-content/uploads/2015/10/comap-support.pdf | …/ComAp_Electronic_Engines_Support_2015.pdf |
| Yacht Devices YDEG-04 manual | — | compatibilidad J1939/Volvo Penta (EDC III/IV, EVC), lista mensajes | PDF 57 p. | Gratis | Sí | https://www.yachtd.com/downloads/ydeg04.pdf | …/YachtDevices_YDEG-04_Manual_J1939_VolvoPenta.pdf |
| Cattron/Dynagen TOUGH J1939 reference (genérico TSC1) | 9M02-9252-A201 | TSC1 genérico | PDF 43 p. | Gratis | Sí | https://www.cattron.com/wp-content/uploads/dynagen-tough-series-J1939-reference-manual-en.pdf | …/Cattron_Dynagen_TOUGH_J1939_Reference_Manual.pdf |
| DEIF AGC-150/iE-150 Engine communication – Volvo Penta EMS 2.3 | 4189341302 | TSC1, SA 3, start/stop | web | Gratis | Sí (una página) | https://documentation.deif.com/r/ie-150-agc-150-engine-communication-4189341302-uk/j1939-ecus-and-engines/volvo-penta-%E6%B2%83%E5%B0%94%E6%B2%83%E9%81%8D%E8%BE%BE/volvo-penta-ems-2.3 | — |
| Volvo Penta Genset Engine Electrical Interface (EMS/EMS2, resumen de doc. Volvo) | — | tabla funciones VP Status/J1587/CIU, arranque, limp 80 % | web | Gratis | Sí (wordpress) | https://dieselgeneratortechblog.wordpress.com/2018/12/03/volvo-genset-engine-electrical-interface/ ; https://www.dieselgeneratortech.com/generator-sets/Volvo-Penta-genset-engine-electrical-interface.html | — |
| **No abribles / no descargables (listado para referencia)** | | | | | | | |
| EMS2 Installation Manual D16 US (TAD734GE, D9, TAD125xVE, D13, D16; CIU 42 polos AMP) | ¿7748665? | | pdfcoffee | Gratis (403) | No | https://pdfcoffee.com/ems2-installation-manuald16us-pdf-free.html | — |
| Electrical Interface Specification EMS2.3 | 47706487 | | pdfcoffee | — | No | https://pdfcoffee.com/download/electrical-interface-specification-ems2347706487en-pdf-free.html | — |
| Electric Interface Specification EMS 2.4 | 47711360 / 47714300 | | Scribd | — | No | https://www.scribd.com/document/716023088/Electric-Interface-Specification-47711360-EN ; https://www.scribd.com/document/716023109/Electrical-Interface-Specification-EMS2-4-47714300 | — |
| Installation D13 EMS | 47701853 | | pdfcoffee | — | No | https://pdfcoffee.com/volvo-47701853installation-d13-ems-pdf-free.html | — |
| "Volvo TAD750VE engine wiring" (EMS2 harness) | — | | Scribd | — | No | https://www.scribd.com/document/475446944/Volvo-TAD750VE-engine-wiring | — |
| EDC (EDC4) Installation manual | — | | Scribd | — | No | https://www.scribd.com/document/729725310/Installation | — |
| Volvo D12 Electrical Wiring Diagram (conector A 36 pines) | — | | Scribd | — | Parcial | https://es.scribd.com/document/399888990 | — |
| Volvo CE EC210B / Electrical System handout / Error codes EW160B | — | | Scribd | — | Parcial | https://www.scribd.com/document/326541302/EC210B ; https://www.scribd.com/document/439922521/Electrical-System ; https://www.scribd.com/document/814203409/Error-code | — |
| Workshop manual 2007 TAD650VE… (2,35 MB) | 7747632 | | volvo-club.cz | Gratis con login | No (HTML) | https://en.volvo-club.cz/manual_download.php?id=1976 | — |
| Group 30 TAD650VE-760VE/TAD734GE; Group 23 EDC TAD1240…; EMS2 TAD1340-1365 install; EDC 4 operator's | — | | sellfy/obdtotal/heydownloads | **Pago** | No | (varios, p.ej. https://txuxg6nv.sellfy.store/p/volvo-penta-tad650ve-tad760ve-tad734ge-group-30-workshop-manual-304495118-pdf-download/) | — |

Nota: los sitios oficiales pubs.volvopenta.com (503) y vppn.com (login dealer) no fueron accesibles.

---

## 10. Resumen de lo confirmado / inferido / no encontrado
- **Confirmado**: TAD650-760VE son EMS 2 common rail (no D6D); CIU usa CAN 250 k + J1587; demanda de régimen Volvo = mensaje propietario VP Status (VP70 PGN 65350, SA 0x11, 20 ms) con TSC1 como override desde SA 0x03/0x11 (10 ms); sin VP70/pedal válido → ralentí; sin CAN ni J1587 → ralentí + AUX-STOP; códigos SID 231 (6.5/6.4), PSID 201, SID 250, PPID 132; EMS lleva terminación 120 Ω integrada; conector OEM Deutsch 8 pines; EDC III admite potenciómetro directo (0,3-1,9 / 1,9-4,7 V, idle switch 80 %); corriente ECU 10 A; parámetros ralentí 600-1200, droop 0-8 %.
- **Inferido**: la E-ECU D6D (20577135) es hermana de la EDC III D12 (20577134), 2×36 pines, y debería compartir el esquema de mensajería propietaria Volvo; la ECU 60100001 es Bosch EDC7 y no comparte hardware con 60100002.
- **No encontrado**: pinout completo de los 2×36 pines de 20577135/20577134 (sólo pines parciales); PGN exactos de la V-ECU EC210B; timeout en ms; números de parte oficiales de los conectores de 36 polos; documentación DSE/Woodward Volvo; proyectos ESP32/Arduino con Volvo EMS; confirmación "LucasVarity".

---

## 11. AMPLIACIÓN: Deutz EMR2 como posible base de la E-ECU Volvo CE 03161983 / 20577135

> Nota de alcance: esta ampliación se hizo con el presupuesto de búsquedas web ya agotado; sólo se usaron descargas directas de URL conocidas y los PDF ya obtenidos (ComAp, DEIF, Woodward). **No se consiguió ningún documento oficial Deutz** (Systembeschreibung EMR2 0297 xxxx, Schnittstellenbeschreibung CAN, pinout Fahrzeugstecker): deutz.com bloquea el acceso automatizado (BotStopper) y la documentación técnica Deutz está en el portal de servicio (SERPIC/Serviceportal, login). Las copias en Scribd no son legibles por herramienta. Se recomienda una segunda pasada con búsqueda web para: "EMR2 Systembeschreibung", "0297 7384", "EMR 2 Schnittstellenbeschreibung CAN", "EMR2 Fahrzeugstecker Belegung", "Deutz EMR2 Bedienungsanleitung 0297 9929".

### 11.1 Qué dicen las fuentes de controladores sobre Deutz EMR2 (MEDIA)
| Tema | ComAp (ECU-list 7.0.0 §3.6.2; Support 2015 p.61-63) | DEIF Omni 4189341306-K §6.5.3 | Woodward easYgen-1600 B37699A §7.1 |
|---|---|---|---|
| Motores | Deutz serie 1000 (10xx) con EMR2; **"Volvo EDC4 (EMR2) = D5, D7" → "follow Deutz EMR2 chapter"** | Deutz EMR 2 | Tipo de dispositivo **"30 Deutz EMR2 / Volvo EDC4"** (además "14 Volvo", "15 Volvo EMS2", "16 Volvo EMS2b", "17 Volvo EDC4") |
| Demanda de velocidad | **TSC1** ("Requested speed", SPN 898); salida analógica alternativa (SG OUT) | **TSC1**, dirección de control por defecto **3**; "Idle mode" ●; 50/60 Hz ● | TSC1 (J1939) |
| Start/Stop por CAN | Stop Request (propietario); "Lock status" (propietario); **sin start por CAN** | Start –; **Stop ● mensaje propietario "Engine Stop Request"** | Arranque por relé de arranque directo al solenoide; alimentación ECU por relé (pin 14, fusible 16 A) |
| Conector ECU | **"ECU 25pin F connector": CAN H = 12, CAN L = 13, Bat+ = 14, Bat– = 1**; Key switch, pot. "?" | — | **Conector F: 1 = batería negativo, 12 = CAN H, 13 = CAN L, 14 = alimentación batería vía relé (fusible 16 A)**; "impedance 120 Ω line recommended" |
| Parámetros SERDIA necesarios | **4400 = 1** (CAN activation), **4412 = 1** (activate TSC1a receive telegram), **4470 = 1** (CAN set point by TSC1a), **4829 = 8** (enable stop request telegram), **4900 = 8** (input channel type for nominal speed value sensor), **829 FunctEngineStop** (asignación interruptor "Engine stop"), **4424 TelStopRequestOn** (SAE J1939 engine stop request telegram) | — | — |
| Avisos | "Deutz does not recommend switching off the engine by removing the power supply (battery). It causes fault code SPN=536" | — | — |
| Códigos (SPN→texto) | 84, 91 APP, 98, 100, 102, 105, 108, 109, 110, 111, 171, 174, 190, 536 (oculto) | DM1/DM2 | — |

**Respuestas a las preguntas concretas (2):**
- **¿Acepta TSC1 (PGN 0)?** Sí, en los EMR2 configurados con SERDIA 4412/4470 ("TSC1a receive telegram"; "CAN set point by TSC1a") [CONFIRMADO ComAp; DEIF/Woodward lo usan]. **Direcciones fuente aceptadas**: DEIF usa por defecto SA **3**; ComAp no indica; **[NO ENCONTRADO]** la lista exacta de SA aceptadas en documentación Deutz. "TSC1a" sugiere que EMR2 distingue varios TSC1 por emisor (TSC1a/TSC1b…) **[INFERIDO]**.
- **¿PGN propietarios Deutz de demanda de velocidad?** No aparece ninguno en ComAp/DEIF/Woodward; la velocidad va por TSC1. Lo propietario es sólo el **"Engine Stop Request"** (telegrama de paro, parámetros 4829/4424) y "Lock status" **[CONFIRMADO en controladores; sin doc Deutz]**.
- **Entradas del conector de vehículo** (PWG analógico, acelerador manual, "Festdrehzahlen", selección de velocidad, paro): el parámetro **4900 "Selection of input channel type for nominal speed value sensor" (=8 para CAN)** confirma que existe una entrada de **sensor de valor nominal (PWG/potenciómetro)** conmutable con la consigna CAN; **829 FunctEngineStop** confirma una entrada digital de **paro de motor** asignable. Las entradas de **velocidades fijas** y el acelerador manual no aparecen en estas fuentes **[NO ENCONTRADO; requiere doc Deutz]**. Volvo Penta (nota 2003) confirma que EDC4 existe en variante "potenciómetro tradicional" y variante "CAN J1939".
- **Número de pines y correspondencia con el mapa Volvo (B1 CAN-H, B2 CAN-L, B25/B26 J1708, B9/B10 GND, B11/B12 +24 V, B4 emergency speed, B31 preheat, B5 heater feedback):** las tres fuentes describen el conector de vehículo del **EMR2 como "F connector" de 25 pines con CAN H/L en 12/13 y batería en 1/14** — **no coincide** con el mapa de 36 pines B1/B2 de la E-ECU Volvo. Esto indica que **la E-ECU 20577135 (2×36 pines) no es un EMR2 estándar**; si deriva del EMR2 sería un hardware/carcasa específico de Volvo **[INFERIDO]**. En cambio, el mapa Volvo (B1/B2 CAN, B25/B26 J1708, B31 relé precalentamiento, B4 velocidad de emergencia) encaja mejor con la familia Volvo EDC III (D12), cuyo "conector rojo" lleva CAN en 1-2 y relé de precalentamiento en 36 (el número 31 vs 36 difiere, lo que sugiere pinout propio del D6D) **[INFERIDO]**. Nota: para EMR2 el J1587/J1708 no se menciona en ninguna fuente; Volvo CE sí usa J1587 de respaldo → otro indicio de hardware Volvo.

### 11.2 Volvo Penta EDC3 / EDC4 / EMS según DEIF Omni 4189341306-K (MEDIA, 2024)
- §6.19.2 "Volvo Penta generic: **EDC 3, EDC 4 → TAD4x, TAD5x, TAD6x, TAD7x**": Start –, Stop –, **Speed control ● (TSC1, SA por defecto 3)**, Idle mode ●, 50/60 Hz ●, Shutdown override ●. Igual para §6.19.3 EDC 3 y §6.19.4 EDC 4 (sin start/stop por CAN).
- §6.19.5 "Volvo Penta EMS: **D6, D7, D9, D12, D16 (GE and AUX variants only)**": Start ●, Stop ●, Speed control ●, J1939 **TSC1 + propietario VP70**. §6.19.6 EMS 2.3 (EMS, EMS 2.0-2.3) y §6.19.7 EMS 2.4.
- §6.19.8/6.19.10: "If 'Volvo proprietary – Primary speed 50/60 Hz' is used, the controller disables standard J1939 speed control and uses the Volvo proprietary **VP70**… **the CAN bus ID for speed control is 0xCFF4611** (Volvo Penta proprietary telegram)"; cambio de frecuencia: apagar EMS, cambiar selección, encender y cambiar dentro de **10 s** de ignición, apagar/encender. Preheat: "the controller sends a preheat signal; the ECU determines whether preheating is needed".
- Woodward easYgen-1600 cableado: **Volvo EDC3 / TAD1240-1242**: conector "Stand alone" → **H = alimentación (fuel relay output), E = arranque, P = ECU power**; conector "Data bus" → **1 CAN H, 2 CAN L**; "preheating time ≥ 3 s". **Volvo EDC4 / TD520, TAD520 (opc.), TD720, TAD720 (opc.), TAD721, TAD722, TAD732**: conector F pines **1 (–), 12 CAN H, 13 CAN L, 14 (+ vía relé 30 A, fusible 16 A)**. **Volvo EMS2 / TAD734, TAD940/941, TAD1640-1642**: puerto CAN 8 pines **1 CAN H, 2 CAN L, 3 –, 4 +, 5 ECU power, 6 ECU stop**.
- Implicación: la nomenclatura DEIF ("Volvo Penta EMS: D6, D7… GE/AUX") muestra que Volvo Penta llama **"EMS"** (con VP70) a la 1ª generación de D12 y también a variantes D6/D7 GE/AUX, mientras que "EDC4" (=EMR2) no tiene start/stop por CAN **[CONFIRMADO en DEIF]**. Para la E-ECU D6D de Volvo CE (que sí recibe petición de rpm por J1939/J1587 desde la V-ECU) el modelo "EMS/EDC III con mensaje propietario" sigue siendo el más plausible **[INFERIDO]**.

### 11.3 SERDIA (software de diagnóstico Deutz) — EMR2
- Parámetros EMR2 citados por ComAp (ver tabla 11.1): 4400, 4412, 4470, 4829, 4900, 829, 4424 (páginas SERDIA 10/12/30/31). **[NO ENCONTRADO]** manual SERDIA público ni descripción de datasets EMR2. Volvo CE usa VCADS/Tech Tool ("Dataset EMR control unit programming") según la pista del coordinador; no verificado aquí.

### 11.4 Manuales descargables (ampliación) — carpeta /home/user/docs/manuales/deutz_emr2/
| Título | Nº pub. | Contenido relevante | Formato/tamaño | Gratis | ¿Abierto? | URL | Ruta local |
|---|---|---|---|---|---|---|---|
| DEIF Omni – Engine interface communication iE 250 / iE 350 | 4189341306-K | §6.5 Deutz EMR generic/EMR 2/3/4/5 (TSC1, SA 3, stop propietario); §6.19 Volvo Penta EDC3/EDC4/EMS/EMS2.3/2.4, VP70 0xCFF4611, procedimiento 50/60 Hz | PDF 161 p., 1,5 MB | Sí | Sí | https://www.deif.com/rtd/omni/eic (→ https://deif-cdn-umbraco.azureedge.net/media/vtaghavu/omni-engine-interface-communication-4189341306-uk.pdf) | /home/user/docs/manuales/deutz_emr2/DEIF_Omni_Engine_Interface_Communication_4189341306.pdf |
| Woodward easYgen-1600 Technical Manual | B37699A rev. D | Lista de ECU J1939 (Volvo, Volvo EMS2/EMS2b, Volvo EDC4, Deutz EMR2/Volvo EDC4); cableado por tipo de motor (pines F 1/12/13/14; EDC3 standalone H/E/P; EMS2 8 pines) | PDF 113 p., 9,3 MB | Sí | Sí | https://www.woodward.com/products/publication-asset/b37699a | /home/user/docs/manuales/deutz_emr2/Woodward_easYgen-1600_Technical_Manual_B37699A.pdf |
| ComAp Electronic Engines Support 08-2015 (ya listado) | — | Deutz EMR2 cap. p.61-63; Volvo EDC4 (EMR2) p.179; códigos EMR2 | PDF | Sí | Sí | https://grupofeynsa.wordpress.com/wp-content/uploads/2015/10/comap-support.pdf | /home/user/docs/manuales/volvo_penta_tad/ComAp_Electronic_Engines_Support_2015.pdf |
| ComAp ECU list 7.0.0 Global Guide (ya listado) | r3 | §3.6.2 EMR2 (p.76-78), §3.26.4 EDC4 (EMR2), §4.18 códigos EMR2 (p.304) | PDF | Sí | Sí | http://generator-info.com/ComAp/Control%20Panels/ECU-list-7-0-0-Global-Guide_r3.pdf | /home/user/docs/manuales/volvo_penta_tad/ComAp_ECU_List_7-0-0_Global_Guide_r3.pdf |
| Volvo Penta Manuel d'atelier Groupe 20-26 TD/TAD520-722 (EDC4) | — | sólo mecánica; esquemas pág. 131-135 son de arranque/paro básico sin la ECU EDC4 | visor 142 p. | Sí (visor) | Sí | https://www.manualslib.fr/manual/627509/Volvo-Penta-Td520Ge.html | — |
| Deutz EMR2 Systembeschreibung / Schnittstellenbeschreibung CAN / Fahrzeugstecker | 0297 xxxx | — | — | — | **No encontrado / no accesible** (deutz.com bloqueado; portal de servicio con login) | — | — |
| DEIF AGC-150/iE-150 Engine communication 4189341302 (Deutz) | 4189341302 | — | web | Sí | **503** repetido | https://documentation.deif.com/r/ie-150-agc-150-engine-communication-4189341302-uk/j1939-ecus-and-engines | — |

### 11.5 Esquemas extraídos (ampliación, prefijo emr2_) — /home/user/docs/esquemas/
| Imagen | Fuente | Qué muestra |
|---|---|---|
| emr2_ComAp2015_p61_Deutz_EMR2_signals.png | ComAp 2015 p.61 | Señales EMR2 (lámparas, Lock status, Stop Request) |
| emr2_ComAp2015_p62_Deutz_EMR2_Serdia_params_25pin_wiring.png | ComAp 2015 p.62 | **Parámetros SERDIA 4400/4412/4470/4829/4900/829/4424 y cableado conector F 25 pines (CAN H 12, CAN L 13, Bat+ 14, Bat– 1)** |
| emr2_ComAp2015_p63_Deutz_EMR2_wiring_cont.png | ComAp 2015 p.63 | continuación |
| emr2_DEIF_Omni_4189341306_p65_Deutz_EMR2_interface_TSC1_SA3.png | DEIF p.65 | Deutz EMR 2: Stop ●, Speed control ● TSC1, SA 3, Idle, 50/60 Hz, stop propietario |
| emr2_DEIF_Omni_4189341306_p142_VolvoPenta_EDC4_interface.png | DEIF p.142 | Volvo Penta EDC 4: sólo speed control TSC1 SA 3, sin start/stop CAN |
| emr2_DEIF_Omni_4189341306_p143_VolvoPenta_EMS_interface_VP70.png | DEIF p.143 | Volvo Penta EMS (D6, D7, D9, D12, D16 GE/AUX): start/stop/speed, TSC1 + VP70 |
| emr2_DEIF_Omni_4189341306_p146_VolvoPenta_speed_control_0xCFF4611.png | DEIF p.146 | Selección "Volvo proprietary", ID 0xCFF4611, procedimiento 50/60 Hz |
| emr2_Woodward_easYgen1600_p51_J1939_device_list_Volvo_EDC4_DeutzEMR2.png | Woodward p.51 | Lista de tipos de ECU J1939 |
| emr2_Woodward_easYgen1600_p84_Deutz_EMR2_VolvoEDC4_Fconnector_pins_1_12_13_14.png | Woodward p.84 | Cableado Deutz EMR2 / Volvo EDC4 (conector F) |
| emr2_Woodward_easYgen1600_p85_Volvo_EDC3_TAD1240_standalone_H_E_P_databus_1_2.png | Woodward p.85 | Cableado Volvo EDC3 TAD1240-42: standalone H/E/P, data bus 1/2 |
| emr2_Woodward_easYgen1600_p86_Volvo_EDC4_and_EMS2_8pin_wiring.png | Woodward p.86 | Cableado Volvo EDC4 (F 1/12/13/14) y EMS2 (8 pines) |

### 11.6 Conclusión de la ampliación
- **Confirmado**: EMR2 (y Volvo EDC4) se gobierna por **TSC1** (SA por defecto 3 en DEIF) tras habilitar por SERDIA (4400/4412/4470); paro por telegrama propietario Deutz; **sin arranque por CAN**; conector de vehículo "F" **25 pines** con CAN en 12/13 y batería en 1/14.
- **Inferido**: el mapa de 2×36 pines de la E-ECU Volvo (B1/B2 CAN, B25/B26 J1708, B31 precalentamiento) **no corresponde al conector EMR2 estándar**; o la E-ECU 20577135 es un derivado Volvo-específico del EMR2 (hardware distinto) o pertenece a la familia Volvo EDC III/EMS (más coherente con J1587 de respaldo y con la petición de rpm propietaria por J1939 que usa Volvo CE). La captura CAN en la máquina sigue siendo imprescindible; si la E-ECU respondiera a TSC1 desde SA 3/0x11 sería un indicio de base EMR2; si sólo responde a un PGN propietario (p.ej. 0xFF46 "VP Status"), de base Volvo EMS.
- **No encontrado**: documentación oficial Deutz EMR2 (pinout completo del Fahrzeugstecker, lista de SA aceptadas para TSC1, entradas de velocidades fijas/PWG/acelerador manual), manual SERDIA, documentos DSE para Deutz EMR2/Volvo.
