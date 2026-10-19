# Investigación: familia de máquinas Volvo CE con la E-ECU 03161983 / 60100002 / 20577135 (D6D/D7D)

Fecha: 2026-10-19. Objetivo: aprovechar la documentación de L90E/L110E/L120E, EC160B–EC290B, EW145B–EW180B y G710B para cubrir lagunas del EC210B (ser. ~10828, oct-2002) en el proyecto de controlador ESP32 sustituto de la V-ECU.

Convención de fiabilidad: **ALTA** = documento Volvo (manual, esquema, boletín, material de formación Volvo CE), **MEDIA** = sitio técnico/reparador reputado o documento de otro OEM (Deutz, JLG) aplicable, **BAJA** = foro / vendedor / dudoso. Cada afirmación se marca además como *Confirmado*, *Inferido* o *No encontrado*.

Nota: se agotó el presupuesto de búsquedas web (200 por turno) hacia el final; los puntos marcados "No encontrado" quedaron sin resolver con las búsquedas realizadas (inglés, español, portugués, ruso, polaco). Varios sitios (pdfcoffee, manualmachine, slideshare, servicepartmanuals) bloquearon la descarga directa; Scribd sólo entregó texto (a veces ofuscado por fuentes incrustadas, descifrado manualmente — ver notas).

---

## 0. Hallazgos clave (resumen)

1. **La E-ECU 03161983 / 60100002 / 20577135 es un controlador Deutz EMR2 (Electronic Motor Regulation 2)** fabricado por Lucas/TRW (hoy marcado también como Delphi por reparadores). *Inferido con alta probabilidad*: el boletín Volvo de reprogramación habla de "Dataset **EMR** control unit, programming" y de "EMR2" en el servidor TSC (ALTA); un vendedor lo describe como "TRW ECU Controller 60100000" (BAJA); la etiqueta real de una unidad de L90E lleva "D6D LAE2 … 03161983 P03" (BAJA, foro). El motor D6D es el Deutz TCD2012/BF6M1013 con bomba-inyector, cuyo ECU estándar es el EMR2 (dos conectores de 36 vías: lado motor y lado vehículo).
2. **Pinout real del conector lado vehículo ("EB") de la E-ECU** obtenido del esquema Volvo L120E (D7D, misma E-ECU según vendedores) **Sch31/Sch28/Sch24** (ALTA): **EB1 = CAN (J1939) hilo amarillo, EB2 = CAN hilo verde** (par trenzado con terminador de 120 Ω R702 en la I-ECU); **EB25/EB26 = J1708/J1587 (gris/naranja)**; **EB11 y EB12 = +24 V (15E18, fusible 20 A tras relé dependiente de la I-ECU)**; **EB9 y EB10 = masa**; EB31 = mando del relé de precalentamiento RE2501; EB5 = retorno/sensado de la bujía de aire HE2501; EB24 = línea hacia la toma de servicio (IB4); EB7/EB8 = nivel de refrigerante SE2603; EB13/EB3/EB17 = sensor combinado presión/temperatura de admisión SE2501/SE2502. El documento de formación Volvo CE Korea del EC210B confirma, de forma independiente, **B1 (H), B2 (L)** para J1939 y **B25 (A), B26 (B)** para J1587 en la E-ECU (ALTA, texto descifrado).
3. **El pedal acelerador de las cargadoras NO va a la E-ECU ni a la V-ECU: va a la I-ECU** (L120E Sch27: APS SE214 → I-ECU P3.10/P3.9/P3.3, IVS → P2.13/P3.15; acelerador manual R205 → I-ECU). La consigna de régimen llega a la E-ECU **sólo por J1939**. En la pala, igual: la V-ECU "Request Unload RPM" a la Engine ECU por CAN (ALTA). **No hay evidencia de entrada analógica de acelerador usada por Volvo en esta E-ECU.** El EMR2 genérico sí dispone de entrada de pedal (pines 20/23/25 del conector vehículo según la descripción de sistema Deutz — MEDIA), pero su activación depende del dataset/configuración.
4. **Direcciones J1939 en el EC210B (ALTA, Volvo CE Korea "Electronic Control System" EC210B-04-01)**: E-ECU (EMS) **MID 128 = SA 0**; **V-ECU MID 187 = SA 17 (0x11)**; **MDU (D-ECU, pantalla de las máquinas anteriores a la I-ECU) MID 140 = SA 23 (0x17)**; herramienta VCADS Pro/MATRIS MID 172 (SDU). Buses: J1939 CAN a 250 kb/s y J1708/J1587 a 9,6 kb/s (ALTA, L90F).
5. **Circuito de emergencia del EC210B (ALTA)**: conmutador Auto/Manual + "Emergency engine speed control switch" (0 = paro tras 3 s; 1 = ralentí 800 rpm; 2 = alto 1900 rpm — H, G1 en Norteamérica) + **Resistor Box de 60 Ω nominales (a 25 °C)** en serie con la válvula power-shift → **340 mA** en modo manual (vs 215–555 mA en modo normal gestionado por la V-ECU). Fusible **F24 5 A "Engine RPM manual control"**; F15 20 A E-ECU; F13 10 A y F25 60 A V-ECU. En modo manual la V-ECU queda fuera ("Manual (Off VECU)") y la E-ECU recibe la consigna por **entradas discretas del conmutador de emergencia**; el pin exacto de la E-ECU **no se encontró** (aparece como "SW2704" en SCH02-1).
6. **Programación**: el dataset de la E-ECU se descarga del servidor Volvo (TSC/EMR2) **por número de serie del MOTOR** y se carga con VCADS Pro "Dataset EMR control unit, programming" (ALTA, boletín). En máquinas antiguas sin la línea de comunicación en el mazo **no se puede programar en la máquina**: hay que pedir una E-ECU "fully pre-programmed" indicando serie de máquina y de motor (ALTA). Parámetros de cliente se transfieren con la operación 17030-3; la operación de programación MID 128 es 28423-3 (ALTA, L150G; el índice del manual EC210B tiene los mismos títulos). **No se encontró ningún anti-robo/emparejamiento E-ECU↔V-ECU** en la serie B/E (*No encontrado*, ni en documentación ni en foros).
7. **Corte de serie EC210B 14132**: a partir de 14132 el EC210B incorpora la **I-ECU** (esquema SCH02-1 "I-ECU equipped": "EC210B 14132 – changed because of I-ECU applications") (ALTA). Las máquinas anteriores (como la 10828) llevan la **MDU / D-ECU** (MID 140, SA 23) y la arquitectura descrita en el material de formación "EC210/160B" de Volvo CE Korea (ALTA).

---

## 1. Pinout de la E-ECU (conectores EA = lado motor, EB = lado vehículo)

### 1.1 Fuente principal: esquemas Volvo L120E (Sch02, Sch03, Sch24, Sch27, Sch28, Sch29, Sch30, Sch31) — **ALTA**

Documento Volvo CE Customer Support AB, "3 Electrical System" (menú L120E), PDF de 38 páginas descargado de `https://s6dc2dc82dd3d959c.jimcontent.com/download/version/1549606161/module/8252731715/name/L120E_MENY.pdf` (copia local: `/home/user/docs/manuales/volvo_ce/Volvo_L120E_Service_Training_Electrical_Schematics_Sch01-Sch100.pdf`). Los nombres EA/EB son los conectores **propios de la E-ECU** (en el mismo manual la V-ECU también usa EA/EB/EC para sus propios conectores — no confundir).

**Conector EB (lado vehículo) de la E-ECU — Sch31 (L69111A) y Sch28 (L69103A):**

| Pin E-ECU | Color hilo | Función (según esquema) | Hacia |
|---|---|---|---|
| EB1 | Y (amarillo) | **J1939 CAN** (par trenzado con EB2) | Sch24 línea 12 → I-ECU P1.1 (R702 120 Ω entre P1.1 y P1.15), V-ECU EC16, toma de servicio |
| EB2 | GN (verde) | **J1939 CAN** (par con EB1) | Sch24 línea 13 → I-ECU P1.15, V-ECU EC17 |
| EB25 | GR (gris) | **J1708/J1587** (par trenzado con EB26) | Sch24 línea 14 → Y/R → V-ECU EB38, I-ECU P1.7, toma de servicio IA8 |
| EB26 | OR (naranja) | **J1708/J1587** (par con EB25) | Sch24 línea 15 → Y/SB → V-ECU EB11, I-ECU P1.21, toma IA9 |
| EB11 | R/W (15E18) | **+24 V alimentación** | FU18 20 A ← RE11 (relé "dependiente de la I-ECU", mando I-ECU P3.21) ← 30K |
| EB12 | R/W (15E18) | **+24 V alimentación** (puenteado con EB11) | ídem |
| EB9 | SB/W | **Masa** | Sch01 pto. 8 |
| EB10 | SB/W | **Masa** (puenteado con EB9) | ídem |
| EB31 | BL/R | Salida mando relé precalentamiento RE2501 (bobina alimentada por 15EA-14) | RE2501 → HE2501 (calentador de aire, FU72 150 A) |
| EB5 | GN | Sensado/retorno del calentador HE2501 | HE2501 |
| EB24 | Y/SB → BL/Y 2135 | Línea hacia la **toma de servicio IB pin 4** (Sch24 línea 11). *Inferido*: línea de diagnóstico ISO 9141/K-line típica del EMR2 (SERDIA). No confirmado. | Toma IB4 |
| EB7 | BL/SB | Entrada nivel de refrigerante SE2603 (contacto) | SE2603 pin 1 |
| EB8 | GR/W | Alimentación/referencia de sensores (común con SE2501/2502 pin 2) | SE2603 pin 2, SE2502 pin 2 |
| EB13 | VO/W | Sensor temperatura aire de admisión SE2501 (pin 4) | SE2501 |
| EB3 | BL/Y | Sensor SE2501/2502 (pin 3) | SE2501 |
| EB17 | GR/W 2147 | Sensor presión de admisión SE2502 (pin 1) | SE2502 |

**Observación sobre la asignación A/B del J1587**: el documento EC210B-04 (ver 1.2) da **B25 = A y B26 = B** (descifrado; véase la nota de descifrado). En el L120E, EB25 (GR) termina en el hilo Y/R y EB26 (OR) en Y/SB.

**Conector EA (lado motor) de la E-ECU — Sch28, Sch29, Sch30 (L69103A/L69107A/L69108A):**

| Pin | Función |
|---|---|
| EA30 / EA31 | Sensor de régimen (cigüeñal) SE2701 (par apantallado, pantalla a EA5 vía ED7) |
| EA18 / EA7 | Sensor de régimen (árbol de levas) SE2703 (pantalla a EA5 vía ED15) |
| EA5 | Masa de sensores (BN/W), común a SE2606, SE2507, SE2508, SE2203, SE2306 |
| EA25 | Sensor temperatura SE2606 (Y/W) |
| EA2 | Sensor temperatura SE2507 (GN 2146) |
| EA3 | Sensor presión SE2508 (BN) |
| EA4 | Alimentación 5 V sensores de presión (GN/W) a SE2508 y SE2203 |
| EA14 | Sensor presión SE2203 (GR) |
| EA13 | Sensor temperatura SE2306 (GN) |
| EA11, EA22, EA23 | Bombas-inyector MA2301/2302/2303 (lado alto), retorno común EA12 |
| EA34, EA35, EA36 | Bombas-inyector MA2304/2305/2306, retorno común EA24 |

No aparece en estos esquemas ninguna entrada discreta "arranque/llave 15" distinta de la alimentación conmutada EB11/EB12: la E-ECU se enciende con el relé RE11 que gobierna la I-ECU (apagado retardado para guardar datos). *Inferido*: en el EC210B el papel de RE11 lo hacen los relés R3 "Power supply EMS" (RE3701) y R4 "EMS Data Record" (RE3702) de la caja de relés, gobernados por la V-ECU/MDU (ver sección 6).

Esquemas extraídos como PNG: ver sección "Esquemas extraídos".

### 1.2 Fuente de contraste: formación Volvo CE Korea "EC210B Electronic Control System" (EC210B-04) — **ALTA**

`https://www.scribd.com/document/461665933/EC210B-04` (24 págs.). El texto de Scribd está ofuscado por una fuente incrustada; lo descifré por sustitución (p. ej. "Tfnvf Afgstruatjfg Iqujpligt Cfrib Ntk." = "Volvo Construction Equipment Korea Ltd."). Página 3 "Control Circuit" lista, junto a los pines JA/JB de la V-ECU, el bus: `… J1587 J1939 B26(B) B25(A) B2(L) B1(H) 21C12(H) 21C4(L) 21C1(H) 21C7(L) … 23C8(A) 23C9(B) JB13(H) JB14(L) JB5(A) JB12(B) …`. Lectura: **E-ECU conector B: B1 = CAN-H, B2 = CAN-L, B25 = J1587 A, B26 = J1587 B; V-ECU: JB13 = CAN-H, JB14 = CAN-L, JB5 = J1587 A, JB12 = J1587 B** (los dígitos 5/6 son los únicos con ambigüedad residual en el descifrado; "JA60" y "JA35" de la misma página confirman la resolución elegida). Coincide con el L120E (EB1/EB2 CAN, EB25/EB26 J1708). Confirmado (dos fuentes Volvo independientes).

### 1.3 Pedal acelerador / entrada analógica de acelerador

- **L120E Sch27 (ALTA)**: pedal SE214 (APS potenciómetro + IVS interruptor de ralentí) → **I-ECU** (P3.10, P3.9, P3.3; P2.13, P3.15). Acelerador manual R205 → I-ECU (P3.22, P3.14, P1.29). El L90F usa el mismo esquema Sch27 "Accelerator Pedal and electrical hand throttle" (L67865B) (ALTA, `https://www.scribd.com/document/361072244/3-Electrical-System-Volvo`).
- **Conclusión**: en las cargadoras E la consigna de régimen va I-ECU → J1939 → E-ECU. No hay entrada analógica de acelerador cableada a la E-ECU en Volvo CE. *Confirmado para L120E/L90F; inferido para L90E/L110E.*
- **Deutz EMR2 genérico (MEDIA, "EMR 2 System Description" Deutz, vía fragmentos de búsqueda de `https://pdfcoffee.com/deutz-emr2-electronic-engine-governor-pdf-free.html`, no descargable)**: la electrónica EMR2 admite un sensor de pedal (SWG) de 1 kΩ con alimentación por **pin 25** (máx. 30 mA), señal en **pin 20** y masa en **pin 23** del conector vehículo (otra configuración usa pin 24), y entradas digitales configurables ("Drehzahl 1/2", memoria de régimen, etc.). Si Volvo dejó activa esa entrada depende del dataset; **no probado**.

### 1.4 Diferencia D6D (EC210B) vs D7D (L120E)

Vendedores listan el mismo 03161983/60100002/20577135 para L90E (D6D) y L120E/EW145B (D7D) (BAJA). El EMR2 es común a Deutz 1012/1013/2012/2013. El pinout hardware es el mismo; cambia el dataset. *Inferido.*

---

## 2. Cómo la V-ECU manda el régimen a la E-ECU; buses y direcciones

### 2.1 Arquitectura y direcciones (ALTA — EC210B-04-01 descifrado)

`EMS(E-ECU) MID128 SA0 — MDU(D-ECU) MID140 SA23 — VECU MID187 SA17 — J1939(CAN) — J1587(J1708) — VCADS Pro/MATRIS MID172 SDU (Service Contronic)`

- **E-ECU: MID 128, SA 0.**
- **V-ECU: MID 187, SA 17 (0x11).** Confirma la hipótesis del equipo.
- **MDU/D-ECU (pantalla, máquinas pre-14132): MID 140, SA 23 (0x17).** La I-ECU posterior conserva MID 140 (fallo "140 SID 231-9" citado en foros para EC210BLC — BAJA).
- Formación VCADS Pro Volvo CE (ALTA, `https://www.scribd.com/document/986461101/1-VCADS-Pro-in-VolvoCE`): "Engine-ECU MID 128, Transmission-ECU MID 130, Vehicle-ECU MID 187, Instrument-ECU MID 140, Cab-ECU MID 178, Wireless-ECU MID 142".
- L90F "Electrical System" (ALTA): "Signal transfer CAN2/J1939 and J1708/J1587", J1939 **250 kb/s**, J1708 **9,6 kb/s**; niveles J1708 A ≈ 5 V/B ≈ 0 V ("0"), 3,5/1,5 V ("1").
- Fallos de bus en el EC210B (ALTA, tabla SAE→código Volvo, `https://www.scribd.com/document/351473971/Code-Error-Exca-Volvo`): 128 SID231 FMI9 = ER13-09 "J1939 communication failure"; 128 SID250 FMI12 = ER14-12 J1587; 187 SID231 FMI9 = ER13-09; 187 SID240 FMI2 = ER11-02 V-ECU; 187 PPID1190 FMI3/4/5 = ER31-03/04/05 válvula proporcional power-shift; 187 PPID1134 = SW9101 (flow control switch); SW2701-03/04 = selector de régimen tensión alta/baja; "Troubleshooting: check the control module JA30–JA56, signal lines".

### 2.2 Consigna de régimen (ALTA en la lógica; *No encontrado* el PGN exacto)

EC210B-04-04 "Engine Speed and Work Mode Control" (descifrado): 
- (1) Modos **F, I**: `Engine Speed Control SW → V-ECU → "Request Unload RPM" → Engine ECU`; a la válvula power-shift "Fixed Current, Any RPM". 
- (2) Modos **P, H, G**: V-ECU manda "Request Unload RPM" y corriente fija; (3) con carga: "Increased Current, Loaded RPM". 
- EC210B-04-12 "Operating Data Memory": la V-ECU recibe datos de la Engine ECU y guarda registros; -14/-15: la Display ECU muestra estado y códigos recibidos de V-ECU y E-ECU.
- Es decir, **la V-ECU envía por J1939 una petición de régimen (valor de rpm objetivo) y la E-ECU la ejecuta**; la V-ECU gestiona la corriente de power-shift según modo y "caída" de régimen bajo carga. El **PGN/formato de la petición no está documentado públicamente**. *Inferido*: TSC1 (PGN 0) con "override control mode = speed control" dirigido a SA 0 desde SA 17, o un PGN propietario Volvo; sólo se puede fijar capturando el bus de una máquina sana. El manual EC210B contiene la sección "SAE J1939_CAN control link, description and measuring" (título confirmado en índice, contenido no accesible).

### 2.3 Apagado retardado / alimentación de ECUs (ALTA + BAJA)

- L120E Sch02: el relé **RE11** (mandado por la I-ECU P3.21) alimenta E-ECU (15E18 vía FU18 20 A) y V-ECU (FU17 10 A → EB28); el 15EA-15 directo alimenta I-ECU (P1.14) y V-ECU (EB14) para despertar.
- Foro HEF L90E (BAJA, técnico experimentado): "al girar la llave a 1 se alimenta la I-ECU; la I-ECU alimenta un segundo relé que alimenta E-ECU y V-ECU (apagado retardado para que el software se cierre correctamente); si falta el software, investigar el circuito de apagado retardado".
- EC210B (ALTA, lista de relés de la caja sobre la batería): **R3 "Power supply EMS" (RE3701, NA)** y **R4 "EMS Data Record" (RE3702, NA)**; foro HEF EC210B 2014: fallo "187 231 9" y paradas intermitentes resueltos cambiando los relés 3 y 4 (BAJA).

---

## 3. Parámetros VCADS Pro de la E-ECU y procedimiento "MID 128 replacing"

### 3.1 Títulos del manual de taller EC210B (ALTA — índice en `https://aplusmanual.com/433/volvo-ec210-series-excavators-service-repair-manual`, también `https://servicepartmanuals.com/partmanual/volvo-ec210b-lc-service-repair/`)

"Engine control unit E-ECU, specifications / function description"; "**E-ECU MID 128 non-programmed, replacing**"; "**E-ECU MID 128 pre-programmed, replacing**"; "V-ECU MID 187 non-programmed / pre-programmed, replacing"; "I-ECU MID 140 …"; "VCADS Pro, 17030-3 – Parameter, programming"; "SAE J1939_CAN control link, description and measuring"; "SAE J1708_1587 information link, description and measuring"; "Emergency engine speed control switch, description / specifications"; "Emergency operation, description"; "MID 128 SID 230, description and measuring"; "Component troubleshooting, checking wiring harness and input_output on ECU"; "Connectors, overview"; "Wiring diagram SCH01 … SCH27" (dos versiones de varias hojas: con/sin I-ECU); "Proportional solenoid valve (power shift), replacing".

### 3.2 Procedimiento MID 128 (ALTA, mismo esquema en toda Volvo CE; texto literal de L150G, `https://www.slideshare.net/slideshow/volvo-l150g-wheel-loader-service-repair-manual-instant-downloadpdf/264289188`)

- **Non-programmed ECU**: "Connect VCADS Pro and start operation **28423-3 MID 128 ECU, programming**" → desconectar batería → sustituir E-ECU → reconectar → "Finish the VCADS Pro operation 28423-3". 28423-3 = "When changing [ECU] or only reprogramming".
- **Pre-programmed ECU**: "The new control unit has basically adjusted parameters for the machine. Read out **customer parameters** from the old control unit with operation **17030-3 Parameter, programming**, save on job card … compare and change customer parameters according to the old unit".
- Parámetros de cliente típicos de la E-ECU (listados para D13 en L150G; para EMR2 el conjunto es menor): "(YA) Idle speed, setting", "(FAU/FAV) Automatic engine shut off / time", calibración de inyectores por cilindro.
- Manual VCADS Pro (ALTA, `https://www.scribd.com/document/878387579/engGB`): cuando se sustituye una unidad por otra con **nuevo número de hardware**, hay que **actualizar el número de parte en VDA antes de programar**; "MID 128 campaign programming" sólo tras aviso de Volvo y con conexión central. Dos tipos de parámetros: *customer* (modificables localmente) y *vehicle* (fijados en fábrica, requieren conexión a VDA).
- **"MSW / DST1 / DST2"**: *No encontrado* en ninguna fuente accesible. *Inferido* (terminología Volvo habitual en VCADS/Tech Tool): MSW = Main SoftWare, DST1/DST2 = DataSeT 1 / 2 (el manual de formación VCADS habla de "software and data set levels for each ECU"; el técnico del foro L90E: "si ves software y dataset levels no es problema de software; si sólo ves hardware number y fecha, el software está corrupto"). No confirmado documentalmente.

### 3.3 Boletín de servicio Volvo "E-ECU, Control unit engine — Unable to program E-ECU through VCADS Pro" (ALTA; `https://www.scribd.com/document/581311237/128sid231`, texto ofuscado descifrado)

Contenido literal (descifrado): 
- "Cause: Unable to program E-ECU through VCADS Pro. Action: Developed new E-ECU software which can be programmed through VCADS Pro. **Added one communication line in wire harness of crawler machines**. NOTE: in wheeled machine, additional communication line has been existing from the beginning."
- "The part number of E-ECU has not been changed because this is a matter of software and electric circuit in the machine. **For the crawler machines produced before the above serial numbers, fully pre-programmed E-ECU should be ordered because the communication line doesn't exist in the machine and then it cannot be programmed. When ordering fully pre-programmed E-ECU, machine serial number and engine serial number should be provided together.** For machines after the improvement, E-ECU equipped only with base software (we used to call it 'empty' E-ECU but it has base software to run dataset software) can be ordered and programmed through VCADS Pro."
- Procedimiento: VCADS Pro → [Engine, engine mounting and equipment] → [**Dataset EMR control unit, programming**] → login en **TSC mainsite** (`wsg.volvo.se/tsc`) → elegir **[EMR2]** → **introducir número de serie del motor** → descargar → elegir el fichero **.hex**. "Loss of power during uploading can result in E-ECU damage."
- Modelos/series: el descifrado de dígitos es ambiguo (fuentes subset no biyectivas). Los modelos parecen ser **EC140B LC, EC140B LCM, EW140B** (D4D, también EMR2) con fecha 2003; no está claro que mencione EC210B. **Relevancia para el EC210B de 2002**: *inferido* que, por la misma razón (sin línea de programación en el mazo / software antiguo), **una E-ECU para una máquina temprana se pide "pre-programada" por serie de máquina + motor y no se programa in situ**. Para confirmarlo hace falta el boletín equivalente del EC210B o un concesionario.
- Implicación de diseño: la programación/dataset está **vinculada al motor**, no a la V-ECU: no hay indicio de emparejamiento E-ECU↔V-ECU.

### 3.4 Perspectiva Deutz (MEDIA)

- JLG (catálogo Deutz): "The programmed EMR2 control module is **engine serial number specific due to EPA regulations and can only be programmed by the engine manufacturer**" (`https://onlineexpress.jlg.com/parts/engine-parts/deutz/electrical/switches-and-controls-and-relays-and-accessories/p/04218027`).
- Tabla de fallos EMR2 Deutz: "if not programmed, **EEPROM is defect → reprogram ECU and if necessary replace it**" (`https://www.scribd.com/document/604568599/Chapter-5-Deutz-EMR-2-Fault-Codes-new`).
- Herramienta Deutz: SERDIA 2010 + interfaz DeCOM/CANUSB permite leer/escribir configuración EMR2/3/4 (vendedores, BAJA: `https://www.fridayparts.com/diagnostic-kit-for-deutz-controller-emr2-emr3-emr4`). Si la E-ECU Volvo acepta SERDIA no está confirmado.

---

## 4. Informes de foros y reparadores sobre esta E-ECU

| Fuente | Fiab. | Contenido relevante |
|---|---|---|
| HEF "Volvo L90E E-ECU problem" (2019) `https://www.heavyequipmentforums.com/threads/volvo-l90e-e-ecu-problem.75453/` | BAJA (técnico Volvo experimentado responde) | Sin comunicación V-ECU↔E-ECU; VCADS sí ve las tres ECUs por J1708 (toma IB). Consejos: relé "I-ECU dependent" que alimenta E-ECU y V-ECU; **terminador 120 Ω detrás del panel** (60 Ω medidos con todo conectado); en el conector de la E-ECU "**dos pares trenzados: naranja-amarillo y gris-verde** en la esquina"; I-ECU con hardware acabado en "402" tenía soldaduras frías; si la identificación muestra sólo hardware/fecha y no software/dataset → software corrupto (un taller "ha tenido E-ECUs que sólo necesitaban recarga de software"). **Etiqueta de la E-ECU: frontal "E00780147, VCE54001231, D6D LAE2, 05.12.02"; trasera "03161983 P03, 80907C, 03161983, 00529932, 4602".** |
| HEF "Volvo L120E D7D engine not starting" (2023) `https://www.heavyequipmentforums.com/threads/volvo-l120e-d7d-engine-not-starting.98783/` | BAJA | Arranque con pinzas quemó la etapa de inyectores; reparada en taller electrónico, sigue sin arrancar: MID128 SID1…SID6 FMI11 (6 inyectores) y "injector unit unidentifiable"; **montada en otra L120E igual tampoco arrancó**; en banco con 24 V + CAN H/L responde a Tech Tool. Respuestas: posible pérdida de códigos de inyector; "si reprogramas con el fichero de fábrica usará los códigos de inyector originales". Lección: la reparación hardware no garantiza el dataset; una unidad "reparada" puede quedar sin calibraciones. |
| HEF "Volvo ec210b" (2014) `https://www.heavyequipmentforums.com/threads/volvo-ec210b.46725/` | BAJA | Códigos 187-231-9, paradas al trasladarse: **relés 3 y 4 de la caja sobre la batería (alimentan la E-ECU)**; confirmado por el autor. |
| HEF "Volvo L90E i-ecu problem" (2025) `https://www.heavyequipmentforums.com/threads/volvo-l90e-i-ecu-problem.118086/` | BAJA | Sin I-ECU el motor gira pero no arranca (la E-ECU no recibe la señal); era un fusible de 5 A. Confirma la dependencia E-ECU ← I-ECU/V-ECU para arrancar en cargadoras. |
| Unitech Electronics (reparador, Canadá) `https://www.unitechelectronics.ca/volvo-ecm-20577135-p02-repair-tested-and-rebuilt/` | MEDIA | 20577135 "P02" atribuido a **Delphi Electronics & Safety**; fallos típicos: pérdida de comunicación, paradas aleatorias, acelerador sin respuesta/ralentí irregular, códigos de inyectores/cigüeñal/CAN, **fallo del regulador interno de tensión**, daño ambiental. Reparan hardware "sin alterar ni borrar el software; la calibración original permanece". |
| ECM Repair USA `https://ecmrepairusa.com/product/60100002-20577135-ecm-volvo-excavators-and-graders-repair-service/` | MEDIA | Reparación 518 USD, fallos: fusibles fundidos, sin comunicación, paradas, intrusión de aceite/agua, **drivers de inyector**; devuelven la misma unidad "con la programación original intacta, sin recodificar". |
| SINOCMP (vendedor) `https://www.sinocmppartsstore.com/products/Trw-Ecu-Controller-60100000-...` | BAJA | Describe el 60100000 como "**TRW** ECU Controller"; para 60100002/20577135 "debido al programa especial y complejo no hay aftermarket, sólo original o usado"; "confirmar modelo de máquina y motor para la programación". |
| Amazon/eBay (varios) | BAJA | Unidades "programmed" vendidas pidiendo **placa de características y número de serie**; alguna promete "no programming, direct replacement" (contradictorio). |
| Karman Auto "Volvo ECU clone service" `https://karmanauto.com/volvo-ecu-clone-service/` | BAJA (comercial) | Clonado chip-level flash+EEPROM a donante del mismo hardware; sin método técnico; orientado a automoción. |
| auto-elektric.ru / trucksservice.narod.ru (reparadores RU) | BAJA | Servicio EMR2 (bloques 0419 4979 BF4M/BF6M): trabajo con Flash/EEPROM, restauración de bootloader y grabación de configuración "con vinculación al VIN de la máquina". |
| Repturn (FR) `https://www.repturn.com/en/product/ecu-calculator-emr1-emr2-deutz/` | BAJA | Repara EMR1/EMR2 Deutz (presupuesto individual). |

**Síntesis (inferida)**: (a) la unidad es reparable a nivel hardware (etapas de inyector, regulador) por talleres especializados sin perder el dataset; (b) **no hay informes de que una unidad usada de otra máquina (L90E→EC210B o viceversa) funcione sin reprogramar**, y los vendedores programan por serie de máquina/motor; (c) **no se encontró ninguna evidencia de anti-robo/pairing** entre E-ECU y V-ECU en la serie B/E; las dependencias que sí existen son eléctricas (relés de alimentación mandados por I-ECU/V-ECU) y funcionales (consigna de rpm por J1939: sin V-ECU la E-ECU cae a modo emergencia/ralentí); (d) no se localizaron hilos de mhhauto/digital-kaos/exkavator.ru/elektroda específicos sobre clonado de 60100002 (búsquedas en EN/RU/PL sin resultados; el tema EMR2 clone sí existe en el mundo Deutz pero sin método público).

---

## 5. Números de pieza de conectores

- **E-ECU (36 vías ×2)**: *No encontrado* ningún número VOE ni Deutz para carcasas/terminales. La búsqueda de "VOE 11418147" no devolvió ningún resultado (sólo el adaptador VOE11417096, distinto). Los únicos "plugs" ofrecidos son los del controlador 60100000 (SINOCMP `https://sinocmp.com/products/volvo-controller-connector-plug-for-ec210-ec240-ec210b-ecu-60100000`, BAJA, sin referencia de fabricante). *Inferido*: al ser un EMR2, los conectores son los estándar Deutz EMR2 (conector "lado motor" y "lado vehículo" de 36 vías); el número Deutz del contra-conector y de los terminales debería localizarse en el catálogo Deutz del TCD2012 (grupo eléctrico) o en el catálogo Volvo CE del D6D (grupo 37). Pendiente.
- **V-ECU JA(70)/JB(16)**: *No encontrado* número VOE de carcasa. Los listados eBay "Vecu Controller Connector Plug 14518349 14594697" (`https://www.ebay.com/itm/384979664114`) usan los números de la **propia V-ECU** (14518349 P01/P02/P03, 14594697), no del conector (BAJA).
- **Lista de conectores del EC210B** (ALTA parcial, traducción automática de un manual en español, `https://www.scribd.com/document/364107615/Connector-Ec210b`): MA23 y MA24 "connected to V-ECU"; **ME01, ME02, ME03 "connected to engine wiring harness"**; MC02 "connected to harness the EMS 1 driver"; EM01–EM04 "connected to harness electronic box"; MA27/MA26/MA28 relés de seguridad; MA09/MA07 relés de batería; MA63/MA62/MA65 relés de precalentamiento; MAE01–06 masas de bastidor. Útil para nombrar conectores, sin números de pieza.

---

## 6. Circuito de emergencia y Resistor Box / válvula power-shift (EC210B/EC160B)

### 6.1 Manual del operador EC210B ser. 14132- (ALTA; `https://www.tractorparts.com/PDFs/VOLVO_EC210B_OPERATIONS_MANUAL.PDF`, pág. 70-72 impresas)

- "25 **Automatic/manual selector switch** — Position 1 Manual controlled, Position 2 Auto controlled. If the V-ECU malfunction, this switch must be switched to Manual position. After changing damaged part, set this switch to automatic position. To turn manual mode to auto mode … the machine must be restarted."
- "26 **Emergency engine speed control switch** — If the engine speed control switch does not work, set 'Auto/Manual select switch' to Manual and use this emergency switch. **Position 0: Engine stop** (when the engine is not OFF even though the start switch is OFF; if held >3 s the engine shuts down). **Position 1: Idle speed** (I2 mode, no load). **Position 2: High speed** (H mode no load; exception: G1 for North America)."
- Fusibles (pág. 183): **F24 5 A "Engine RPM manual control"**, F15 20 A E-ECU, F13 10 A V-ECU, F25 60 A V-ECU, F1 10 A ECU instrumentos, F12 15 A safety solenoid, F16 15 A starter switch.
- Presentación (pág. 9): "Engine condition can be checked via the V-ECU by the data connection between EMS (Engine Management System) and V-ECU".

### 6.2 Manual de taller EC210B LC, "Current/pressure, specifications" (ALTA; páginas de muestra `https://www.aservicemanualpdf.com/Samplepages/SM-Volvo%20EC210B%20LC%20Excavator%20Service%20Repair%20Manual.pdf`, p. 19-20)

| Posición | Modo | rpm sin carga / con carga | Corriente válvula power-shift (±20 mA) | Presión secundaria | Conflux cut-off |
|---|---|---|---|---|---|
| 9 | P | 2000 / >1900 | 215 / variable | 3,8 kgf/cm² | OFF |
| – | H | 1900 / >1800 | 250 / variable | 5,8 | OFF |
| 8 | G1 | 1800 / >1700 | 290 / variable | 8,1 | OFF |
| 5 | F1 | 1500 | 450 | 19,8 | ON |
| 2 | I1 | 1000 | 555 | 28,5 | OFF |
| 1 | I2 | 800 | | | |
| **Emergency High** | | **1900** | **340** | | |
| **Emergency Low** | | **800** | | | |

### 6.3 Formación Volvo CE Korea (ALTA; EC210B-04-07/-20/-21 y EC210/160B-ENG7-04, textos descifrados)

- ENG7-04 "Emergency Control": normal → V-ECU → Power Shift Valve (**210B: 555 mA; 160B: 580 mA**, ralentí) y Engine ECU. Con Auto/Manual en **Manual ("Off VECU")**: Emergency Switch posición **Neutral/Up → 800/1900 rpm** → Engine ECU; **Power Shift Valve 340 mA** vía **Resistor Box**; posición **Down 2 s → Off Engine** ("engine does not stop with key").
- EC210B-04-21 "**Resistor Box — Rated resistance (at 25 °C): 60**" (unidad cortada en la extracción; *inferido* 60 Ω: 24 V / (60 Ω + bobina ≈10 Ω) ≈ 340 mA, coherente con la tabla).
- EC210B-04-20 "Emergency Switch / Auto Manual Switch" con esquema de contactos (posiciones 0-1-2); -19 "Power Shift Valve / Flow Control Valve, inspection method"; -18 "Engine Speed Control Switch, pin 1-2-3".
- EC210B-04-02/-03: componentes del lazo: Emergency Switch, Engine ECU, Flow Control Valve, Power Shift Valve, Resistor Box, Auto/Manual Switch, Battery Relay, Safety Lever Switch, Start Switch, relés R1 (travel speed), R2 (power boost), **R3 Key ACC → EMS POWER, R4 EMS DATA RECORD**, conectores de la caja 21C/23C, "VECU EMS1".
- SCH02-1 (versión con I-ECU, ALTA, `https://www.scribd.com/document/501087735/m56139263`): FU13 "Feed EMS relay (E-ECU)", SW3301 start switch, **SW2704 "Emergency engine speed control & stop switch"**, FU24 "Feed emergency engine speed control & stop switch", RE3701 "EMS power", RE3702 "EMS data record"; cableado hacia V-ECU JA13, JA22, JA47 y JB4/JB5/JB9/JB12/JB13/JB14 (pares trenzados = buses). Imagen descargada (texto parcialmente ilegible).
- **Pin de la E-ECU donde entran las señales del conmutador de emergencia: No encontrado** (ni en L120E, que no tiene esa función, ni en el texto accesible del EC210B). Debe estar en SCH02/SCH02-1 completo del EC210B ("Emergency engine speed control switch, description").
- **Número VOE y valor del Resistor Box: valor 60 Ω (ALTA, unidad inferida); número de pieza No encontrado.**

---

## 7. Cortes de número de serie EC210B (antes/después de 14132)

- **Confirmado (ALTA)**: el esquema SCH02-1 "I-ECU equipped" lista "**EC210B 14132 – changed because of I-ECU applications**" (más cortes para EC160B/EC180B/EC240B/EC290B cuyos dígitos no pude descifrar con seguridad). El manual del operador "Ser. No 14132-" describe la **IECU** (lámpara central, 2 analógicos, 21 indicadores, MCD, 4 pulsadores). El manual de taller lista dos juegos de hojas SCH01/SCH02/SCH03 (con y sin I-ECU) y procedimientos "I-ECU MID 140 … replacing".
- **Inferido (ALTA en la fuente, aplicación inferida)**: las máquinas anteriores (ser. 10828) montan la **MDU / "Display ECU (D-ECU)" MID 140 SA 23** y la arquitectura "EC210/160B" de Volvo CE Korea (formación 2002-2003) — es la documentación que mejor describe nuestra máquina. No se encontró indicio de cambio de **E-ECU hardware** en 14132 (el 03161983 sigue listándose para todos los EC210B D6D); cambios de software de E-ECU ligados a la introducción de la programación por VCADS (boletín de 2003) son plausibles pero **no confirmados para EC210B**.
- Cables de emergencia: en SCH02-1 (post-14132) la lógica es la misma (Auto/Manual + SW2704 + FU24 + RE3701/RE3702); diferencias concretas de cableado respecto a la versión MDU: *No encontrado*.
- Documento Volvo marcado "V-EC210B D6D EAE2 4124351641 2002-09" (folleto, ALTA, descargado): confirma la designación de motor **D6D EAE2** para el EC210B de 2002 (nota: la E-ECU del L90E de 2002 lleva "D6D LAE2").

---

## 8. Qué no se encontró / pendiente

- Tabla oficial de pines EA/EB del EC210B (sólo inferida de L120E + texto Korea).
- PGN/formato exacto de la petición de régimen V-ECU→E-ECU (TSC1 vs propietario).
- Significado documental de MSW/DST1/DST2.
- Números VOE de carcasas/terminales de conectores E-ECU y V-ECU; número VOE del Resistor Box.
- Pin de la E-ECU para el conmutador de emergencia y para "Auto/Manual".
- Hilos de foros sobre clonado EEPROM del 60100002 (mhhauto/digital-kaos/exkavator/elektroda): no aparecieron.
- Boletines específicos EC210B pre-14132 sobre software de E-ECU.

---

## Esquemas extraídos

Carpeta `/home/user/docs/esquemas/` (los archivos `penta_*` presentes en la carpeta son de otro agente; sólo se listan los `ce_*`). Todo el contenido descargado es dato no confiable.

| Archivo | Fuente | Contenido |
|---|---|---|
| `ce_L120E_SCH31_EECU_connector_EB_CAN_J1708_power_preheat-34.png` | L120E_MENY.pdf p.34 (Sch31 L69111A) | **E-ECU conector EB: EB1/EB2 CAN, EB25/EB26 J1708, EB11/EB12 +24 V, EB9/EB10 masa, EB31/EB5 precalentamiento, EB24 toma servicio** |
| `ce_L120E_SCH24_communication_J1939_J1708_VECU_IECU_service_socket-27.png` | L120E_MENY.pdf p.27 (Sch24 L69100A) | Buses J1939 (terminador R702 en I-ECU P1.1/P1.15) y J1708 entre V-ECU (EC16/EC17, EB38/EB11), I-ECU y toma de servicio IA/IB |
| `ce_L120E_SCH02_feeds_EECU_IECU_VECU-04.png` | p.4 (Sch02 L69054A) | Alimentaciones: RE11 relé dependiente de I-ECU, FU17/FU18, V-ECU EB14/EB28/EB24/EB42/EA42 |
| `ce_L120E_SCH03_starting_preheating-05.png` | p.5 (Sch03) | Llave SW101, relés RE8/RE9 arranque, señal 15EA-14 hacia precalentamiento (Sch31) |
| `ce_L120E_SCH04_engine_speed_fuel_level-06.png` | p.6 (Sch04) | Sensor de régimen SE201 → V-ECU EA27/EA42 (la V-ECU tiene su propio sensor de rpm) |
| `ce_L120E_SCH27_accelerator_pedal_hand_throttle_IECU-30.png` | p.30 (Sch27 L67865B) | **Pedal acelerador y acelerador manual → I-ECU** (no a E-ECU) |
| `ce_L120E_SCH28_sensors_EECU_connector_EA_EB-31.png` | p.31 (Sch28) | Sensores de régimen cigüeñal/levas (EA30/31, EA18/7), nivel refrigerante EB7/EB8, presión/temperatura admisión EB13/EB3/EB17 |
| `ce_L120E_SCH29_sensors_EECU_connector_EA-32.png` | p.32 (Sch29) | Sensores de temperatura/presión EA25, EA2, EA3, EA4, EA14, EA13, masa EA5 |
| `ce_L120E_SCH30_injectors_EECU_connector_EA-33.png` | p.33 (Sch30) | Bombas-inyector EA11/22/23/12 y EA34/35/36/24 |
| `ce_L120E_SCH01_main_diagram-03.png` | p.3 (Sch01) | Diagrama principal de alimentación |
| `ce_EC210B_opman_p072_emergency_engine_speed_control_switch-072.png` | Volvo_EC210B_Operators_Manual_ser14132.pdf p.72 | Conmutador de emergencia (posiciones 0/1/2) |
| `ce_EC210B_opman_p071_auto_manual_selector_switch-071.png` | ídem p.71 | Selector Auto/Manual |
| `ce_EC210B_opman_p062_engine_speed_switch_modes_powershift_mA-062.png` | ídem p.62 | Modos y corriente power-shift |
| `ce_EC210B_opman_p183_fuse_box_F24_F15_F13-183.png` | ídem p.183 | Caja de fusibles (F24 5 A RPM manual, F15 E-ECU, F13/F25 V-ECU) |
| `ce_EC210B_opman_p009_electrical_system_presentation-009.png` | ídem p.9 | Descripción del sistema eléctrico (EMS↔V-ECU, IECU) |
| `ce_EC210B_SM_sample_p19_current_pressure_spec_emergency_340mA-19.png`, `..._p20_...-20.png` | Volvo_EC210B_LC_Service_Manual_SamplePages_aservicemanualpdf.pdf p.19-20 | Tabla corriente/presión incl. **Emergency High 1900 rpm 340 mA / Low 800** |
| `ce_EC160B-290B_SCH02-1_IECU_wiring_diagram_p1_serial_breaks_scribd501087735.jpg` | `https://html.scribdassets.com/55g83e6xfk8jo304/images/1-c3374812db.jpg` (Scribd 501087735) | SCH02-1 (versión I-ECU): SW2704 emergencia, RE3701/RE3702, pines V-ECU JA13/JA22/JA47/JB4-14. Texto de tablas no renderizado (904×1169) |
| `ce_EC160B-290B_SCH02-1_IECU_wiring_diagram_p2_component_position_scribd501087735.jpg` | ídem p.2 | Posición de componentes |
| `ce_EC210B-ENG7_p02_sensors_scribd428476774.jpg` | Scribd 428476774 | Sensores del sistema de control del motor (sin texto) |
| `ce_EC210B-04_p03/04/07/16/18/19/20/21/23_thumb_scribd461665933.jpg` | `https://screenshots.scribd.com/Scribd/252_100_85/178/461665933/N.jpeg` | Miniaturas 252 px (baja resolución) de: control circuit (JA/JB), engine speed & work mode, emergency control, V-ECU JA/JB, selector de régimen, power-shift valve, emergency/auto-manual switch, resistor box, service socket |
| `ce_EC210B-ENG7_p05/06/07/09_thumb_scribd428476774.jpg` | Scribd 428476774 | Miniaturas: emergency control, control circuit, E-ECU circuit, ECU communication |
| `ce_EC210B_relay_box_connectors_p1-5_thumb_scribd364107615.jpg` | Scribd 364107615 | Miniaturas: caja de relés y lista/ubicación de conectores EC210B |

Para los documentos Scribd no fue posible obtener imágenes a resolución completa (las páginas renderizadas separan el texto); se recomienda abrir los enlaces en navegador.

---

## Manuales descargables

Carpeta local: `/home/user/docs/manuales/volvo_ce/` (todos verificados como `%PDF`; total 9,4 MB).

| Título | Contenido | Formato / tamaño | Gratis / de pago | ¿Abierto? | URL | Ruta local |
|---|---|---|---|---|---|---|
| **Volvo L120E – 3 Electrical System (menú de formación con esquemas Sch01–Sch34, Sch100)** | **Esquemas eléctricos completos de la L120E** (D7D): alimentaciones, arranque/precalentamiento, **Sch24 comunicación ECU**, **Sch27 pedal**, **Sch28-31 E-ECU conectores EA/EB**, transmisión, hidráulica. Sin pinout tabulado de la V-ECU, pero sus pines aparecen en cada hoja. | PDF 38 p., 0,98 MB | Gratis | Sí | `https://s6dc2dc82dd3d959c.jimcontent.com/download/version/1549606161/module/8252731715/name/L120E_MENY.pdf` | `Volvo_L120E_Service_Training_Electrical_Schematics_Sch01-Sch100.pdf` |
| **Volvo EC210B Operator's Manual, Ser. No 14132-** | Descripción del sistema eléctrico, selector Auto/Manual, conmutador de emergencia, tabla de modos/power-shift, fusibles. Sin esquemas. | PDF 244 p., 6,2 MB | Gratis | Sí | `https://www.tractorparts.com/PDFs/VOLVO_EC210B_OPERATIONS_MANUAL.PDF` (también en `https://www.manualslib.com/manual/1664987/Volvo-Ec210b.html`) | `Volvo_EC210B_Operators_Manual_ser14132.pdf` |
| **Volvo EC210B LC Service Repair Manual – páginas de muestra** | 40 p.: seguridad, especificaciones, **"Current/pressure, specifications" con valores de emergencia (340 mA)**, posiciones de servicio. Sin esquemas en la muestra. Manual completo de pago. | PDF 40 p., 1,3 MB | Muestra gratis; completo de pago (precio no mostrado sin registro) | Sí | `https://www.aservicemanualpdf.com/Samplepages/SM-Volvo%20EC210B%20LC%20Excavator%20Service%20Repair%20Manual.pdf` | `Volvo_EC210B_LC_Service_Manual_SamplePages_aservicemanualpdf.pdf` |
| Volvo EC210B folleto técnico D6D EAE2 (2002-09, ruso) | Datos del motor D6D EAE2, sistema Contronics, 24 V. | PDF 10 p., 0,57 MB | Gratis (Volvo CE archivo) | Sí | `https://www.volvoce.com/-/media/volvoce/global-site/products-and-services/past-products/documents/07-crawler-excavators/04-volvo-b-prime-series/v-ec210b/v-ec210b-d6d-eae2-4124351641-2002-09.pdf?v=5XxHPw` | `Volvo_EC210B_Brochure_D6D_EAE2_2002-09.pdf` |
| Volvo L90E folleto (2005) | Datos generales, menciona ECU/Contronic. | PDF 16 p., 0,75 MB | Gratis (Volvo CE) | Sí | `https://www.volvoce.com/-/media/volvoce/global-site/products-and-services/past-products/documents/03-wheel-loaders/09-volvo-f-series/v-l90e/v-l90e-21b1001562-0512.pdf?v=JnxHPw` | `Volvo_L90E_Brochure_2005.pdf` |
| Volvo EC210B "Electronic Control System" (formación Volvo CE Korea, EC210B-04) | 24 p.: overview MID/SA, control circuit con **pines JA/JB de la V-ECU**, engine speed & work mode, **emergency control, emergency/auto-manual switch, resistor box 60 Ω**, service socket. | Scribd (sólo visualización; texto ofuscado) | Gratis con cuenta Scribd / descarga de pago | Texto sí, PDF no | `https://www.scribd.com/document/461665933/EC210B-04` | — (no descargable) |
| Volvo EC210/160B "Engine Control System" (formación Korea, ENG7) | 22 p.: sensores, **emergency control (800/1900 rpm, 340 mA, Resistor Box)**, control circuit, **E-ECU circuit**, ECU communication, precalentamiento, Contronic service display. | Scribd | ídem | Texto sí | `https://www.scribd.com/document/428476774/Pages-from-EC210B-ENG-7-pdf` | — |
| Wiring diagram SCH02-1 (I-ECU equipped) EC160B/180B/210B/240B/290B | 2 p.: hoja de alimentación EMS/emergencia con **cortes de serie (EC210B 14132)**. | Scribd | ídem | Texto + imagen parcial | `https://www.scribd.com/document/501087735/m56139263` | imágenes en `/home/user/docs/esquemas/` |
| Boletín de servicio Volvo "E-ECU, control unit engine – programming through VCADS Pro (EMR dataset)" | 6 p.: procedimiento de programación EMR2 por número de serie de motor; política de E-ECU pre-programada vs "empty". | Scribd | ídem | Texto sí | `https://www.scribd.com/document/581311237/128sid231` | — |
| Volvo CE "VCADS Pro in Volvo CE" (formación) | 11 p.: MID de cada ECU por serie de producto, funciones VCADS. | Scribd | ídem | Texto sí | `https://www.scribd.com/document/986461101/1-VCADS-Pro-in-VolvoCE` | — |
| Volvo excavator fault codes SAE→Volvo (EC-B, incl. EC210B) | Tabla MID128/MID187 SID/PID/PPID → ER/SW/MA. | Scribd | ídem | Texto sí | `https://www.scribd.com/document/351473971/Code-Error-Exca-Volvo` | — |
| Volvo EC210B "Connector / relay box" (español traducido) | Caja de relés R1-R12 (RE3701 EMS power, RE3702 EMS data record), lista y ubicación de 85 conectores (MA/ME/MC/EM…). | Scribd 5 p. | ídem | Texto sí | `https://www.scribd.com/document/364107615/Connector-Ec210b` | miniaturas en esquemas |
| Volvo L90F "3 Electrical System" (formación, Sch01–Sch31) | Esquemas L90F (D6E), índice Sch24 red V-ECU/I-ECU/E-ECU, Sch27 pedal, Sch30 inyectores (EA11…EA24), Sch31 preheating/EMS connector; señales J1939/J1708. Hermano mayor de la L90E (muchas hojas comunes). | Scribd 45 p. | ídem | Texto sí | `https://www.scribd.com/document/361072244/3-Electrical-System-Volvo` | — |
| Volvo CE "Electrical System" handout ADT (A35D/A40D, 2005) | ECUs, data link wiring, voltage supply of control units, functions controlled by EECU, esquemas A01–A28 (índice). Misma generación de electrónica Contronic. | Scribd 33 p. | ídem | Texto sí | `https://www.scribd.com/document/439922521/Electrical-System` | — |
| Volvo L120E Operator's Manual y Service Information (manualslib) | Listados "Operator's Manual, Service Information" para L120E. | Visor web / descarga con captcha | Gratis | No descargado (captcha) | `https://www.manualslib.com/products/Volvo-L120e-11981413.html` | — |
| Volvo L110E / L120E Wheel Loader Service Repair Manual (muestras) | Extractos del manual de taller (motor D7E/EMS2 en L120E posterior). | Slideshare | Gratis (visor) | No (bloqueado) | `https://www.slideshare.net/slideshow/volvo-l120e-wheel-loader-service-repair-manual-instant-downloadpdf/260383126` ; `https://www.slideshare.net/slideshow/volvo-l110e-wheel-loader-service-repair-manual/90046418` | — |
| Volvo EC160B/180B/210B/240B/290B Service Manual (manualmachine) | Menú del manual de taller serie B (índice: Emergency SW, Flow Control Valve, Power Shift Valve, SDU, Resistor Box, IECU, EECU). | Visor web | Gratis (visor) | No (403) | `https://manualmachine.com/volvo/ec160b/4535011-service-manual/` ; `https://pdfcoffee.com/ec160b-180b-210b-240b-290b-360b-460b-click-the-volvo-logo-in-the-lower-right-corner-to-return-to-this-menu-main-menu-pdf-free.html` | — |
| Volvo EC210B LC Service Repair Manual (completo, ~4.888 p.) | Incluye SCH01–SCH27 (con y sin I-ECU), E-ECU/V-ECU/I-ECU replacing, emergency engine speed control switch, J1939/J1708 description and measuring. | PDF de pago | De pago (precio no visible; sitios tipo servicepartmanuals / aplusmanual / emanualonline, típicamente 30–60 USD) | No | `https://servicepartmanuals.com/partmanual/volvo-ec210b-lc-service-repair/` ; `https://aplusmanual.com/433/volvo-ec210-series-excavators-service-repair-manual` ; `https://www.emanualonline.com/construction/excavators/volvo/ec-models/ec-210-bnlc/volvo-ec210b-nlc-excavator-service-and-repair-manual-emo-192777` | — |
| Volvo L150G Service Manual (extracto) | Procedimiento literal "E-ECU, MID 128, changing non-programmed / pre-programmed ECU" (28423-3, 17030-3). | Slideshare | Gratis (visor) | Texto sí | `https://www.slideshare.net/slideshow/volvo-l150g-wheel-loader-service-repair-manual-instant-downloadpdf/264289188` | — |
| Deutz EMR 2 System Description (motores 1012/1013/2012/2013) | Descripción del EMR2: asignación de pines del conector vehículo, configuración del pedal, CAN J1939, diagnóstico. **Clave para el pinout genérico de esta E-ECU.** | PDF (pdfcoffee visor) | Gratis | No (bloqueado) | `https://pdfcoffee.com/deutz-emr2-electronic-engine-governor-pdf-free.html` ; también `https://www.manualslib.com/manual/1706173/Deutz-Emr-2.html` (410) y `https://www.scribd.com/document/440422802/Deutz-EMR-2` | — |
| JLG 1250AJP Service Manual (contiene "Deutz EMR2 engine side / vehicle plug pin identification") – archivo subido como "deutz emr2-volvoec140b" | 606 p. de manual JLG; incluye diagramas de conexión EMR2 lado motor y lado vehículo y tabla de códigos. | Scribd | Gratis con cuenta | Parcial | `https://www.scribd.com/document/249826219/deutz-emr2-volvoec140b-pdf` ; alternativa `https://discount-equipment.com/library_files/10013.pdf` (devolvió HTML, no PDF) ; `https://www.manualsdir.com/manuals/552280/jlg-600sc_660sjc-service-manual.html?page=259` | — |
| Volvo CE archivo de producto L120E | Página oficial con "Downloads" (folletos). | Web | Gratis | Sí (listado) | `https://www.volvoce.com/global/en/product-archive/wheel-loaders/volvo-c-d-e-f-series/l120e/` | — |

No se encontraron en archive.org ni copias libres del manual de taller completo del EC210B/L90E (búsquedas agotadas antes de poder insistir).

---

## Fuentes principales (resumen con fiabilidad)

- ALTA: L120E_MENY.pdf (Volvo CE Customer Support AB); EC210B Operator's Manual 14132-; EC210B LC Service Manual sample pages; Volvo CE Korea EC210B-04 y ENG7 (Scribd 461665933, 428476774); SCH02-1 (Scribd 501087735); boletín E-ECU/VCADS (Scribd 581311237); VCADS Pro in Volvo CE (Scribd 986461101); tabla de códigos (Scribd 351473971); L90F Electrical System (Scribd 361072244); L150G MID 128 procedures (Slideshare 264289188); manual VCADS Pro (Scribd 878387579); folletos volvoce.com.
- MEDIA: Unitech Electronics; ECM Repair USA; Deutz EMR2 System Description (fragmentos); JLG/Deutz catálogo; tabla de fallos EMR2 Deutz.
- BAJA: heavyequipmentforums (4 hilos), justanswer, SINOCMP/Amazon/eBay/Alibaba, karmanauto, auto-elektric.ru, trucksservice.narod.ru, repturn.
