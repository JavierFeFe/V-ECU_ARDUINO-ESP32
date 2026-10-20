# Sustitución/emulación de la V-ECU — Volvo EC210B (motor D6D EAE2)

**Documento de investigación consolidado** · Fecha: 2026-10-19

| | |
|---|---|
| Máquina | Volvo EC210B (LC), excavadora de cadenas, generación "B" |
| Módulo a sustituir | **V-ECU** (Vehicle ECU), MID 187 |
| Módulo con el que hay que dialogar | **E-ECU / EMS** del motor, etiqueta "VOLVO VCE56003584 D6D EAE2 — S/N E00747373", MID 128 |
| Situación actual | La máquina funciona **sin V-ECU**, con el selector Auto/Manual en **Manual** y el interruptor de régimen de emergencia en **alta** |
| Objetivo fase 1 | **Regular la potencia** (bomba hidráulica y/o régimen del motor) con un **ESP32/Arduino** y un potenciómetro o encoder |
| **Estado actual** | Alcance reducido a **control de rpm** (parte hidráulica aplazada). Placa **ESP32_Relay X1 V1.2** con relé confirmado en GPIO16, módulo CAN **Adafruit CAN Pal** (G17/G18, SLNT en G4) y **firmware v0.1** grabado y verificado en banco (modos Reposo / Alto / Auto-ralentí, J1939 en solo escucha, TSC1 bajo flag). Ver [`CONTROL_RPM.md`](CONTROL_RPM.md), [`MONTAJE.md`](MONTAJE.md) y [`../firmware/README.md`](../firmware/README.md) |

> **Nota sobre la referencia del módulo.** "D6D EAE2" es el motor: Volvo D6D, 6 cilindros, 5,7 l, Tier 2/Stage II, derivado de Deutz 2012 con bombas unitarias. Por tanto el módulo **VCE56003584 es la ECU del motor (E-ECU/EMS)**, no la V-ECU. La V-ECU es la centralita de la máquina: modos de trabajo, bomba, auto-ralentí, etc. Además le pide el régimen a la E-ECU por el bus. La referencia "VCE56003584" **no aparece en ninguna fuente pública**. Lo más probable es que sea un número de conjunto o de software de Volvo CE. Para identificarla con certeza hay que leer MSW/DST1/DST2 con VCADS Pro.

### Identificación física de la E-ECU (foto del usuario, 2026-10-19)

| Etiqueta | Contenido | Interpretación |
|---|---|---|
| Placa del fabricante del hardware | "VOLVO — *A Product developed in partnership with LucasVarity*" · **03161983 P03** · 80907C · *Made in UK* · código de barras 03161983 / **00317121** / **2702** | **Hardware Volvo EMS desarrollado con LucasVarity (Reino Unido; después Delphi)** · n.º de pieza Volvo 03161983, revisión P03 · n.º de serie del hardware 00317121 · fecha de fabricación probable: **semana 27 de 2002** |
| Superior (programación del motor) | Código de barras **E00747373** · **VCE56003584** · **D6D EAE2** · VOLVO **05.08.02 07:25** | Identificador de programación o de dataset para el motor D6D EAE2 · fecha **5 de agosto de 2002** si el formato es DD.MM.AA (encaja con la semana 27 de fabricación) o 8 de mayo si es MM.DD.AA |
| Inferior (programación para la máquina) | Código de barras · **EC210** · **010828** · VOLVO **10.23.02 08:04** | Modelo de máquina · **probable n.º de serie o de producción de la máquina (10828)** · **23 de octubre de 2002** (formato MM.DD.AA, porque 23 no puede ser un mes) |

- **Equivalencias de la pieza 03161983** (vendedores, BAJA pero coincidentes): **60100002 / 20577135**. Se usa en el **motor D6D de EC210B, EC160B, EC180B, EC240B y EC290B, en las cargadoras L90E, L110E/F, L120E, L160E y L170F/L190F y en la motoniveladora G710B**.
  - Por tanto es la E-ECU **estándar de la serie B** y la documentación de la EC210B aplica.
  - **Las cargadoras L90E/L120E comparten E-ECU**, así que sus manuales y foros son otra fuente útil.
  - Fuentes: [FridayParts](https://www.fridayparts.com/controller-ecu-03161983-for-volvo-engine-d6d-excavator-ec210b-ec210blc-ec290blc-wheel-loader-l90e-l120e-l110f-l160e-l190f-l170f), [eBay 314128098470](https://www.ebay.com/itm/314128098470), [sinocmp](https://sinocmp.com/products/voe-3161983-volvo-ec240b-ec210b-ecu), [hrparts](https://www.hrparts.com/3161983-engine-control-module-volvo-l90e).
- **Fabricante del hardware: LucasVarity** [CONFIRMADO por la placa]. Era la primera generación del EMS de Volvo, antes de la EMS2. **No se ha encontrado documentación pública** que relacione la pieza con LucasVarity.
- **Conectores** (foto): **dos conectores iguales de 36 pines** (3 filas × 12), uno junto a otro. Corresponden a los conectores A (motor) y B (máquina) de la lámina ENG7-06, con pines numerados hasta el 36. Marca de los conectores **sin identificar**: hace falta una foto de los conectores del mazo, con el cierre y las marcas.
- **Carcasa:** de aluminio fundido con aletas de refrigeración, para montaje en el motor o el chasis, con los conectores en el lateral.
- **Implicaciones [INFERIDO]:**
  - La máquina es de **finales de 2002**, una de las **primeras unidades** con el motor Volvo D6D. Volvo da como producción de la EC210B 2003–2009 ([Volvo CE](https://www.volvoce.com/global/en/products-and-services/past-products/crawler-excavators/volvo-b-prime-series/ec210b/)).
  - El manual del operador usado como fuente principal cubre los **números de serie 14132 en adelante**. Si la máquina es la 10828, **es anterior** a ese manual, y algunos valores pueden diferir: tablas de mA y rpm, versión de la V-ECU, quizá el cableado.
  - Volvo avisa de que, al sustituir una V-ECU antigua, hace falta el "conversion kit" de VCADS Pro (EC330B p.65).
  - **Hay que confirmarlo con la placa de la máquina.**
- La etiqueta "EC210 010828" implica que la E-ECU **se programó para esa máquina concreta**. Si en algún momento se sustituye, hará falta reprogramar con VCADS Pro.

### Actualización 2 — hallazgos tras identificar la E-ECU (2026-10-19, tarde)

**1. Familia de hardware confirmada [ALTA].** La E-ECU 03161983 P03 "LucasVarity, Made in UK" tiene **el mismo pinout de dos conectores de 36 pines** que la EECU de los camiones Volvo D12B/D12C "Vectro II" (manual Volvo Trucks PV776-144528, 2001) y que el circuito "EECU Electric Circuit EC160B-290B" del boletín Volvo CE **UPDATE EC160B~460B** (2004). Cadena de fabricantes: Lucas → LucasVarity (1996) → TRW (1999) → Delphi Diesel Systems. Mismo hardware con los números 3161962, 20577131, 20582958, 20412506, 8170700 y Volvo Penta 20582963 (EDC III/EMS del D12). "P03" = revisión de hardware; "VCE56…" = identificador de software/dataset de Volvo CE (inferido). Detalle en el [Anexo D](anexos/D_familia_LucasVarity_D12.md).

**2. Pinout de la E-ECU, conector B (lado máquina) — CONFIRMADO por el circuito OEM:** B1 CAN H, B2 CAN L, B25/B26 J1708 A/B, B9/B10 masa, B11/B12 +24 V (vía relé R3 "EMS power" y F15), **B4 "Emergency speed control"**, B31 relé de precalentamiento, B5 bobina de precalentamiento, B7/B17/B8/B3/B13 sensores, **B24 línea EOL/programación**. **No hay pin de llave:** la E-ECU recibe la posición de la llave por J1939 desde la V-ECU. En el camión, **B4 es la entrada "idle validation": < 4 V = ralentí, > 8 V = acelerado**; en la excavadora la alimenta el interruptor de emergencia a través de F24 (terminal 3 del interruptor → B4). Es una entrada de **dos estados**.

**3. Pinout de la V-ECU — CONFIRMADO por la página "Control Circuit (EC160B~EC460B)" del mismo boletín** (`esquemas/ce_EC-B_UPDATE_p06_control_circuit_300dpi.png`). Resumen de los pines útiles:

| Función | Pin V-ECU |
|---|---|
| +24 V desde fusibles V-ECU | JB7, JB8 |
| Masa | JA15, JA63 (GND); JA14 (GND del dial) |
| "VECU operating power" → selector Auto/Manual | JB15 (term. 1), JB16 (term. 2) |
| Llave START (R2) / ON (ACC) | JB2 / JB9 |
| J1939 (derivación del par E-ECU ↔ panel) | **JB14 = H, JB6 = L** |
| Mallas de los cables J1587 / J1939 | JB13 / JB5 (no son CAN) |
| J1587 | JB12 = A, JB4 = B |
| Dial de régimen | JB11 (+24 V), **JA39 (0,5–4,5 V)**, JA14 (GND) |
| Válvula power shift | **JA32 "Power shift Signal" (+)**, **JA5 "P/Shift Ground" (low-side PWM)** |
| Válvula de caudal X1 | JA56 (señal), JA30 (masa) |
| Salida "VECU STATUS" al panel | JA34 |
| Alimentación de solenoides | JA60, JA35 |
| Power boost / conflux cut-off / flotación / velocidad traslación | JA36 / JA37 / JA59 / JA38 |
| Presostatos (traslación, implemento, martillo, flotación) | JA43, JA19, JA66, JA17 |
| Auto-ralentí / P-Max / confirmación / buzzer stop | JA67 / JA44 / JA42 / JA16 |
| Relé de batería / alternador "L" | JA61 / JA7 |

Corrige la deducción anterior (JB13/JB14 = CAN): **CAN H = JB14, CAN L = JB6**. **Revisado con el esquema a 300 ppp (2026-10-20):** JB13 y JB5 no son un segundo par CAN, sino las **mallas** de los cables J1587 y J1939 (elipses discontinuas). El par de la E-ECU (EB1/EB2) y el del panel (1/2) se empalman en el mazo y siguen hasta JB14/JB6: la V-ECU es una **derivación**, no un nodo de paso. Sin ella, la E-ECU y el panel siguen unidos; **no hay que puentear nada** (un puente JB13↔JB14 o JB5↔JB6 uniría CAN a las mallas).

**4. Circuito del selector Auto/Manual (6 terminales) — CONFIRMADO:** AUTO cierra 1–2 y 4–5; MANU cierra 2–3 y 5–6. Terminal 1 = JB15; 2 = JB16 y señal "A/M position" al panel; 3 = válvula (+) y JA32; 4 = JA5; 5 = válvula (−); 6 = Resistor Box → masa. En AUTO la V-ECU regula la válvula por el **lado de masa (JA5)**; en MANU la válvula se alimenta a 24 V por el terminal 2–3 y retorna por 6 → Resistor Box (≈60 Ω → ≈340 mA). **Nuestro driver se intercala entre el terminal 6 y masa.** Tabla completa y esquema en [`ESQUEMA_CONEXION.md`](ESQUEMA_CONEXION.md).

**5. Terminaciones del bus:** en la L120E (misma E-ECU) la resistencia R702 de 120 Ω está **dentro del panel I-ECU** y la otra en la E-ECU (**confirmada: 117 Ω** entre B1 y B2 de la E-ECU suelta, 2026-10-20). El emulador **no** debe añadir terminación si B1–B2 da ≈60 Ω en la máquina; si da ≈120 Ω, el panel MDU de esta máquina no termina el bus y sí hay que añadirla.

**6. Interruptor de emergencia (3 posiciones, 6 terminales):** F24 alimenta el terminal 2. STOP: 1–2 y 4–5; ralentí: 1–2 y 5–6; alto: **2–3** y 5–6 → el terminal 3 lleva +24 V a **B4**. El contacto 4–5 de STOP actúa sobre los relés R3/R4 (EMS power / EMS data record) para parar el motor.

**7. Volvo Penta TAD650VE–760VE NO es la misma centralita** (son common-rail EMS2, conectores de más de 36 pines). La familia Penta equivalente es la **EDC III / EMS del D12** (TAD1240–1242GE, ECU 20577134), cuya documentación sí aplica: manual de instalación con potenciómetro directo a la ECU en versión "standalone", CIU por CAN, parámetros de ralentí y droop. [Anexo E](anexos/E_volvo_penta_deutz_emr2.md).

**8. Pista Deutz EMR2:** boletines Volvo llaman a esta E-ECU "EMR control unit" y hablan de un servidor "EMR2" para los datasets. Pero la EMR2 estándar de Deutz tiene un conector de vehículo de **25 pines** (1 = bat −, 12 = CAN H, 13 = CAN L, 14 = bat +) y no usa J1587, así que la E-ECU Volvo es, como mucho, un derivado específico. La EMR2 estándar acepta **TSC1 (SA 3)** una vez habilitado con SERDIA (parámetros 4400/4412/4470/4900) y tiene entrada de pedal analógico conmutable con CAN. La descripción del sistema EMR2 (Deutz 0297 9885, 60 p.) está descargada en `manuales/deutz_emr2/`. **Conclusión** ([Anexo H](anexos/H_deutz_emr2.md)): la EMR2 de Deutz tiene **2 conectores AMP de 25 polos** (F vehículo / M motor) y su conector M está pensado para actuador de cremallera, no para bombas unitarias; **no existe ninguna variante EMR2 de 2×36 pines**, así que la E-ECU Volvo es hardware propio (LucasVarity) que, como mucho, comparte la familia de firmware/datasets "EMR". Lo que sí es extrapolable: J1939 a 250 kbit/s, consigna por **TSC1** (SA 3 por defecto en los controladores de grupos), paro por telegrama propietario, y al perder la consigna CAN conmuta a pedal o a una "velocidad auxiliar" configurable. En la EMR2 estándar un potenciómetro directo (F25/F24/F23, 1 kΩ o 0,5–4,5 V) sí es posible si el dataset lo activa; en la E-ECU Volvo **no hay indicios** de que el dataset lo admita.

**9. Programación:** la E-ECU se programa con un **dataset descargado por número de serie del motor** y cargado con VCADS Pro (op. 28423-3); en las máquinas tempranas sin línea de programación en el mazo hay que pedir la unidad "fully pre-programmed". Ningún indicio de emparejamiento antirrobo E-ECU↔V-ECU; el **Code Lock** es opcional, se programa con VCADS y actúa por CAN (petición "SHUTDOWN" del panel a la E-ECU). El salto de serie **14132** corresponde a la introducción del panel I-ECU; la máquina del proyecto (≈10828) lleva el MDU anterior (MID 140, SA 23) y es la que describen las láminas "EC210/160B" de Volvo CE Korea. [Anexo F](anexos/F_L90E_L120E_misma_EECU.md).

**10. Conectores (dónde comprar):** [Anexo G](anexos/G_conectores_compra.md). Resumen: la familia de los conectores de 36 vías de la E-ECU y de los JA/JB de la V-ECU **no se ha podido identificar** (no hay kit de reparación Volvo público). Vías prácticas: pigtail aftermarket de la E-ECU (SINOCMP, ≈259 US$ el par) o del mazo motor; contraconector JA/JB de la V-ECU con cable en eBay (≈164 US$ + envío, ítems 384979664114 / 375584859654) o Amazon (SINOCMP B06W9JF7XT); fotografiar el número moldeado y pedir "repair terminal" al concesionario. La válvula Kawasaki KDRDE5K usa **TE Econoseal J Mark II**: carcasa 174352-2 + terminales 173707-1 + juntas 1-172888-3 (RS/Farnell, < 2 €). La toma de servicio de 8 pines **no lleva CAN** (solo J1587 y alimentación). Genéricos: SN65HVD230 (≈5 €) o TJA1051T/3 (≈1,5 €), kits Deutsch DT (≈40 €), caja IP67 (≈15 €).

**Manuales descargados en el proyecto** (`docs/manuales/`, ≈160 MB, todos PDF verificados):
- `volvo_trucks_d12/` (31): **Volvo_EC160B-EC460B_Service_Manual.pdf** (= boletín UPDATE EC160B~460B, 31 p., con los circuitos OEM de V-ECU y E-ECU), **Volvo_TSI_Vectro_II_Vehicle_Management_System_PV776-144528.pdf** (250 p., pinouts EA/EB/VECU del camión), Volvo_J1939_J1708_Datalink_Fault_Tracing.pdf, manuales D12, esquemas FH12/VN, body builder, códigos MID 128/144.
- `volvo_ce/` (5): manual del operador EC210B (ser. 14132-), muestra del manual de taller EC210B LC, **esquemas L120E Sch01–Sch100** (misma E-ECU), folletos.
- `volvo_penta_tad/` (11): especificación de interfaz CAN Volvo Penta EMS 47706587, guías ComAp 2015/2019, demo del manual de taller TAD650–760VE, hojas técnicas, manual YDEG-04.
- `deutz_emr2/` (10): **Deutz EMR2 System Description 0297 9885**, DEIF Omni / AGC, Woodward easYgen, ComAp, manual EDC4.
- Esquemas extraídos como imagen: `docs/esquemas/` (prefijos `ce_`, `d12_`, `penta_`, `emr2_`).

Los informes detallados, con todas las fuentes, están en los anexos:
- [Anexo A — Arquitectura eléctrica, pinouts, modo emergencia, bomba, hardware de potencia](anexos/A_arquitectura_electrica.md)
- [Anexo B — Protocolos J1939 / J1587, TSC1, mensajes, códigos, ESP32/Arduino CAN](anexos/B_protocolos_comunicacion.md)
- [Anexo C — Foros, averías típicas, reparación, conectores, uso en manual](anexos/C_foros_averias_reparacion.md)
- [Anexo D — Familia LucasVarity / Volvo D12 EECU, pinouts de camión, TSC1 en Volvo](anexos/D_familia_LucasVarity_D12.md)
- [Anexo E — Volvo Penta EMS/EDC III y Deutz EMR2, controladores de grupos](anexos/E_volvo_penta_deutz_emr2.md)
- [Anexo F — L90E/L120E/EW-B con la misma E-ECU, programación, saltos de serie](anexos/F_L90E_L120E_misma_EECU.md)
- [Anexo G — Conectores: identificación y dónde comprarlos](anexos/G_conectores_compra.md)
- [Anexo H — Deutz EMR2: documentación, pines F/M, CAN, SERDIA](anexos/H_deutz_emr2.md)
- [Esquema de conexión ESP32/Arduino](ESQUEMA_CONEXION.md)

---

## 0. Criterio de fiabilidad

| Nivel | Significado |
|---|---|
| **ALTA** | Documento OEM de Volvo (manual del operador EC210B, manual de servicio, training EC330B en manualslib), especificación oficial Volvo Penta, norma SAE o fabricante del componente. |
| **MEDIA** | Documento OEM reconstruido. Algunas láminas de training de Volvo CE Korea están en Scribd con fuente cifrada y se descifraron; las asignaciones de pines se dedujeron del orden del texto. También entran aquí los fabricantes de controladores y varios terceros que coinciden. |
| **BAJA** | Un solo post de foro, JustAnswer, anuncios de vendedores, blogs de códigos. |

Cada dato importante lleva la etiqueta: **[CONFIRMADO]**, **[INFERIDO]** (deducido, hay que verificarlo en la máquina) o **[NO ENCONTRADO]**.

**Fuentes principales:**
- Manual del operador EC210B (ALTA): https://www.tractorparts.com/PDFs/VOLVO_EC210B_OPERATIONS_MANUAL.PDF y https://www.manualslib.com/manual/1664987/Volvo-Ec210b.html
- Training de servicio EC330B, misma generación B (ALTA): https://www.manualslib.com/manual/1639294/Volvo-Ec330b.html
- Training Volvo CE Korea:
  - EC210B-04 "Electronic Control System" (MEDIA): https://www.scribd.com/document/461665933/EC210B-04
  - EC210/160B-ENG7 "Engine control system" (MEDIA): https://www.scribd.com/document/428476774/Pages-from-EC210B-ENG-7-pdf
  - EC210B-10 "Main pump" (MEDIA): https://www.scribd.com/document/461665854/EC210B-10
- Páginas de muestra del manual de servicio EC210B LC, "Current/pressure specifications" (ALTA): https://www.aservicemanualpdf.com/Samplepages/SM-Volvo%20EC210B%20LC%20Excavator%20Service%20Repair%20Manual.pdf
- Volvo Penta *Electrical Interface Specification* EMS, doc. 47706587 (ALTA para Volvo Penta, aplicabilidad INFERIDA): https://www.marinpro.com/Cms_Data/Contents/powerhouse/Folders/Accessories/AccessoryFiles/~contents/4YD2DR3WYE3MEBNA/OpenCAN_InstallGuideline_rev_1.pdf

---

## 1. Resumen ejecutivo

1. **El modo de emergencia de fábrica no usa la V-ECU** [CONFIRMADO, ALTA/MEDIA]. Lo forman tres elementos:
   - **Selector 25 Auto/Manual.** El manual dice: *"If the V-ECU malfunction, this switch must be switched to Manual"*. Este selector decide de dónde le llega la corriente a la válvula de la bomba:
     - En **Auto**, desde la V-ECU.
     - En **Manual**, desde una **"Resistor Box" de unos 60 Ω** que da unos **340 mA fijos**. Volvo dice que eso equivale al *"85 % of the maximum pump input torque"*.
   - **Interruptor 26 de régimen de emergencia**, cableado **directamente a la E-ECU** (pin B4, "Emergency speed control") y protegido por el fusible **F24 de 5 A**. Tiene tres posiciones:
     - neutral: **800 rpm**;
     - arriba: **1900 rpm**;
     - abajo durante más de 2–3 s: **parada del motor**.

     Los dos regímenes son parámetros de la E-ECU que se cambian con VCADS Pro. **Por esa entrada no hay regulación continua.**
2. **Válvula de potencia de la bomba ("power shift", PPID 1190, código ER31).** **A más corriente, menos potencia absorbida por la bomba**: P 215 mA → I 555 mA. A **0 mA** la bomba tiene **la máxima absorción**, más incluso que en modo P [CONFIRMADO, ALTA].
3. **Posible avería en tu máquina** [INFERIDO]. Según Volvo, en emergencia alta la bomba debería quedar limitada (340 mA, entre G1 y F1), **no a la máxima potencia**. Si la máquina "va a tope" o el motor se ahoga con carga, comprueba en este orden: la Resistor Box, el fusible F24, los contactos del selector Auto/Manual (a menudo corroídos) y el conector de la válvula. **Lo primero es medir la corriente en serie en la válvula.**
4. **Vía más sencilla y segura para regular la potencia: controlar la corriente de la válvula de la bomba** con el ESP32 (driver de corriente regulada de 200 a 600 mA), en lugar de la Resistor Box.
   - No toca el CAN ni el motor y reproduce exactamente lo que hacía la V-ECU (tabla del §3).
   - Si además se lee el régimen del motor por J1939 (mensaje EEC1, en modo solo escucha), se puede programar el **control anti-calado (ESSPC)** de la V-ECU: subir la corriente cuando las rpm caen con carga.
5. **Regular el régimen del motor de forma continua** solo es posible **por J1939**, enviando la petición de régimen que normalmente manda la V-ECU [CONFIRMADO que existe; formato INFERIDO]. Indicios:
   - El training de la EC210B asigna a la **V-ECU la dirección J1939 SA 17 (0x11)** (MEDIA).
   - Volvo Penta EMS acepta **TSC1 (PGN 0)** precisamente desde **SA 0x11** ("OEM controller") o 0x03, cada 10 ms (ALTA para Penta).
   - Juntos, estos dos datos hacen muy probable que la V-ECU use TSC1 desde 0x11. **Hay que confirmarlo en la máquina** (plan en el §7).
6. **Inmovilizador o autenticación V-ECU↔E-ECU: no hay ninguna prueba de que exista** [NO ENCONTRADO]. El "Code Lock" antirrobo se guarda en la V-ECU, y en modo Manual el motor arranca, como ya ocurre en tu máquina. En modo Auto sin V-ECU, la E-ECU registra un fallo de comunicación (**PSID 201-09 / SID 231**) porque no recibe los mensajes periódicos de la V-ECU.
7. **No existe ningún emulador público de V-ECU, ningún DBC de Volvo CE ni un pinout completo publicado** [NO ENCONTRADO]. Habrá que medir en la máquina.

---

## 2. Arquitectura eléctrica de la EC210B

### 2.1 Unidades de control y bus

| Unidad | Función | MID (J1587) | SA (J1939) | Fiab. |
|---|---|---|---|---|
| **E-ECU / EMS** | Motor D6D EAE2: inyección por bombas unitarias con electroválvula, precalentamiento, entrada de régimen de emergencia | 128 | 0 (0x00) | ALTA (MID) / MEDIA (SA) |
| **V-ECU** | Modos de trabajo, control de bomba (ESSPC), auto-ralentí, power boost, traslación, arranque y parada seguros, registro de datos, "Code Lock" | 187 | **17 (0x11)** | ALTA (MID) / MEDIA (SA, lámina EC210B-04-01) |
| **I-ECU / MDU** (panel con pantalla) | Testigos, pantalla de mensajes, códigos ER | 140 | 23 (0x17) | ALTA / MEDIA |
| W-ECU (telemática, si la lleva) | – | 142 | ? | MEDIA |
| Herramientas (VCADS Pro / SDU / MATRIS) | Toma de servicio | 172 | – | MEDIA |

- **Dos buses** [CONFIRMADO, ALTA, training EC330B p.20]:
  - **SAE J1939 (CAN)**: "control link", control rápido entre ECUs.
  - **SAE J1708/J1587 (RS-485, 9600 bit/s)**: "information link", información y diagnóstico. También funciona como respaldo.
- **J1939 a 250 kbit/s con identificadores de 29 bits**: confirmado en camiones Volvo y Volvo Penta; **inferido** para la EC210B. Hay que verificarlo con el analizador en modo solo escucha.
- **Terminación 120 Ω × 2**: una está **dentro de la E-ECU** (medidos 117 Ω, 2026-10-20); la otra, según el esquema L120E, en el panel. Medición pendiente en la máquina: con todo apagado, entre CAN-H y CAN-L.
  - **≈60 Ω**: bus correcto.
  - **≈120 Ω**: falta la segunda terminación (el panel MDU no la lleva o no está en el bus) y **el emulador debe llevar 120 Ω**.
- **Qué intercambian V-ECU y E-ECU** (lámina ENG7-08, MEDIA; EC330B p.66, ALTA):
  - De V-ECU a E-ECU: señal de arranque y **"Engine speed (Request value)"**.
  - De E-ECU a V-ECU: régimen real y señal de error.
  - El dial de régimen va a la V-ECU, no a la E-ECU.

### 2.2 Alimentación, fusibles y relés (manual del operador p.181–183, ALTA)

- Sistema de **24 V**: 2 baterías de 12 V y 150 Ah, alternador de 28 V y 80 A.
- Fusibles:

  | Fusible | Valor | Circuito |
  |---|---|---|
  | F1 | 10 A | I-ECU |
  | F13 | 10 A | V-ECU |
  | F25 | 10 A (OCR dudoso) | V-ECU |
  | F15 | 20 A | E-ECU |
  | **F24** | **5 A** | **"Engine RPM manual control"** (interruptor de emergencia) |

- Relés en la caja (MEDIA): **R3 "EMS power"**, **R4 "EMS data record"**. Según los foros, R3/R4 son una causa frecuente de fallos de alimentación de la E-ECU.
- La "Resistance box for emergency pump control" está en la caja eléctrica (EC330B p.57, ALTA).

### 2.3 V-ECU

| Dato | Valor | Fiab. |
|---|---|---|
| Referencias (familia EC140B–EC700B) | 14518349 (equivalentes 14514090, 14531360, 14594697) | BAJA (vendedores) |
| 14390065 | **No es V-ECU**: aparece como I-ECU/monitor o su conector | BAJA (coinciden todas las fuentes) |
| Ubicación | Detrás del asiento o pared derecha de la cabina, junto a la caja del climatizador | ALTA (EC330B) / BAJA (foro EC210B) |
| Conectores | **JA de 70 pines + JB de 16 pines** | ALTA (EC330B p.65) |
| Marca de los conectores | **[NO ENCONTRADO]**: hay que identificarla físicamente | – |
| Fabricante del hardware | **[NO ENCONTRADO]** | – |
| Programación | Una V-ECU nueva viene **vacía** y se programa con VCADS Pro según el número de serie de la máquina ("non-programmed / pre-programmed, replacing") | MEDIA-ALTA |

**Pinout parcial probable** (MEDIA-BAJA, **verificar con polímetro antes de conectar nada**):

| Pin | Señal probable | Origen del dato |
|---|---|---|
| JB7, JB8, JB15, JB16 | +24 V (rojo) y masa (negro) | Foro + esquema EC210B-04-03 |
| JB13 / JB14 | J1939 CAN-H / CAN-L — **superado**: CAN H = JB14, CAN L = JB6; JB13/JB5 son mallas (§3) | Esquema EC210B-04-03 (orden del texto) |
| JB6 / JB12 | J1587 A / B | Ídem |
| JA39 | Señal del dial de régimen (0,5–4,5 V) | Lámina EC210B-04-18 y fragmento |
| JA56 | Salida de la válvula de control de caudal (X1) | Lista de códigos (BAJA) |
| JA14 / JA15 | Masas | Lista de códigos (BAJA) |
| Salida de la válvula power shift | **[NO ENCONTRADO]** | – |

**Dial de régimen** (EC210B-04-18, MEDIA): 4 pines.
- Pines: 1 alimentación (probablemente 5 V de referencia), 2 señal, 3 masa, 4 malla.
- Señal lineal: **0,5 V en el paso 1, 2,5 V en el paso 5 y 4,5 V en el paso 9**.
- **Dato útil:** el dial original puede reutilizarse como entrada del ESP32, con un divisor hasta 3,3 V.

### 2.4 E-ECU (EMS) del D6D EAE2

- Dos conectores: **A** (motor: sensores e inyectores) y **B** (máquina). Posiblemente 2 × 36 vías, sin confirmar (MEDIA).
- Pines del conector B (MEDIA, deducidos de los diagramas):

  | Pin | Señal |
  |---|---|
  | **B1** | J1939 CAN-H |
  | **B2** | J1939 CAN-L |
  | **B25** | J1708 A |
  | **B26** | J1708 B |
  | **B4** | **Emergency speed control**, entrada del interruptor 26 a través de F24. **No se sabe qué tipo de señal es**: hay que medirla. |
  | B9/B10 | Masa probable (BAJA) |
  | B11/B12 | Alimentación probable, vía F15 y R3 (BAJA) |

- **Entrada analógica de acelerador: no aparece** en el diagrama OEM [NO ENCONTRADO].
- Regímenes: ralentí 800 ± 40 rpm y máximo en vacío 2000 ± 40 rpm. Potencia neta 145 PS a 1900 rpm (ALTA).
- Referencias de recambio que circulan (BAJA, contradictorias): 60100000/60100002, 03161983, 20577131/20582958. Son de la misma familia que las EMS2 de Volvo Penta, lo que apoya (sin confirmar) usar la especificación de Penta como referencia de protocolo.

---

## 3. Bomba: válvula proporcional "power shift" (la palanca más fácil)

**Bomba:** Kawasaki **K3V112DT**, doble, de pistones axiales, 2 × 200 l/min, 330/350 kgf/cm² (normal/power boost) [ALTA].

**Principio** (EC330B p.61, ALTA): la válvula proporcional genera una presión secundaria proporcional a la corriente. Esa presión llega al regulador de la bomba y **reduce el par absorbido**. Además, *"the spool vibrates continuously"*, es decir, **necesita dither**.

**Tabla de modos de la EC210B** (mercado no-USA; manual del operador p.61–63 con tolerancia ±10 mA y manual de servicio con ±20 mA; ALTA):

| Paso del dial | Modo | rpm vacío / carga | Corriente (mA) | P. secundaria (kgf/cm²) |
|---|---|---|---|---|
| 9 | P (P/Max) | 2000 / 1900 | 215 (variable) | 3,8 |
| 9 | H | 1900 / 1800 | 250 (variable) | 5,8 |
| 8 / 7 / 6 | G1 / G2 / G3 | 1800 / 1700 / 1600 | 290 (variable) | 8,1 |
| 5 / 4 / 3 | F1 / F2 / F3 | 1500 / 1400 / 1300 | 450 (fija) | 19,8 |
| 2 / 1 | I1 / I2 | 1000 / 800 | 555 (fija) | 28,5 |
| Emergencia alta | – | 1900 | **340** (Resistor Box) | – |
| Emergencia baja | – | 800 | 340 (Resistor Box) | – |

- **USA:** sin modo P. H 220, G1 260, G2/G3 300, F 450, I 570 mA.
- Una segunda tabla del manual de servicio da valores algo distintos: P 215, H 245, G1 275, G2/G3 320, F1 505, I1 595 mA. Los valores finales se ajustarán midiendo en la máquina.
- "(variable)" significa que en P, H y G la V-ECU **sube** la corriente cuando la carga hace caer el régimen. Es el **ESSPC**, el control anti-calado.

**Bobina** [INFERIDO]: probablemente una Kawasaki **KDRDE5K**.
- Especificación del fabricante: **0–0,7 A a 24 V** y unos **17,5 Ω a 20 °C** (Kawasaki, ALTA/MEDIA).
- Dos usuarios midieron unos 17–17,5 Ω (BAJA).
- Encaja con la cuenta: 26 V / (60 + 17,5 Ω) ≈ 340 mA.
- **Medir antes de diseñar.**
- **Frecuencia de PWM y dither de Volvo: [NO ENCONTRADO].** Valores genéricos: dither de 100 a 250 Hz con amplitud de ±5–10 %.

---

## 4. Protocolo: cómo se pide el régimen al motor por J1939

### 4.1 TSC1, PGN 0 (candidato principal)

Fuente: especificación Volvo Penta EMS 47706587 (ALTA para Penta). Formato SAE J1939-71, confirmado también por el documento CAN de Hatz.

| Campo | Valor |
|---|---|
| ID de 29 bits | **0x0C000011** (prioridad 3, PGN 0, destino 0x00, SA 0x11). Alternativa: 0x0C000003 |
| Periodo | **10 ms**, sin interrupciones |
| Byte 1 | SPN 695, modo de override: `01` = control de velocidad. SPN 897, prioridad. Resto de bits a 1 → p. ej. **0xF1**. Probar también 0xC1 (prioridad máxima) |
| Bytes 2–3 | SPN 898, régimen pedido, **0,125 rpm/bit, little-endian**. 1500 rpm = 12000 = 0x2EE0 → `E0 2E` |
| Byte 4 | SPN 518, par: 0xFF (no disponible) |
| Bytes 5–8 | 0xFF. Volvo: *"All unused bits must be set to 1"* |

Trama de ejemplo, 1500 rpm desde SA 0x11 [INFERIDA, no probada]:

```
ID 0x0C000011  DLC 8  F1 E0 2E FF FF FF FF FF
```

### 4.2 VP70 "VP Status" (alternativa propietaria de Volvo Penta)

- ID **0x0CFF4611** (PGN 65350), cada 20 ms.
- Contenido: posición de "pedal" de 0 a 100 % (bytes 3–4, 0x0000–0x03FF) y peticiones de arranque, parada, ralentí y precalentamiento.
- Sin VP70 válido el motor Penta va a ralentí. TSC1 tiene prioridad sobre VP70.
- **No se sabe si la E-ECU de la EC210B lo usa.**

### 4.3 Mensajes que emite la E-ECU (útiles para leer el estado)

| ID | PGN | Mensaje | Periodo | Dato útil |
|---|---|---|---|---|
| 0x0CF00400 | 61444 | EEC1 | 20 ms | **SPN 190 régimen** (bytes 4–5, 0,125 rpm/bit); par real (byte 3) |
| 0x0CF00300 | 61443 | EEC2 | 50 ms | % de carga (byte 3) |
| 0x18FEEE00 | 65262 | ET1 | 1 s | Temperatura de refrigerante (byte 1, °C − 40) |
| 0x18FEE500 | 65253 | HOURS | 10 s | Horas (0,05 h/bit) |
| 0x18FEF600 | 65270 | IC1 | 500 ms | Presión y temperatura de sobrealimentación |
| 0x18FECA00 | 65226 | DM1 | 1 s | Fallos activos (SPN/FMI) |
| 0x18FEE300 | 65251 | EC1 | a petición | Ralentí y ralentí alto configurados |

Estos son los periodos de Volvo Penta; en la EC210B **habrá que confirmarlos con el analizador**.

### 4.4 Códigos de fallo relevantes

| Código | MID / SID / FMI | Significado |
|---|---|---|
| ER13-09 | 128 / SID 231 / 9 | E-ECU: fallo de comunicación J1939 |
| — | 128 / PSID 201 / 9 | *"bus communication is missing with V-ECU on CAN/J1939"* |
| ER13 / ER14 | 187 / SID 231 · 250 | V-ECU: fallo en J1939 / J1587 |
| ER21 | 187 / SID 251 | Tensión de alimentación de la V-ECU |
| **ER31-03/04/05** | 187 / PPID 1190 | **Válvula power shift**: tensión alta, tensión baja, circuito abierto |
| ER32 | 187 / PPID 1191 | Válvula de control de caudal X1 |
| SW2701 | 187 / PPID 1133 | Dial de régimen fuera de rango |

---

## 5. Problemas típicos (foros) y cómo se resuelven

Detalle y fuentes en el [Anexo C](anexos/C_foros_averias_reparacion.md). Casi todo es BAJA/MEDIA (anecdótico).

| Problema | Síntoma | Solución reportada |
|---|---|---|
| Contactos internos de la V-ECU: en unidades antiguas la CPU va en zócalo | ER11, "no signal", fallos intermitentes, fallos hacia las 3000–6000 h | Abrir, limpiar la oxidación y reasentar el chip (arreglo temporal). Reparación de placa (~US$957 en EE. UU.; también talleres en Polonia y Rusia) o sustitución (~US$4000 programada) |
| Conectores detrás del asiento corroídos; mazo rozado por el movimiento del asiento | Fallos de comunicación intermitentes | Limpiar, proteger y reparar el mazo |
| Relés R3/R4 de la E-ECU, agua bajo la caja de relés | No arranca, "no signal to ECU" | Intercambiar o sustituir R3/R4 y secar la caja |
| Selector Auto/Manual con pines corroídos | Manual no funciona bien o "va a tope" | Limpiar o sustituir el interruptor |
| Baterías o alternador débiles | "Ghost codes", SID 250/231/251 | Revisar la carga (24 V con contacto, ~27 V en marcha) |
| Bus J1939 dañado | ER13, PSID 201 | Medir 60 Ω, continuidad y cortos a masa o a +24 V. Desconectar las ECUs una a una |
| **Uso prolongado en Manual** | Solo dos regímenes, sin auto-ralentí, más consumo. Un caso de EC210BLC D6D EAE2 **se cala con carga a 1900 rpm** | Comprobar que llegan los 340 mA a la válvula. Sin ESSPC la bomba puede ahogar el motor |
| V-ECU nueva o usada | Viene vacía o con el programa de otra máquina | Programarla con VCADS Pro según el número de serie. Algunos talleres clonan la flash/EEPROM a una unidad donante |

**Conectores:**
- V-ECU B: JA (70) y JB (16). Se venden conectores de recambio "14518349/14594697 connector plug".
- **No se encontraron números Deutsch/TE de carcasa ni de terminales.**
- Recomendación: no cortar el mazo original. Hacer un **adaptador** con conectores de recambio del mismo tipo, o enchufar el emulador en la posición de la V-ECU con un conector macho equivalente.

---

## 6. Propuesta técnica para el ESP32/Arduino (fases)

### Fase 0 — Mediciones obligatorias antes de diseñar

1. Resistencia de la bobina power shift: se esperan ~17,5 Ω.
2. **Corriente real en la válvula** en Manual con la emergencia en alta: se esperan ~340 mA. Si da 0 mA, hay una avería en la Resistor Box, F24 o el selector.
3. Resistencia de la Resistor Box: se esperan ~60 Ω.
4. Bus CAN, con todo apagado: resistencia CAN-H↔CAN-L. Identificar los pines B1/B2 en la E-ECU y JB14/JB6 en el mazo de la V-ECU. ✅ Terminación de la E-ECU: 117 Ω.
5. Tensión en el pin B4 de la E-ECU con el interruptor 26 en neutral y en alta.
6. Tensiones de alimentación: con contacto y con el motor en marcha.
7. Cableado del selector Auto/Manual: qué contactos conmutan entre la salida de la V-ECU y la Resistor Box.

### Fase 1 — Regulación de la potencia de la bomba (sin CAN, riesgo bajo)

- **Dónde conectarlo:** en lugar de la Resistor Box (modo Manual), o en la salida de la V-ECU hacia la válvula (modo Auto, vía el selector).
- **Opción A, la más robusta:** un **amplificador de válvula proporcional comercial** con entrada de 0–10 V o potenciómetro, rampas y dither.
  - Modelos: EWM-A-PV, Danfoss EHH-AMP-702, Hansa-Flex HK PAM 19.
  - Hay que comprobar que admiten un fondo de escala de ~600–700 mA.
  - El ESP32 o el potenciómetro solo generan la consigna.
- **Opción B, driver propio:**
  - Etapa de potencia: MOSFET en lado bajo de ≥60 V, **diodo de libre circulación** en la bobina y shunt con amplificador (INA180/INA240).
  - Control: **lazo PI de corriente** en el ESP32, con PWM de 1–5 kHz y dither de 100–250 Hz de ±30–50 mA.
  - CI dedicados posibles: Infineon TLE7241E / TLE82453 (comprobar el margen de 24 V).
- **Interfaz:** un encoder o potenciómetro selecciona los pasos 215 / 250 / 290 / 340 / 450 / 555 mA, o un valor continuo limitado a **≥290 mA si no hay ESSPC**.
- **Fail-safe obligatorio:**
  - 0 mA significa **la bomba al máximo**.
  - Un **relé NC devuelve la Resistor Box original** si el ESP32 falla, con watchdog.

### Fase 2 — Lectura del motor y ESSPC (CAN en solo escucha)

- **Hardware CAN:** ESP32 (TWAI) a 250 kbit/s con transceptor de 3,3 V (SN65HVD230, TJA1051T/3 o TCAN1051).
  - Con Arduino: MCP2515, declarando bien el cristal (`setBitrate(CAN_250KBPS, MCP_8MHZ)`).
- **Mensajes a leer:** EEC1 (rpm) y ET1 (temperatura), con `TWAI_MODE_LISTEN_ONLY`.
- **ESSPC sencillo:** si las rpm caen más de X por debajo de la consigna con carga, subir la corriente de la válvula.

### Fase 3 — Regulación del régimen del motor (TSC1)

- **Requisitos:** selector en **Auto** y la V-ECU original **desconectada**.
- **Funcionamiento:** el emulador envía TSC1 desde SA 0x11 cada 10 ms, con la consigna limitada por software a 800–2000 rpm.
- **Problema abierto:** en Auto, la válvula de la bomba recibe la corriente desde la salida de la V-ECU. El emulador también tendrá que generarla (Fase 1 en el pin de la V-ECU).
- **Probable efecto secundario:** si la E-ECU espera otros mensajes periódicos de la V-ECU, aparecerán PSID 201 / SID 231. Para evitarlo hay que capturar el tráfico de una EC210B sana.
- **Bibliotecas J1939:** Open-SAE-J1939 (MIT) o ARD1939. Opcionalmente, enviar el address claim (PGN 60928).

### Protecciones para 24 V (todas las fases)

- Load dump según ISO 16750-2: ~58 V suprimido, hasta 150–200 V sin suprimir.
- TVS, protección contra inversión de polaridad (LM74700/LM74930) y DC-DC de entrada ancha.
- Transceptor CAN tolerante a ±58 V o aislado.
- No añadir una tercera terminación de 120 Ω.
- Fusible propio, conectores sellados y caja IP67.

---

## 7. Plan de verificación del protocolo (antes de transmitir nada)

1. Conectar el ESP32 o un adaptador USB-CAN (con SavvyCAN, cangaroo o python-can) en **modo solo escucha** a 250 kbit/s. Confirmar que llega EEC1 (0x0CF00400).
2. Si es posible, **capturar una EC210B sana en modo Auto** y anotar los IDs con SA 0x11 (V-ECU), su periodo y cómo cambian al mover el dial. Es la única manera de saber con certeza qué espera la E-ECU.
3. Preguntar a la E-ECU su configuración: Request PGN 65251 (EC1) con ID 0x18EA0011 y datos `E3 FE 00`.
4. Con la máquina parada y los mandos bloqueados, en Auto y sin V-ECU, enviar TSC1 desde SA 0x11 con consignas cercanas al ralentí (900–1000 rpm). Comprobar en EEC1 que el motor obedece. Si no responde, probar SA 0x03 y la prioridad 0xC1.
5. Revisar DM1 y los códigos en pantalla: SID 231 y PSID 201.
6. Comportamiento si falla el emulador: al dejar de enviar TSC1, el motor debe volver a su régimen por defecto. Comprobarlo.

---

## 8. Lo que NO se ha podido confirmar (lagunas abiertas)

1. El pinout completo de la V-ECU (JA de 70 y JB de 16 pines), incluido **el pin de salida de la válvula power shift**.
2. La marca y referencia de los conectores de la V-ECU y de la E-ECU, y el número exacto de vías de la E-ECU.
3. **El mensaje exacto con que la V-ECU pide el régimen** (TSC1 u otro propietario), el resto de mensajes periódicos que espera la E-ECU y la velocidad del bus J1939 en la EC210B.
4. La ubicación de las resistencias de terminación del bus: la de la **E-ECU confirmada** (117 Ω); falta saber si el panel MDU lleva la otra.
5. El tipo de señal en el pin B4 (emergencia) de la E-ECU.
6. La resistencia real de la bobina y de la Resistor Box, y la frecuencia de PWM y dither que usa Volvo.
7. El significado de "VCE56003584" y la generación (EMS1 o EMS2) y fabricante del hardware de la E-ECU.
8. Si la E-ECU acepta TSC1 con el selector en Manual: probablemente no, porque prioriza la entrada cableada.
9. Colores de los cables y el esquema completo del manual de servicio (grupo 37). Solo está en el manual de servicio de pago o en Volvo PROSIS.

> **Recomendación:** conseguir el **manual de servicio completo de la EC210B** (esquemas eléctricos del grupo 37, con colores de cable y referencias de conectores). Es la fuente que cerraría la mayoría de estas lagunas. Se vende en webs de manuales; también se puede pedir a un concesionario Volvo CE una impresión de los esquemas desde PROSIS.

---

## 9. Advertencias de seguridad

- Hacer todas las pruebas con la máquina **estacionada**, la **palanca de seguridad hidráulica bloqueada** y el equipo apoyado en el suelo.
- La corriente de la válvula a 0 mA da la **máxima absorción de la bomba**. Una corriente demasiado baja sin ESSPC puede **calar el motor bajo carga**.
- Limitar por software el régimen a 800–2000 rpm y la corriente a 0–700 mA.
- Mantener siempre la posibilidad de volver al **modo Manual de fábrica** (Resistor Box + interruptor 26) con un solo interruptor.
- Antes de soldar en la máquina, desconectar la V-ECU, la E-ECU y la I-ECU (indicación del manual de servicio).
