# Investigación: DEUTZ EMR2 (EMR 2) y su relación con la E‑ECU del Volvo EC210B (D6D EAE2)

Fecha: 2026‑10‑19. Idiomas de búsqueda: inglés y alemán (también francés, por un hallazgo).
Fiabilidad: **ALTA** = documento oficial Deutz/Volvo; **MEDIA** = manual de integrador OEM (ComAp, DEIF, Woodward, JLG, Smartgen…); **BAJA** = foro / vendedor / copia sin procedencia clara.
Etiquetas: **CONFIRMADO** (texto o imagen de una fuente verificada), **INFERIDO** (deducción razonada a partir de fuentes), **NO ENCONTRADO**.

---

## 0. Resumen ejecutivo

1. **La documentación oficial Deutz del EMR2 existe y se ha podido descargar** (copia de terceros del documento Deutz *0297 9885 "System Description Electronic Engine Governor EMR 2"*, ed. 06/02, parte inglesa, 60 páginas) → `/home/user/docs/manuales/deutz_emr2/Deutz_EMR2_System_Description_0297_9885_EN_06-2002_60p_idoc-tips.pdf`. Incluye las tablas de pines del conector de motor (M) y del conector de vehículo (F), ambos de **25 polos**, y los esquemas de conexión (incl. CAN/diagnóstico).
2. **El EMR2 "de catálogo" Deutz usa dos conectores AMP de 25 polos**, no de 36. **No se ha encontrado ninguna variante EMR2 con 2 × 36 pines** en ninguna fuente (Deutz, JLG, ComAp, DEIF, Woodward, Volvo Penta). La E‑ECU Volvo 03161983/20577135 (2 × 36 pines, "LucasVarity, Made in UK") **no coincide físicamente** con el hardware EMR2 documentado.
3. **La relación Volvo ↔ EMR2 sí está confirmada a nivel de protocolo/firmware por los integradores**: ComAp lista "Volvo EDC4 (EMR2)" para motores Volvo D5/D7 y remite al capítulo Deutz EMR2; Woodward easYgen‑1600 agrupa "Deutz EMR2 / Volvo EDC4" en una sola entrada de ECU con el mismo cableado (conector F pines 1/12/13/14); Smartgen pone "Engine type: VOLVO‑EDC4" dentro de su apartado "DEUTZ EMR2". Es decir, Volvo Penta llamó **EDC4** a la aplicación Volvo del EMR2 (motores TAD520/720 = Deutz 1012/1013). Para la E‑ECU de los Volvo CE D6D/D7D (Deutz 2012/2013 con bombas unitarias), la hipótesis "variante Volvo del EMR2" queda **INFERIDA (software/protocolo)**, pero **el hardware de 36 pines no está documentado como EMR2** en ninguna fuente.
4. **CAN del EMR2 (CONFIRMADO en fuentes MEDIA):** J1939, 250 kbit/s (fuente oficial Deutz solo dice "SAE J1939"; la cifra 250/100 kbit/s viene de una copia de la "CAN Doku EMR2" de 2004, BAJA), acepta **TSC1** como consigna de velocidad; **dirección fuente por defecto del controlador emisor = 3** (DEIF, para EMR2/EMR3/EMR Generic); paro del motor por **telegrama propietario "Engine Stop Request"**; se activa por SERDIA con parámetros 4400 (CAN on), 4412 (recibir TSC1a), 4470 (consigna CAN por TSC1a), 4829/4424 (stop request), 4900 (tipo de canal de consigna) (ComAp).
5. **Pérdida de consigna CAN (CONFIRMADO, doc. Deutz §4.15 Limp home):** el EMR2 puede conmutar, si falla la consigna por CAN, a (a) el pedal acelerador y/o (b) una "velocidad auxiliar" (Notlaufdrehzahl) configurable con SERDIA. En un caso real de foro (BF6M1013 con EMR) la pérdida de CAN llevó al motor a "plena carga" porque la velocidad de emergencia estaba configurada alta (BAJA).
6. **Consigna por potenciómetro en el conector de vehículo (CONFIRMADO):** sí, EMR2 admite pedal/potenciómetro 1 kΩ (pines F25 +5 V, F24 señal, F23 GND), tensión externa 0,5–4,5 V (F24/F23), y acelerador manual 1 kΩ (F25/F20/F23) con función "máximo" entre pedal y handgas. Que el *dataset Volvo* de la E‑ECU de 36 pines lo permita es **NO CONFIRMADO**: la E‑ECU de los EC‑B recibe la consigna del V‑ECU por J1939 y el único mando "físico" conocido es la entrada B4 "Emergency speed control" (ver §4.4).
7. **Fabricante del hardware EMR2:** **NO ENCONTRADO** en ninguna fuente pública (ni Lucas, ni TRW, ni Bosch como fabricante de la ECU; Bosch solo aparece como fabricante del *actuador EDC* del 1015). La placa "LucasVarity / Made in UK" de la unidad Volvo es un dato propio (ya confirmado en `INVESTIGACION_V-ECU_EC210B.md`).

---

## 1. Documentación oficial Deutz del EMR2

### 1.1 "System Description Electronic Engine Governor EMR 2" / "Systembeschreibung Elektronischer Motor‑Regler EMR 2" — Deutz **0297 9885 de/en**

- Identidad del documento: **CONFIRMADO**. Título bilingüe, nº 0297 9885 de/en, ediciones 03/02 y 06/02; cubre las series **1012/1013/2012/2013/1015** ("1) same system with Bosch EDC‑actuator (1015)"). Fuentes: índice del Scribd "S08‑EMR2‑EN" (https://www.scribd.com/document/554966444/S08-EMR2-EN , BAJA), PDFCoffee "Emr2 de en" (https://pdfcoffee.com/emr2-de-en-pdf-free.html , BAJA, bloquea descarga automática), ManualsLib "Deutz EMR 2 System Description" (https://www.manualslib.com/manual/1706173/Deutz-Emr-2.html , BAJA, bloquea).
- **Descargado y verificado** (parte inglesa, páginas 65–118 del original bilingüe, 60 páginas PDF, generado con pdftk/Ghostscript, con el logo Deutz y "© 06/02" en cada página): https://idoc.tips/deutz-emr2-electronic-engine-governor-pdf-free.html → `/home/user/docs/manuales/deutz_emr2/Deutz_EMR2_System_Description_0297_9885_EN_06-2002_60p_idoc-tips.pdf`. Fiabilidad del contenido: **ALTA (texto Deutz)**; procedencia de la copia: BAJA. Nota: algunas páginas están recortadas por abajo (tablas truncadas); la traducción francesa (abajo) completa esas tablas.
- **Traducción francesa automática de las mismas páginas 59–118** (adjunto de foro, 60 p., contiene íntegra la tabla "Aperçu des fonctions, affectation des broches" y el texto completo de §4.15 Limp home): https://forums.futura-sciences.com/attachments/electronique/427604d1607857752-mli-manuel-emr2-de-059-118-..fr.pdf → `/home/user/docs/manuales/deutz_emr2/Deutz_EMR2_Systembeschreibung_traduction_FR_p59-118_futura-sciences.pdf` (BAJA como copia; contenido = Deutz).
- Contenido (capítulos): 1 Introducción, 2 Notas, 3 Descripción del sistema, 4 Funciones (4.3 control de velocidad, 4.4 consignas, 4.5 curvas de potencia, 4.6 estatismo/P‑grado, 4.7 arranque/paro, 4.9 LDA, 4.11 velocidad de vehículo F7, 4.12 protección, 4.13 corrección de altitud, 4.15 **Limp home**, 4.16 arranque en frío), 5 Interfaces (5.1 diagnóstico ISO 9141, 5.2 **CAN SAE J1939**), 6 Configuración (6.1 **tabla funciones/pines**), 7 Botón de diagnóstico y códigos de parpadeo, 8 Sustitución de componentes, 9 Datos técnicos (9.2 especificación de señales, **9.3.1 conector motor M, 9.3.2 conector vehículo F**, 9.4 sensores), 12 **Esquemas de conexión** (12.1 lado vehículo/instalación, 12.2–12.3 lado motor hojas 1–2, 12.4 **CAN‑Bus y línea de diagnóstico**).
- Frase clave sobre pines (CONFIRMADO, §3.3/§5): "there are different variations of the functions and the pin assignments of the plugs … For pin assignment see the application‑dependent switch diagrams" y "Only the switching diagram specific for the particular engine is binding" (§12).

### 1.2 "EMR2 Installation instructions" / Einbauanleitung

- **NO ENCONTRADO** como PDF libre. Existe un "Installation Manual – Electronic governors for DEUTZ diesel engines (EMR2, EMR3, EMR4)" en manualzz (https://manualzz.com/doc/37731658/installation-manual-electronic , BAJA, bloquea la descarga; menciona "max. cable length battery–control unit 7 m"). El propio 0297 9885 remite a las "Installation Guidelines for electronic systems of DEUTZ diesel engines".

### 1.3 "EMR2 CAN bus interface description" / "CAN Doku EMR2" / "CAN‑Specification EMR2"

- Existencia **CONFIRMADA** por índices de terceros, descarga **NO conseguida** (Scribd y PDFCoffee bloquean el acceso automatizado):
  - "CAN Specification EMR2 engl" (50 p., Scribd, BAJA): https://www.scribd.com/document/638279672/CAN-Specification-EMR2-engl — "supported standards, baud rates, message identifiers, diagnostic functions… SAE J1939 and EMR2‑specific CAN messages".
  - "CAN Doku EMR2 Engl" (PDFCoffee, BAJA, fechada **29.01.2004**): https://pdfcoffee.com/can-doku-emr2-engl-pdf-free.html — fragmentos indexados: "baud rate is **250 K Bit/s or 100 K Bit/s**"; "additional messages are defined specially for EMR beyond the SAE J1939 standard"; "if a data … is not used … the content must be FF"; TSC1 descrito como mensaje para "send a commanded (or desired) engine speed to the ECM"; "Multipacket Transport Protocol" para mensajes >8 bytes.
- Documentos equivalentes de generaciones posteriores sí están accesibles (útiles solo como referencia de formato): EMR3 CAN BUS Specification v11.3 (https://www.scribd.com/doc/135565695/Deutz-emr3-CAN-BUS-specification-V11-3 ; https://docplayer.net/5821322-Emr-3-can-bus-specification.html), EMR4 TIER4f CAN (https://docplayer.net/39752039-Emr-4-tier4f-can-bus-specification-customer.html ; https://idoc.pub/documents/deutz-emr4-tier4f-can-3no78p3ek5ld).

### 1.4 "EMR2 vehicle connector pin assignment" (Fahrzeugstecker)

- **CONFIRMADO** y descargado como parte del 0297 9885 (§9.3.2, PDF p. 47) y, con mejor legibilidad, en el manual de servicio JLG 3121607 (Fig. 3‑56 "EMR 2 Vehicle Plug Pin Identification", que reproduce la tabla Deutz). Ver §2.3.

### 1.5 Sitio oficial Deutz (SerDia)

- https://serdia.deutz.com/en/serdia2000/ (ALTA): "SerDia 2000 supports the earlier ECUs like **EMR1, EMR2**, EMR3, Deutz‑EMS, MVS, EMS2.1 and V‑ECU… Interface: **HS‑Light (Access‑Level controlled)**… Windows XP/2000". Descargas oficiales: SerdiaSetup_V1.8.6.exe, SetupSamDiaX_5.4.5.0.exe. En `fileadmin/contents/serdia/` solo hay listas DTC para EMR L1, MD1, EMR4 (KWP), LPG — **no hay lista DTC ni documentación EMR2** en abierto.

---

## 2. Hardware del EMR2

### 2.1 Fabricante

- **NO ENCONTRADO.** Ninguna fuente pública (Deutz, JLG, ComAp, DEIF, Woodward, vendedores) nombra al fabricante de la caja EMR2. Deutz la presenta como desarrollo propio ("EMR 2 is a further development of the previously utilized EMR", 0297 9885 §1). El único "Bosch" en el documento se refiere al **actuador EDC del 1015** y a la bomba ("Actuator (EDC‑actuator) and Bosch pump belong together"). Un taller alemán llama al EMR2 "Bosch‑Gerät" (https://ahbu.de/… , BAJA, sin pruebas). Búsquedas "Lucas / LucasVarity / TRW / Delphi + EMR2" en inglés y alemán: sin resultados pertinentes. LucasVarity (1996–1999) vendió Lucas Diesel Systems a Delphi en 2000 y fue absorbida por TRW en 1999 (https://en.wikipedia.org/wiki/LucasVarity , MEDIA‑ALTA, contexto).
- Dato propio del usuario (CONFIRMADO en `INVESTIGACION_V-ECU_EC210B.md`): la placa de la E‑ECU Volvo 03161983 dice "A Product developed in partnership with LucasVarity · Made in UK". Esto fecha el *diseño del hardware Volvo* en 1996–1999, pero **no vincula ese hardware al EMR2 Deutz** en ninguna fuente.

### 2.2 Conectores y número de pines (CONFIRMADO)

- 0297 9885 §9.3: "The **25‑pole plugs** of the EMR 2 control unit are mechanically coded (different part numbers). … the vehicle plugs (F) or the plant plugs (F) and engine plug (M) only [fit] into the sockets provided for them". Índice: "AMP plug = Multi‑pole plug of the AMP company". Datos técnicos: 231 × 204 × 62 mm, 1,6 kg, −40…+85 °C, fusible 15 A, longitud máx. cable batería–ECU 7 m.
- Volvo Penta "EDC 4" (Workshop Manual Group 23, índice en PDFCoffee, BAJA): "**2 x 25‑pin (AMP) connector**" → coherente con hardware EMR2 estándar en los TAD520/720.
- ComAp (MEDIA): "ECU **25pin F connector**: CAN H = 12, CAN L = 13, Battery + = 14, Battery − = 1".
- Woodward easYgen‑1600 (MEDIA, manual B37699A ya en carpeta): "Deutz EMR2 / Volvo EDC4 — F connector: 1 = battery negative, 12 = CAN(H), 13 = CAN(L), 14 alimentado por relé 30 A, fusible 16 A".
- **Variante 2 × 36 pines: NO ENCONTRADA** en ninguna fuente EMR2. La única ECU de 36 pines en los resultados es Bosch MEMS (automoción, irrelevante).

### 2.3 Tabla del conector de vehículo F (25 polos) — Deutz 0297 9885 §9.3.2 / JLG 3121607 Fig. 3‑56 (CONFIRMADO)

| Pin F | Designación Deutz | Descripción |
|---|---|---|
| 1 | U Batt − | Negativo batería (borne 31) |
| 2 | GND | Referencia de señal |
| 3 | Output digital 2 | Salida PWM/digital (p. ej. aviso temperatura refrigerante) |
| 4 | DigInOut | **Lámpara de fallo y botón de diagnóstico** |
| 5 | Output PWM1/Dig1 | Salida PWM/digital (p. ej. aviso aire de carga) |
| 6 | DigIn 3 | Genset / cambio de marcha / freno motor |
| 7 | Digital 10 / velocity | Señal de velocidad de vehículo (taco, DIN 11786) |
| 8, 9 | NC | — |
| 10 | L‑line | ISO 9141 |
| 11 | K‑line | ISO 9141 |
| **12** | **CAN high** | Interfaz CAN‑Bus (SAE J1939) |
| **13** | **CAN low** | Interfaz CAN‑Bus |
| 14 | U Batt + | Positivo (borne 15, llave) |
| 15 | Output digital 5 | Salida digital (p. ej. aviso presión aceite) |
| 16 | Output digital 7 / Frequency | Salida de frecuencia/PWM (p. ej. velocidad motor) |
| 17 | Ground | Referencia para entradas 18, 19 y 21 |
| 18 | Digital 1 / PWM 1 | Entrada digital/PWM 1: conmutación de velocidad (velocidad 1/2, fija/variable, congelar, min/max) o PWM 1 |
| 19 | DigIn 4 | Conmutación de curva de potencia 1/2 / genset (DIG‑UP) |
| 20 | Digital 8 / analog 3 | **Acelerador manual (handgas)** / genset / entrada analógica 3 |
| 21 | Digital 2 / PWM 2 | Entrada digital/PWM 2: conmutación de P‑grado 1/2 |
| 22 | Screen | Pantalla (cables de handgas o PWG) |
| 23 | GND | Referencia para pin 24 |
| 24 | Analog 1 / digital 6 | **Pedal (PWG) o tensión externa 0,5–4,5 V** |
| 25 | +5 V REF | Referencia 5 V para pin 24 (máx. 30 mA PWG+handgas) |

Esquema 12.1 (lado vehículo) muestra además: pedal (B46) en 25/24/23/22, handgas en 20, interruptores "speed switch", "limiting torque curve switch / DIG‑UP genset", "speed droop switch", "engine brake/gear switch", "speed signal / DIG‑DOWN genset", lámparas en 3/4/5/15/16, CAN 12/13 hacia conector de diagnóstico X22 (CAN‑H/L, ISO‑L, ISO‑K, +UBatt borne 15, GND) y "bus terminal resistance for CAN‑interface SAE J1939 to be mounted externally".

### 2.4 Tabla del conector de motor M (25 polos) — §9.3.1 / JLG Fig. 3‑55 (CONFIRMADO)

1 reserva · 2 salida digital 3 (solenoide de paro, <4 A) · 3 salida digital 4 (brida calefactora/bujías) · 4 temp. combustible · 5 temp. aire de carga · 6 nivel refrigerante/aceite · 7 PWM2/dig 6 · 8 GND · 9 NTC refrigerante · 10 GND · 11 velocidad 2 (cigüeñal, opc.) · 12 GND · 13 velocidad 1 (árbol de levas) · 14 STG− · 15 STG+ (bobina actuador, PWM) · 16 pantalla · 17 RF− · 18 RF REF · 19 RF MESS (sensor de carrera de cremallera) · 20 GND · 21 presión aceite · 22 +5 V REF (15 mA) · 23 GND · 24 presión aire de carga · 25 +5 V LDA.

**Observación clave (INFERIDO):** el conector M del EMR2 está pensado para **un actuador de cremallera** (bobina STG± + sensor inductivo RF) y un solenoide de paro, no para 4–6 electroválvulas de bombas unitarias. El D6D EAE2 (BF6M2012C, bombas unitarias con electroválvulas) necesita 6 etapas de potencia → otro hardware. Esto explica los 2 × 36 pines de la E‑ECU Volvo y es coherente con que **ninguna fuente describa un EMR2 para bombas unitarias**.

### 2.5 Comparación conector F (EMR2) ↔ conector B (Volvo E‑ECU)

| Función | EMR2 conector F (Deutz, CONFIRMADO) | Volvo conector B (dato del usuario) | Coincide |
|---|---|---|---|
| CAN‑H / CAN‑L | F12 / F13 | B1 / B2 | Función sí, **pines no** |
| J1708/J1587 | **no existe** en EMR2 (diagnóstico = ISO 9141 K/L en F11/F10) | B25/B26 J1708 | **No** (J1708 es específico Volvo) |
| GND | F1 (−batería), F2, F17, F23 | B9/B10 | Función sí, pines no |
| +24 V (borne 15) | F14 (único positivo, 15 A) | B11/B12 (dos pines) | Función sí, pines no |
| Consigna de emergencia | F24 analógica 0,5–4,5 V / pot; F18/F19/F21 digitales de conmutación | B4 "Emergency speed control" | **Indeterminado** (ver §4.4) |
| Relé de precalentamiento | **M3** (lado motor, salida digital 4 "heating flange/glow plug") | B31 (lado vehículo) | Función sí, **lado distinto** |
| Realimentación calentador | no documentada | B5 | No encontrado |
| Nivel refrigerante | **M6** (lado motor) | B7/B17 (lado vehículo) | Función sí, lado distinto |
| Presión/temp. aire admisión | **M24/M25/M23** presión LDA y **M5** temperatura (lado motor) | B8/B3/B13 (lado vehículo) | Función sí, lado distinto |

**Conclusión (INFERIDO):** la asignación Volvo B no es un "renumerado" del conector F del EMR2; comparte el *catálogo de funciones* (CAN J1939, lámpara/diagnóstico, precalentamiento, nivel refrigerante, sensores de aire de carga, consigna externa) pero la distribución motor/vehículo y el número de pines son distintos. Los únicos solapamientos exactos son conceptuales (CAN, alimentación, masa).

---

## 3. Comportamiento CAN del EMR2

| Aspecto | Hallazgo | Fuente / fiabilidad | Estado |
|---|---|---|---|
| Protocolo | SAE J1939 ("The SAE J1939 protocol is utilized for communication", §5.2); "CAN‑bus protocol to SAE J1939 has been considerably extended, but remains upwards compatible to the present EMR applications" (§4.2) | Deutz 0297 9885 (ALTA) | CONFIRMADO |
| Bitrate | 250 kbit/s (o 100 kbit/s configurable) | "CAN Doku EMR2" 2004 vía PDFCoffee (BAJA); DEIF AGC150 "general default… J1939, 250 kb/s" (MEDIA) | CONFIRMADO (MEDIA) |
| Dirección fuente del motor (SA) | DEIF: "By default, the engine is expected to use source address 0" (parámetro 7562 EIC SA) | DEIF 4189341302I (MEDIA) | INFERIDO SA=0 (no específico EMR2) |
| Acepta TSC1 (PGN 0) | Sí: "J1939 message: TSC1", "Speed control ●", "Idle mode ●", "50/60 Hz ●", "Start −", "Shutdown override −" | DEIF AGC150 §3.7.1, AGC‑4 MkII §3.6.1, Omni §6.5.3 (MEDIA); ComAp "Requested speed SPN 898" (MEDIA) | CONFIRMADO |
| SA del emisor de TSC1 | "Default speed control source address: **3**" (igual para EMR2/EMR3/EMR Generic); DEIF: "You can ask the engine manufacturer to verify the TSC1 source address" | DEIF (MEDIA) | CONFIRMADO (como valor por defecto del integrador) |
| Formato TSC1 | Byte 1 = 0x01 (override control mode = speed control), bytes 2–3 = rpm × 8 LE (datos EMR4/J1939 genérico; foro PLUS+1: "all bits are set to zero except for the engine control mode… first byte 01") | Foro Danfoss PLUS+1 (BAJA), blog EMR4 (BAJA) | INFERIDO (estándar J1939‑71) |
| Tasa TSC1 | 10–50 ms típicos; IQAN avisa de error "abnormal update rate" si es lento (defecto 50 ms) | foro IQAN (BAJA); DEIF "TSC1 TX rate" 15120 | INFERIDO |
| Paro por CAN | Telegrama **propietario Deutz "Engine Stop Request"** (DEIF: "When the controller wants to stop the engine, it sends this proprietary telegram"); ComAp: "Stop Request – proprietary parameter", "Lock status – proprietary" | DEIF, ComAp (MEDIA) | CONFIRMADO (existe), definición de bytes NO ENCONTRADA |
| PGN propietarios de consigna / velocidades fijas | NO ENCONTRADO el detalle; ComAp y DEIF usan **TSC1** como consigna, no un PGN propietario | — | NO ENCONTRADO |
| Difusión (broadcast) | ComAp lee SPN 190 velocidad (EEC1), 91 pedal, 92 carga, 512/513 par (EEC1), 110 temp. refrigerante (ET1), 174 temp. combustible (ET1), 175 temp. aceite, 98 nivel aceite, 100 presión aceite (EFL/P1), 111 nivel refrigerante (EFL/P1), 183 caudal (LFE), 102/105 presión/temp. colector (IC1), 158 tensión batería (VEP1), lámparas DM1 (623/624/987/1213), 1081 wait‑to‑start; DEIF: DM1 (amarilla/roja/protect/malfunction) y DM2, horas motor, presión atmosférica | ComAp 7.0.0 §3.6.2 (MEDIA), DEIF (MEDIA) | CONFIRMADO |
| Pérdida de consigna CAN | Deutz §4.15 (trad.): "Il est également possible, en cas d'échec du point de consigne par défaut [vía] bus CAN, de basculer a) sur la pédale d'accélérateur et b) en vitesse auxiliaire. Le type de dysfonctionnement est défini dans la mémoire des défauts." Manual de servicio EMR2 (Scribd 440422802): "DTC 1629 – J1939 TSC1 Message Receipt Loss… the ECM must operate the engine at a default idle speed until commanded to do otherwise" | Deutz 0297 9885 (ALTA); Scribd (BAJA) | CONFIRMADO (fallback a pedal y/o velocidad auxiliar configurable) |
| Caso real | Bauforum24: BF6M1013+EMR en extendedora; al perder CAN ("can bus off") el EMR entró en Notlauf y "sofort nach Starten des Motors geht der Motor auf Vollgas"; consejo: "mit SERDIA und dem entsprechenden Userlevel die Notlaufdrehzahl auf eine mittlere Drehzahl setzen" | https://www.bauforum24.biz/forums/topic/29667-emr-schaltplan-deutz/ (BAJA) | CONFIRMADO (anecdótico) |
| Restricción Deutz genset | ComAp 2020: "it is not allowed by Deutz to control speed over CAN bus on gen‑set engines" (contexto EMR3) | ComAp (MEDIA) | CONFIRMADO para EMR3; aplicabilidad a EMR2 INFERIDA |

### 3.1 Parámetros SERDIA del EMR2 relacionados con CAN (ComAp, MEDIA — CONFIRMADO que ComAp los publica)

"Recommended setting of EMR2 using Serdia PC tool":
- Página 30: **4400 = 1** … CAN activation
- Página 31: **4412 = 1** … Activate TSC1a receive telegram
- Página 31: **4470 = 1** … Activate CAN set point by TSC1a
- Página 12: **4829 = 8** … Enable stop request telegram
- Página 10: **4900 = 8** … Selection of input channel type for nominal speed value sensor (fuente de consigna)
- **829 = FunctEngineStop** – asignación de interruptor para "Engine stop"
- **4424 = TelStopRequestOn** – SAE J1939: Active Engine Stop Request receive telegram
- Aviso Deutz: no parar el motor cortando la batería (genera SPN 536).

Otras referencias de configuración (Deutz 0297 9885, ALTA): "More than 1200 different parameters… Access… organized on four levels… SERDIA Level III required… changed data sets must be reported back to DEUTZ (Service Note 0199‑99‑9287)". Variantes de velocidad "programmed at the works" (fija 1500/1800 rpm para gensets "defined in the scope of customer supply (KLU)", velocidad 1/2, fija/variable, congelar, min/max). Nombres alemanes "Festdrehzahl", "Handgas", "Motorstopp" como parámetros SERDIA concretos: **NO ENCONTRADOS** textualmente (solo el manual SerDia2000 en docplayer.org, no accesible, habla de "Festdrehzahl ändern", "Pedalkalibrierung", "Leerlauf feinabstimmen").

---

## 4. Entradas cableadas del conector de vehículo (CONFIRMADO, Deutz 0297 9885 §4.3/4.4/6.1 y esquema 12.1)

### 4.1 Fuentes de consigna configurables ("Set point setting", §4.4)
- **Pedal (SWG 1 / PWG):** potenciómetro 1 kΩ lineal, +5 V ref en F25 (máx. 30 mA compartido con handgas), señal F24, GND F23.
- **Tensión externa:** 0,5–4,5 V en F24 (GND F23) "replacement for pedal value sensor".
- **Acelerador manual (SWG 2 / Handgas):** potenciómetro 1 kΩ, ref F25, señal **F20**, GND F23; la consigna resultante es el **máximo** de pedal y handgas.
- **Memoria (congelar velocidad):** solo con PWG; conmutación por F18/F19 según variante.
- **CAN:** "Setting via the CAN interface (see chapter 6.1)" — pines F12/F13.
- **Interna (velocidad fija):** "setting via internal parameters, for gensets, determined in customer supply (KLU)".
- **PWM 1 / PWM 2:** 100 Hz, 5–95 %, entrada **F18 o F20/F21**, GND F17.
- **Up/Down ("Touch control operation Up/Down (digital)", §4.1):** listado como función; en el esquema 12.1 aparecen "DIG‑UP genset" (F19) y "DIG‑DOWN genset" (F7). Su asignación a "Drehzahl‑Schnellverstellung" no se detalla más (parcial).

### 4.2 Entradas digitales de conmutación (§4.3.1, §4.5, §4.6)
- **F18 (GND F17):** interruptor a −UBatt que conmuta velocidad 1/velocidad 2, fija/variable, variable/congelar, o regulador variable/min‑max (según variante programada en fábrica; abierto = valor por defecto subrayado).
- **F19 (GND F17):** conmutación de curva de potencia 1/2 (1/2/3 solo por CAN).
- **F21 (GND F17):** conmutación P‑grado 1/2 o constante/variable.
- **F6:** genset / cambio de marcha / freno motor. **F7:** velocidad de vehículo.
- **Paro del motor:** por desconexión del borne 15 (F14) → actuador y solenoide de paro a cero por resorte; por CAN (Stop Request); SERDIA parámetro 829 asigna un interruptor a "Engine stop". No hay un pin "Motorstopp" dedicado en la tabla F (INFERIDO: se configura sobre una entrada digital libre).
- **Lámpara/botón de diagnóstico:** **F4** (lámpara a +UBatt borne 15 y botón a −UBatt en el mismo pin, §7).

### 4.3 ¿Permite EMR2 cambiar la consigna con un potenciómetro directo en el conector de vehículo?
- **Sí, CONFIRMADO** (F25/F24/F23 o F25/F20/F23), **si el dataset lo tiene activado** (parámetro 4900 "input channel type for nominal speed value sensor", y "Only one variant can be selected" en varias tablas). El documento Deutz subraya que la variante se programa "at the works" y que cambiarla exige SERDIA nivel III y notificación a Deutz.

### 4.4 ¿A qué corresponde la entrada Volvo B4 "Emergency speed control"?
- En el EC210B (manual del operador, ya en `esquemas/ce_EC210B_opman_p072_emergency_engine_speed_control_switch-072.png`) el mando de emergencia es un **conmutador** que fija el régimen cuando falla el V‑ECU/J1939. En el EMR2 el equivalente funcional más cercano es (a) la conmutación digital **F18 "fija/variable"** (fija = valor interno KLU) o (b) la **velocidad auxiliar de limp‑home** cuando se pierde la consigna CAN (§4.15). Ambas son **digitales**. Una entrada analógica tipo F24 (0,5–4,5 V) también existe en EMR2 pero no hay evidencia de que Volvo la use en B4. **Estado: INFERIDO (digital, "fija/variable" o Notlauf); no confirmado por fuente Volvo.**
- Que un dataset Volvo admita un potenciómetro en el conector B: **NO ENCONTRADO**; dado que la consigna normal llega por J1939 desde el V‑ECU y que la tabla F de EMR2 muestra que la fuente de consigna es una *variante exclusiva* programada, la probabilidad de que el dataset Volvo tenga activada la entrada analógica es baja (INFERIDO).

---

## 5. Manuales de controladores genset/OEM que describen la interfaz Deutz EMR2

| Fabricante / documento | Qué dice del EMR2 | URL | Fiab. | Local |
|---|---|---|---|---|
| **ComAp** "Electronic Engines Support 7.0.0 Global Guide r3" (2019), §3.6.2 EMR2 (10xx series), §3.26.4 "EDC4 (EMR2)" Volvo D5/D7 | Lista de SPN leídos, "Requested speed SPN 898" como salida analógica (TSC1), Stop Request/Lock status propietarios, parámetros SERDIA 4400/4412/4470/4829/4900/829/4424, cableado conector F 25 pines (CAN H 12, CAN L 13, +14, −1), límites 800–2100 rpm, DTC EMR2 | http://generator-info.com/ComAp/Control%20Panels/ECU-list-7-0-0-Global-Guide_r3.pdf | MEDIA | `deutz_emr2/ComAp_Electronic_Engines_Support_7-0-0_Global_Guide_r3_2019.pdf` (p. 76–77) |
| **ComAp** "Electronic Engines Support 08‑2015 r2" (254 p.), "Deutz – EMR2" p. 61–63, "Volvo – EDC4 (EMR2)" p. 179 ("For more information follow Deutz EMR2 chapter") | Idéntico contenido 2015; Volvo EDC4 = motores xxD5xxxx, xxD7xxxx | https://grupofeynsa.wordpress.com/wp-content/uploads/2015/10/comap-support.pdf | MEDIA | `deutz_emr2/ComAp_Electronic_Engines_Support_08-2015_r2.pdf` |
| **DEIF** "AGC 150 CAN bus engine communication 4189341302I", §3.7.1 Deutz EMR2 | Stop ●, Speed control ●, SA por defecto 3, TSC1, Idle mode ●, 50/60 Hz ●, propietario "Engine Stop Request", DM1/DM2 ●, lecturas analógicas; §2.2.4 TSC1 SA (par. 7566) | https://deif-cdn-umbraco.azureedge.net/media/vnujpqtb/agc-150-engine-communication-4189341302-uk.pdf | MEDIA | `deutz_emr2/DEIF_AGC150_CAN_bus_engine_communication_4189341302I.pdf` (p. 82) |
| **DEIF** "AGC‑4 Mk II Option H12/H13 4189341274‑J", §3.6.1 Deutz EMR2, §3.6.7 "Deutz EMR Generic (EMR2, EMR3)", §3.6.9 write commands | Igual que AGC150; write commands: Speed control (= J1939 TSC1), Idle speed, Stop request (telegrama propietario) | https://deif-cdn-umbraco.azureedge.net/media/rfyh21aa/option-h12-h13-engine-communication-agc-4-mk-ii-4189341274-uk.pdf | MEDIA | `deutz_emr2/DEIF_AGC-4_MkII_Option_H12_H13_engine_communication_4189341274J.pdf` (p. 86, 92) |
| **DEIF** "Omni Engine Interface Communication 4189341306‑K", §6.5.3 Deutz EMR 2 | Igual (SA 3, TSC1, Engine Stop Request) | (ya descargado en sesión anterior) | MEDIA | `deutz_emr2/DEIF_Omni_Engine_Interface_Communication_4189341306.pdf` (p. 65) |
| **Woodward** easYgen‑1600 Technical Manual B37699A | Lista J1939: ECU 17 "Volvo EDC4", ECU 30 "Deutz EMR2 / Volvo EDC4"; tabla de cableado "Deutz EMR2 / Volvo EDC4 – F connector": 1 = batt −, 12 = CAN(H), 13 = CAN(L), 14 vía relé 30 A/fusible 16 A | https://www.woodward.com/products/publication-asset/b37699a | MEDIA | `deutz_emr2/Woodward_easYgen-1600_Technical_Manual_B37699A.pdf` (p. 51, 84–86) |
| **Woodward** Product Spec 37553D (easYgen rental) | "Volvo EMS2 & EDC4, Deutz EMR2, MAN MFR/EDC7, SISU EEM…" soportados | https://www.woodward.com/products/wp-content/uploads/sites/3/2024/08/37553_D.pdf | MEDIA | `deutz_emr2/Woodward_easYgen_Rental_Genset_ProductSpec_37553D_ECU_list.pdf` |
| **Smartgen** HGMS61 §13.9 "DEUTZ EMR2" / HGM8140 | Bornes CAN(H)/CAN(L), "Engine type: VOLVO‑EDC4" dentro del apartado EMR2; HGM8140 lista Volvo EDC4 para TD520/TAD520/TD720/TAD720/721/722/732 | https://www.manualslib.com/manual/2201488/Smartgen-Hgms61.html?page=42 ; https://www.manualslib.com/manual/1506106/Smartgen-Hgm8140.html | MEDIA (acceso parcial) | — |
| **Volvo Penta** Operator's Manual 4–7 L (EDC 4) 7745202 | "EDC 4 … electronic system with CAN or potentiometer communication… controls the control rod for the injection pumps… by means of an actuator"; instrumentos: "A. Engine speed potentiometer, B. CAN interface SAE J1939, C. VODIA input"; diagnóstico por lámpara/botón, VODIA con "Penta EDC4 software" | https://www.wincogen.com/wp-content/uploads/PD/Engines/volvo_tad722ge_opm.pdf | ALTA (Volvo) | `deutz_emr2/VolvoPenta_4-7L_EDC4_Operators_Manual_7745202_TAD722GE.pdf` (p. 13–14) |
| **JLG** Service Manual 3121607 (600SC/660SJC), §3.10 Deutz EMR 2 | Fig. 3‑52 esquema lado vehículo (Deutz D5.2), Fig. 3‑55/3‑56 tablas de pines M y F, códigos de fallo EMR2 (5 hojas), Fig. 7‑31 esquema JLG con ECU EMR2 (resistencia 120 Ω, CAN HI/LO, enchufe de diagnóstico Deutz) | https://www.manualsdir.com/manuals/552280/jlg-600sc_660sjc-service-manual.html?page=94 | MEDIA | imágenes en `esquemas/emr2_JLG_3121607_*` |
| DSE (Deep Sea), IQAN, Murphy/Enovation | DSE: no se encontró doc. con capítulo EMR2 (solo EMS2 Volvo en 057‑xxx). IQAN: hilo sobre TSC1 "update rate error" (https://forum.iqan.se/communities/1/topics/3172-j1939-tsc1-and-update-rate-error). Enovation: artículo genérico TSC1 (bloqueado 403) | — | BAJA | NO ENCONTRADO específico EMR2 |

---

## 6. Proyectos DIY / ingeniería inversa / foros / SERDIA

- **Proyectos Arduino/ESP32/PLC específicos para EMR2: NO ENCONTRADOS** (búsquedas en GitHub, Hackaday, Reddit, elektroda, mhhauto). Lo más cercano:
  - Foro Danfoss PLUS+1 (BAJA): https://www.plus1forum.danfoss.com/index.php?topic=49.0 — Deutz con TSC1 que no respondía ("Finally the program of the Motor Controller was wrong"); regla general: byte 1 = 0x01 (solo bit de modo velocidad), dirección destino del motor = 0 y no 3; EMR3 sin DM1/DM2 → revisar "Use Source" (SA distinto).
  - Foro IQAN (BAJA): error TSC1 "abnormal update rate" si el ciclo es lento (defecto 50 ms, hasta 10 ms).
  - Bauforum24 (BAJA, alemán): https://www.bauforum24.biz/forums/topic/29667-emr-schaltplan-deutz/ — pérdida de CAN → Notlauf a plena carga; solución SERDIA nivel adecuado; pregunta abierta "¿regulación solo por CAN o también consigna por potenciómetro?".
  - Hilo Deutz/Bomag DTC en MHH (BAJA): https://mhhauto.com/Thread-Deutz-Bomag-Engine-fault-list-and-DTC-description
- **SERDIA / cables (CONFIRMADO ALTA + BAJA):**
  - Oficial Deutz: SerDia2000 (Win 2000/XP) para EMR1/EMR2/EMR3, interfaz **HS‑Light** con niveles de acceso; SerDia 4.0 también lista EMR2 (https://serdia.deutz.com/en/serdia2000/ , https://serdia.deutz.com/en/serdia40/).
  - EMR2 se programa por **ISO 9141 (K/L‑line, pines F11/F10)**; "Communication is only possible with the electric power switched on" (Deutz, ALTA). Conector de diagnóstico Deutz X22 (esquema 12.1): CAN‑H, CAN‑L, ISO‑L, ISO‑K, +UBatt (15), GND.
  - Vendedores (BAJA): kits "DeCOM"/"HS‑Light II" con SerDia 2010 (EMR2/3/4), p. ej. https://www.fridayparts.com/diagnostic-kit-for-deutz-controller-emr2-emr3-emr4 ; MHH "Deutz Serdia" (https://mhhauto.com/Thread-Deutz-Serdia?page=2 , bloqueado 403).
  - Niveles de acceso (Deutz, ALTA): 4 niveles con contraseña; reprogramación/dataset = nivel III/IIIa; >1200 parámetros.

---

## 7. Volvo ↔ EMR2: estado de la hipótesis

- **CONFIRMADO (MEDIA):** Volvo Penta "EDC4" = aplicación Volvo del Deutz EMR2 (ComAp "EDC4 (EMR2)", Woodward "Deutz EMR2 / Volvo EDC4", Smartgen). Motores: TD/TAD520, TD/TAD720/721/722 (Deutz 1012/1013 con bomba en línea + actuador), hardware 2 × 25 pines AMP.
- **NO ENCONTRADO:** cualquier documento que llame "EMR2" a la E‑ECU Volvo CE 03161983/20577135/60100002 de los D6D/D7D/D4D (EC140B–EC290B, L60E–L120E); los boletines Volvo que cita el usuario ("EMR control unit", servidor de datasets "EMR2") no están indexados públicamente.
- **NO ENCONTRADO:** un EMR2 Deutz para motores 2012/2013 con **bombas unitarias** (el conector M documentado solo prevé un actuador de cremallera).
- **INFERIDO:** la E‑ECU Volvo D6D es un hardware propio Volvo/LucasVarity (36+36 pines, con J1708 que el EMR2 no tiene) que ejecuta una aplicación de la familia EMR2 (de ahí "EMR" en los boletines y datasets "EMR2"); el comportamiento CAN esperable es el del EMR2: J1939 250 kbit/s, consigna por **TSC1** (SA del emisor configurable, 3 por defecto en integradores; el V‑ECU Volvo probablemente usa otra SA — **no confirmado**), paro por telegrama propietario, fallback a pedal/velocidad auxiliar al perder TSC1. Todo esto debe verificarse con captura CAN en la máquina.

---

## Manuales descargables

| Título | URL | Contenido | Gratis/pago | Ruta local |
|---|---|---|---|---|
| Deutz 0297 9885 "System Description EMR 2" (EN, ed. 06/02, pp. 65–118) | https://idoc.tips/deutz-emr2-electronic-engine-governor-pdf-free.html | Descripción completa EMR2, tablas de pines M/F 25 polos, consignas, limp‑home, SERDIA, esquemas 12.1–12.4 | Gratis (copia de tercero; original Deutz no público) | `/home/user/docs/manuales/deutz_emr2/Deutz_EMR2_System_Description_0297_9885_EN_06-2002_60p_idoc-tips.pdf` (60 p., verificado PDF) |
| Ídem, traducción automática al francés pp. 59–118 | https://forums.futura-sciences.com/attachments/electronique/427604d1607857752-mli-manuel-emr2-de-059-118-..fr.pdf | Mismo contenido; tablas 4.4 y 6.1 completas (sin recorte) | Gratis | `/home/user/docs/manuales/deutz_emr2/Deutz_EMR2_Systembeschreibung_traduction_FR_p59-118_futura-sciences.pdf` (60 p.) |
| Deutz "CAN‑Specification EMR2" (2004) | https://www.scribd.com/document/638279672/CAN-Specification-EMR2-engl ; https://pdfcoffee.com/can-doku-emr2-engl-pdf-free.html | Baudrate 250/100 k, mensajes J1939 + propietarios EMR2, TSC1 | Gratis (Scribd/PDFCoffee, requieren navegador/cuenta) | **No descargado** (bloqueo anti‑bot) |
| Deutz "Installation Manual – Electronic governors (EMR2/3/4)" | https://manualzz.com/doc/37731658/installation-manual-electronic | Instalación, longitudes de cable | Gratis (manualzz) | **No descargado** (403) |
| Deutz 0297 9885 ES en tienda | https://wimanual.com/shop/deutz-emr-2-system-description-electronic-engine-governor | 118 p. | Pago | — |
| ComAp Electronic Engines Support 7.0.0 (2019) | http://generator-info.com/ComAp/Control%20Panels/ECU-list-7-0-0-Global-Guide_r3.pdf | §3.6.2 EMR2, §3.26.4 Volvo EDC4 (EMR2), DTC EMR2 §4.18 | Gratis | `/home/user/docs/manuales/deutz_emr2/ComAp_Electronic_Engines_Support_7-0-0_Global_Guide_r3_2019.pdf` (419 p.) |
| ComAp Electronic Engines Support 08‑2015 | https://grupofeynsa.wordpress.com/wp-content/uploads/2015/10/comap-support.pdf | Deutz EMR2 p. 61–63; Volvo EDC4 p. 179 | Gratis | `/home/user/docs/manuales/deutz_emr2/ComAp_Electronic_Engines_Support_08-2015_r2.pdf` (254 p.) |
| DEIF AGC 150 CAN bus engine communication 4189341302I | https://deif-cdn-umbraco.azureedge.net/media/vnujpqtb/agc-150-engine-communication-4189341302-uk.pdf | §3.7.1 Deutz EMR2; §2.2.4 TSC1 SA | Gratis | `/home/user/docs/manuales/deutz_emr2/DEIF_AGC150_CAN_bus_engine_communication_4189341302I.pdf` (221 p.) |
| DEIF AGC‑4 Mk II Option H12/H13 4189341274‑J | https://deif-cdn-umbraco.azureedge.net/media/rfyh21aa/option-h12-h13-engine-communication-agc-4-mk-ii-4189341274-uk.pdf | §3.6.1 EMR2, §3.6.7 EMR Generic, §3.6.9 write commands | Gratis | `/home/user/docs/manuales/deutz_emr2/DEIF_AGC-4_MkII_Option_H12_H13_engine_communication_4189341274J.pdf` (233 p.) |
| DEIF Omni Engine Interface Communication 4189341306‑K | (sesión anterior) | §6.5.3 Deutz EMR 2 | Gratis | `/home/user/docs/manuales/deutz_emr2/DEIF_Omni_Engine_Interface_Communication_4189341306.pdf` (161 p.) |
| Woodward easYgen‑1600 Technical Manual B37699A | https://www.woodward.com/products/publication-asset/b37699a | ECU 30 "Deutz EMR2 / Volvo EDC4", cableado conector F | Gratis | `/home/user/docs/manuales/deutz_emr2/Woodward_easYgen-1600_Technical_Manual_B37699A.pdf` (113 p.) |
| Woodward Product Spec 37553D | https://www.woodward.com/products/wp-content/uploads/sites/3/2024/08/37553_D.pdf | Lista ECUs soportadas (Deutz EMR2, Volvo EDC4) | Gratis | `/home/user/docs/manuales/deutz_emr2/Woodward_easYgen_Rental_Genset_ProductSpec_37553D_ECU_list.pdf` (4 p.) |
| Volvo Penta Operator's Manual 4–7 L EDC 4 (7745202) | https://www.wincogen.com/wp-content/uploads/PD/Engines/volvo_tad722ge_opm.pdf | Descripción EDC4 (= EMR2 Volvo), potenciómetro/CAN J1939/VODIA, códigos de fallo | Gratis | `/home/user/docs/manuales/deutz_emr2/VolvoPenta_4-7L_EDC4_Operators_Manual_7745202_TAD722GE.pdf` (58 p.) |
| JLG Service Manual 3121607 (600SC/660SJC) | https://www.manualsdir.com/manuals/552280/jlg-600sc_660sjc-service-manual.html?page=88 | §3.10 Deutz EMR 2 (pp. 88–99), Fig. 7‑31 (p. 259) | Gratis (visor web; se descargaron las páginas como PNG) | ver "Esquemas extraídos" |
| Volvo Penta Workshop Manual Group 23 "EDC 4" (TAD520/720) | https://pdfcoffee.com/workshop-manual-group-23-edc-4-pdf-free.html | "2 x 25‑pin (AMP) connector", pruebas EDC4 | Gratis (PDFCoffee, bloqueado) / pago en sellfy | **No descargado** |
| Deutz EMR2 para Volvo EC140B ("Deutz Emr2‑Volvoec140b") | https://www.scribd.com/document/249826219/deutz-emr2-volvoec140b-pdf | Según índice: páginas JLG "EMR 2 Engine Plug Pin Identification / Engine Side Connection Diagram" | Gratis (Scribd, bloqueado) | **No descargado** |
| "PINAGEM VOLVO EC140B – EECU completo motor Deutz" | https://www.scribd.com/document/728054926/PINAGEM-VOLVO-EC140B-EECU-COMPLETO-MOTOR-DEUTZ | Especificación E‑ECU Volvo (fabricante, tensión, conectores, pines) — **posible confirmación del fabricante** | Gratis (Scribd, bloqueado) | **No descargado** (recomendado abrir manualmente) |

## Esquemas extraídos (todos en `/home/user/docs/esquemas/`, prefijo `emr2_`)

| Imagen | Fuente | Qué muestra |
|---|---|---|
| `emr2_Deutz_SystemDescription_0297-9885_ch9-3-2_vehicle_plug_F_25pin-47.png` | Deutz 0297 9885 §9.3.2 (idoc.tips) | Tabla conector de vehículo F, 25 pines, con dibujo del conector |
| `emr2_Deutz_SystemDescription_0297-9885_ch9-3-1_engine_plug_M_25pin-46.png` | Deutz 0297 9885 §9.3.1 | Tabla conector de motor M, 25 pines |
| `emr2_Deutz_SystemDescription_0297-9885_ch6-1_function_overview_pin_assignment-29/-30/-31.png` | Deutz §6.1/§7 | Tabla funciones↔pines (ejemplo genset 1012/1013) [p.29 recortada; p.30–31 lámpara/botón diagnóstico F4] |
| `emr2_Deutz_SystemDescription_0297-9885_ch5_interfaces_CAN_J1939-26.png` | Deutz §5 | Interfaces: ISO 9141 (SERDIA) y CAN SAE J1939 |
| `emr2_Deutz_SystemDescription_0297-9885_ch4-3_speed_setpoint_sources_fixed_speed-16..-19.png` | Deutz §4.2–4.4 | Extensiones, variantes de regulación (fija 1500/1800, velocidad 1/2…), interruptor F18/F17, tabla de consignas (pot F25/F24/F23, 0,5–4,5 V, handgas F20) |
| `emr2_Deutz_SystemDescription_0297-9885_ch12_connection_diagrams-56..-60.png` | Deutz §12 | 56: índice; 57: 12.1 lado vehículo (D5.2, pedal, handgas, interruptores, lámparas, CAN 12/13, X22 diagnóstico, resistencia terminal externa); 58–59: 12.2–12.3 lado motor; 60: 12.3 hoja 2 (sensores, solenoide, bujías) |
| `emr2_JLG_3121607_600SC_660SJC_Deutz_EMR2_p94.png` | JLG 3121607 Fig. 3‑56 (manualsdir) | Tabla de pines conector de vehículo F (reproducción nítida de la tabla Deutz) |
| `emr2_JLG_3121607_600SC_660SJC_Deutz_EMR2_p93.png` | JLG Fig. 3‑55 | Tabla de pines conector de motor M |
| `emr2_JLG_3121607_600SC_660SJC_Deutz_EMR2_p90.png` | JLG Fig. 3‑52 | Esquema Deutz D5.2 lado vehículo (pedal, handgas, CAN, diagnóstico X22, fusible 15 A) |
| `emr2_JLG_3121607_600SC_660SJC_Deutz_EMR2_p88.png` | JLG §3.10 | Texto introductorio EMR2 (sensores, actuador, limp home, ISO9141) |
| `emr2_JLG_3121607_600SC_660SJC_Deutz_EMR2_p259.png` | JLG Fig. 7‑31 | Esquema de la máquina JLG: módulo "Deutz EMR2 engine control" con pines M (sensores, actuador), CAN HI/LO/shield con resistencia 120 Ω, enchufe de diagnóstico Deutz |
| `emr2_ComAp_ECUlist_7-0-0_Deutz_EMR2_SerDia_params_25pin_wiring-076/-077.png` | ComAp 7.0.0 §3.6.2 | SPNs, parámetros SERDIA 4400/4412/4470/4829/4900/829/4424, cableado conector F 25 pines |
| `emr2_ComAp2015_p61..p63_*.png` | ComAp 2015 (sesión anterior) | Ídem versión 2015 |
| `emr2_DEIF_AGC150_Deutz_EMR2_TSC1_SA3-082.png` | DEIF AGC150 §3.7.1 | Ficha EMR2: TSC1, SA 3, Engine Stop Request propietario, DM1/DM2 |
| `emr2_DEIF_AGC4mkII_Deutz_EMR2-086.png`, `emr2_DEIF_AGC4mkII_Deutz_EMR_Generic_write_commands-092.png` | DEIF AGC‑4 MkII | Ficha EMR2 y "EMR Generic (EMR2, EMR3)", write commands |
| `emr2_DEIF_Omni_4189341306_p65_Deutz_EMR2_interface_TSC1_SA3.png` (+ p142/143/146 Volvo) | DEIF Omni (sesión anterior) | Ficha EMR2; interfaz Volvo EDC4/EMS |
| `emr2_Woodward_easYgen1600_p51_J1939_device_list_Volvo_EDC4_DeutzEMR2.png`, `..._p84_Deutz_EMR2_VolvoEDC4_Fconnector_pins_1_12_13_14.png`, `..._p85/_p86_*.png` | Woodward B37699A (sesión anterior) | Lista de ECUs (30 = Deutz EMR2 / Volvo EDC4), cableado conector F |
| `emr2_VolvoPenta_EDC4_operators_manual_p11_system-13.png`, `..._p12_instruments_pot_CAN-14.png` | Volvo Penta 7745202 | Descripción EDC4 (actuador de cremallera, sensores) y opciones: potenciómetro, CAN J1939, VODIA |

---

## Fuentes consultadas sin resultado útil / bloqueadas
Scribd (todas las URL, "Client Challenge"), PDFCoffee (403), ManualsLib (403), manualzz (403), docplayer.org (DNS), slideshare (bloqueado), elektroda topic4158221 (503), Enovation Controls KB (403), discount-equipment.com/library_files/10013.pdf (devuelve HTML). Búsquedas sin hallazgos: "EMR2 36‑pin/36‑polig", "EMR2 Lucas/TRW/Delphi", "EMR2 Arduino/ESP32/GitHub", "Volvo CE EMR2 dataset bulletin", DSE 057‑004 Deutz EMR2, IQAN Deutz EMR2, Hatz/Bomag/Hamm EMR2 pinout.
