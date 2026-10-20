# Volvo EC210B: arquitectura electrónica, V-ECU, E-ECU (D6D EAE2) y modo de emergencia

Investigación para sustituir o emular la V-ECU de una excavadora Volvo EC210B que dialoga con la E-ECU etiquetada "VOLVO VCE56003584 D6D EAE2 - S/N E00747373".
Fecha: 2026-10-19.

> **Corrección posterior (2026-10-20):** las asignaciones de JB13/JB14/JB5 de este informe están superadas. Según el circuito OEM "Control Circuit (EC160B~EC460B)", el J1939 de la V-ECU es **JB14 (H) / JB6 (L)**, derivación del mismo par que une la E-ECU (B1/B2) con el panel; **JB13 y JB5 son las mallas** de los cables J1587 y J1939. Sin V-ECU el bus no se parte y no hay que puentear nada. Ver `docs/INVESTIGACION_V-ECU_EC210B.md` §3.

**Escala de fiabilidad**
- **ALTA**: documento OEM de Volvo (manual del operador o material de formación de servicio de Volvo CE Korea) o norma.
- **MEDIA**: documento OEM reconstruido por mí (texto extraído de un PDF subido a Scribd con fuente cifrada o con texto desordenado, que tuve que descifrar o reordenar), o un fabricante de componentes.
- **BAJA**: vendedor de recambios o foro.

> **Nota metodológica.** Los dos documentos clave son extractos del material de formación de servicio de Volvo CE Korea para la EC210B/EC160B:
> - **"EC210B-04 Electronic Control System"**, 23 láminas: https://www.scribd.com/document/461665933/EC210B-04
> - **"EC210/160B-ENG7 Engine control system"**, 21 láminas: https://www.scribd.com/document/428476774/Pages-from-EC210B-ENG-7-pdf
>
> Scribd bloquea la descarga directa. Obtuve la capa de texto de cada página (jsonp en html.scribdassets.com, a través del proxy de translate.goog).
> - El documento EC210B-04 usa una fuente con sustitución de caracteres. Lo descifré con un mapa construido a partir de títulos conocidos, y el resultado es coherente: "Electronic Control System Overview", "Resistor Box", etc.
> - Los diagramas pierden la geometría, así que las asignaciones pin↔señal que doy aquí se deducen del orden del texto y de sus coordenadas.
>
> Por eso marco como MEDIA lo que procede de esa reconstrucción, aunque la fuente sea OEM.

---

## 0. Resumen ejecutivo (lo más útil para el objetivo inmediato)

1. **El "modo de emergencia" (Auto/Manual en MANUAL) no pasa por la V-ECU** [MEDIA-ALTA; EC210B-04-07, EC210B-04-21, EC330B Service Training p.69].
   - **Régimen del motor.**
     - Lo fija la propia E-ECU a partir de una entrada cableada, *"Emergency speed control"*, procedente del interruptor de emergencia de 3 posiciones.
     - La alimenta el fusible **F24 de 5 A, "Engine RPM manual control"**.
     - Posiciones:
       - **Neutral**: 800 rpm, "emergency low speed".
       - **Arriba**: 1900 rpm, "emergency high speed".
       - **Abajo durante 2 s**: para el motor.
     - Volvo indica que *"Emergency low-high speed can be adjusted by VCADS Pro"*, es decir, son dos parámetros de la E-ECU.
     - En consecuencia, por esa entrada **solo hay dos consignas discretas, no un ajuste continuo**.
   - **Bomba.**
     - La válvula proporcional de la bomba (*power shift valve*) se alimenta a través de la **"Resistor Box"**: resistencia nominal de **60 Ω a 25 °C**, corriente a la válvula de **340 mA**.
     - Según Volvo, *"Machine can use 85% of the maximum pump input torque"*.
     - La corriente es fija, sin el control ESSPC de carga.
2. **Lógica del power shift: a más corriente, menos potencia de bomba.** La corriente sube la presión secundaria que llega al regulador de la bomba Kawasaki K3V112DT y reduce el par absorbido [ALTA; manual del operador; EC210B-04-05; EC210B-10-13].

   | Modo | Corriente (mA) |
   |---|---|
   | P (Power max) | 215 |
   | H | 250 |
   | G1-G3 | 290 |
   | F | 450 |
   | I (ralentí) | 555 |

   - Las cifras son de mercado no-USA.
   - En USA, el manual del operador da: H 220, G1 260, G2/G3 300, F 450, I 570 mA.
   - En P, H y G la corriente es "var.": la V-ECU la sube cuando la carga hace caer el régimen (ESSPC).
3. **Cómo regular sin V-ECU:**
   - **Potencia de bomba.** Sustituir la caja de resistencias por un **regulador de corriente** de unos 200 a 600 mA. Con 340 mA fijos la máquina va al 85 % del par máximo. Para tener *menos* potencia hay que **subir** la corriente hacia 450 a 555 mA.
   - **Régimen continuo.** No es posible por la entrada de emergencia, que solo da dos niveles. Haría falta enviar por **J1939** la petición de régimen que normalmente envía la V-ECU. Volvo describe ese mensaje como "Engine speed (Request value)". El PGN y la dirección exactos **no se han podido confirmar** (ver §5).
4. **Bus de datos** [MEDIA; EC210B-04-01]:

   | Unidad | MID | SA J1939 |
   |---|---|---|
   | EMS (E-ECU) | 128 | 0 |
   | MDU / D-ECU (pantalla) | 140 | 23 |
   | V-ECU | 187 | 17 |
   | Herramientas (VCADS Pro / MATRIS) | 172 | - |

   - Dos buses: **J1939 (CAN)** para el "control/fast link" y **J1587/J1708** para información y diagnóstico, que además hace de respaldo.

---

## 1. Arquitectura eléctrica de la EC210B

### 1.1 Unidades de control

| Unidad | Función | MID / SA | Fuente | Fiab. |
|---|---|---|---|---|
| **E-ECU / EMS** (Engine Management System) | Gestiona el motor D6D EAE2: inyección por bomba unitaria con electroválvula, precalentamiento, sensores del motor y entrada de régimen de emergencia | MID 128, SA 0 | EC210B-04-01; manual del operador ("electronically controlled fuel injection by EMS ... Volvo engine D6DEAE2") | ALTA / MEDIA |
| **V-ECU** (Vehicle ECU) | Modos de trabajo, control de bomba (ESSPC), auto-ralentí, power boost, velocidad de traslación, arranque y parada seguros, registro de datos, autodiagnóstico, control de emergencia ("limp home"), caudal X1 opcional | MID 187, SA 17 | EC210B-04-01/02; EC330B Service Training p.64 | ALTA / MEDIA |
| **I-ECU / MDU / D-ECU** (panel de instrumentos con display) | Testigo central, 2 indicadores analógicos, 21 testigos, MCD (Message Center Display), 4 pulsadores | MID 140, SA 23 | Manual del operador p.8 y p.46-53; EC210B-04-01 | ALTA / MEDIA |
| **SDU (Service Contronic) / VCADS Pro / MATRIS** | Herramientas de servicio conectadas a la toma de servicio | MID 172 | EC210B-04-01 y -23 | MEDIA |
| **Climatizador (A/C)** | Control propio con modos auto, manual y fallo | n/d | Manual del operador p.~100 | ALTA (existencia) |

- El manual del operador resume así el sistema eléctrico: *"engine starting system, charging system, machine monitoring system, engine/pump control system and air conditioning system... Engine condition can be checked via the V-ECU by the data connection between EMS and V-ECU."*
  Fuente: [Operator's Manual EC210B, ser. 14132-](https://www.tractorparts.com/PDFs/VOLVO_EC210B_OPERATIONS_MANUAL.PDF), p.8. ALTA.
- **Tensión del sistema**: 24 V.
  - Dos baterías de 12 V y 150 Ah; alternador de 28 V y 80 A; motor de arranque de 24 V y 4,8 kW.
  - Fuentes: ficha técnica EC210B https://www.scribd.com/document/326541302/EC210B (MEDIA-ALTA); manual del operador p.214 (ALTA).

### 1.2 Red

- **J1939 (CAN, "Fast link")**: control. **J1587/J1708 ("Slow link")**: información y diagnóstico.
  - EC330B Service Training p.20: *"One is used for the control signals of system and is designated SAE J1939... The other databus, SAE J1708, is used for information and diagnostics. The link also functions as a back up..."* ([manualslib](https://www.manualslib.com/manual/1639294/Volvo-Ec330b.html?page=20), ALTA; misma generación B).
- **Pines de bus en el esquema "Control Circuit" de la EC210B (EC210B-04-03)** [MEDIA, deducidos del orden del texto]:

  | Unidad | Pines |
  |---|---|
  | EMS, conector B | **B1 = J1939 H**, **B2 = J1939 L**, **B25 = J1708 A**, **B26 = J1708 B**. Confirmado también por coordenadas en la lámina ENG7-06. |
  | MDU, conector "21C" | dos pares CAN: 21C1 (H) / 21C7 (L) y 21C12 (H) / 21C6 (L). Probable entrada y salida del bus en cadena. |
  | V-ECU, conector JB | aparecen juntos "JB13 (H)", "JB14 (L)", "JB6 (A)", "JB12 (B)". Probablemente JB13/JB14 = J1939 H/L y JB6/JB12 = J1587 A/B. **Por confirmar con polímetro.** |
  | Toma de servicio, conector "23C" | 23C8 (A) / 23C9 (B) = J1587. |

- **Resistencias de terminación (120 Ω)**: **no se encontró** en ninguna fuente fiable dónde están (dentro de la ECU o en el mazo) en la EC210B. Comprobación recomendada: con todo apagado, medir CAN H-L en el bus. Unos 60 Ω significa dos terminaciones; unos 120 Ω, que falta una (por ejemplo, si estaba dentro de la V-ECU retirada). La regla de 60 Ω es estándar J1939 ([Simma](https://simmasoftware.com/understanding-the-j1939-terminating-resistor-a-complete-guide/), MEDIA).
- **Códigos de fallo de comunicación** (manual del operador p.53, ALTA). Los SID siguen J1587: 231 = enlace J1939, 250 = enlace J1708, 254 = el propio controlador.
  - `187 SID 231 12`: fallo de la V-ECU en el enlace J1939.
  - `187 SID 250 12`: fallo de la V-ECU en el enlace J1708.
  - `187 SID 254 12` y `128 SID 254 12`: fallo interno del controlador.
  - `187 no signal`: la pantalla no recibe nada de la V-ECU.
- **Diagnóstico Contronic** (ENG7-19, MEDIA): el código 11 corresponde a la V-ECU, el 12 a la E-ECU y el 13 a *"data bus CAN/SAE J1939 for E-ECU"*.

### 1.3 Qué intercambian V-ECU y E-ECU

Lámina ENG7-08 "ECU communication" [MEDIA]:
- **De la V-ECU a la E-ECU**: (1) señal de arranque ("Key START signal"); (2) **régimen solicitado ("Engine speed (Request value)")**.
- **De la E-ECU a la V-ECU**: (1) régimen real; (2) señal de error.
- **Entradas de la V-ECU**: interruptor de régimen ("Engine speed control switch"), terminal R2 de la llave, panel de instrumentos y MDU.
- Confirmación en EC330B p.66 (ALTA): *"The V-ECU always receives the current engine speed from the E-ECU. It balances engine horsepower and pump consuming power by changing output current to power-shift valve."*

### 1.4 Fusibles y relés relacionados

**Caja de distribución eléctrica, a la derecha del asiento** (manual del operador p.181, ALTA). El OCR del manual confunde "1" y "b", así que los valores dudosos están marcados.

| Fusible | Amperaje | Circuito |
|---|---|---|
| F1 | 10 A | IECU (instrumentos) |
| F12 | 15 A | Electroválvula de seguridad |
| F13 | 10 A | V-ECU |
| F14 | 5 A | "Overload" |
| F15 | 20 A | E-ECU |
| F24 | 5 A | **Engine RPM manual control** (interruptor de emergencia) |
| F25 | 10 A (OCR "bOA") | V-ECU |
| F27 | 20 A | Hammer / Booster / Shear |

- **Fusibles lentos**: 2 × 40 A, 140 A y 2 × 80 A, junto al desconectador de batería (p.177, ALTA).
- **Relés de la caja** (documento "Relay box, specification", [Scribd 364107615](https://www.scribd.com/document/364107615/Connector-Ec210b), MEDIA; es una traducción automática del manual de servicio):
  - R1 velocidad de traslación (NC); R2 selección de velocidad de traslación (NA).
  - **R3 "Power supply EMS" (NA)**; **R4 "EMS Data Record" (NA)**.
  - R5/R6 enganche rápido; R7 calefactor y A/C; R8 luz adicional; R9 claxon; R10 luces; R11 limpiaparabrisas; R12 seguridad.
- **En el esquema "Control Circuit"** aparecen "F14 5A, F24 5A, F15 20A, Key ACC, EMS POWER (R3), EMS DATA RECORD (R4)" junto a los pines **B4, B9, B10, B11, B12** del EMS [MEDIA].
- **Conectores de la caja** (Scribd 364107615, MEDIA):
  - **MA23 y MA24: "Connected to V-ECU"**.
  - MC02: mazo del EMS.
  - MA48: electroválvula de power boost.
  - MA49: motor de traslación.
  - ME01-ME03: mazo del motor.
  - MA52: válvula proporcional de caudal (opción).
- **Caja eléctrica** (EC330B p.57, ALTA para la generación B): *"1. Resistance box for emergency pump control"*. En la misma caja hay fusibles lentos, relé de precalentamiento, relé de arranque seguro, relé de batería y relés R1 a R12.

---

## 2. V-ECU

### 2.1 Referencias

| Referencia | Qué dicen las fuentes | Fiab. |
|---|---|---|
| **14518349** | "VECU Controller" para EC140B, EC160B, EC210B, EC240B, EC290B, EC330B, EC360B, EC460B y EC700B. Equivalencias: 14514090, 14531360, 14594697. | BAJA ([eBay](https://www.ebay.com/itm/157088641238), [FridayParts](https://www.fridayparts.com/for-volvo-excavator-ec240b-ec290b-ec330b-ec360b-ec460b-ec700b-ec700bhr-controller-voe14518349)) |
| **14594697** | "24V Cab Controller Panel V-ECU" para EC210B y otros. | BAJA ([FridayParts](https://www.fridayparts.com/for-volvo-excavator-ec700b-ec700bhr-ec290b-ec210b-ec240b-ec140b-ec200b-24v-cab-controller-panel-v-ecu-voe14594697)) |
| **14531360** | "Cab Controller Panel V-ECU" para EC240B-EC360B y EC210B. | BAJA (eBay) |
| **14390065** | **No parece una V-ECU.** FridayParts la vende como *"Monitor Plug Connector of ECU VOE14390065 VOE14636301"*. | BAJA ([FridayParts](https://www.fridayparts.com/monitor-plug-connector-of-ecu-voe14390065-voe14636301-for-volvo-excavator-ec210-ec240-ec290-ec360-ec140)) |
| **14560227** | No encontrada. | - |

- Volvo advierte: *"When you replace the VECU, you have to check the part number... you need to run the conversion kit of VCADS Pro if failed VECU is old one"* (EC330B p.65, ALTA). Los vendedores también avisan de que el programa depende del modelo.
- **Fabricante del hardware**: **no confirmado**.

### 2.2 Ubicación

- **EC330B**: *"The vehicle control unit is mounted at right wall of cabin"* (p.64, ALTA para la generación B).
- **EC210B**: un foro la sitúa "behind the seat next to the HVAC box" ([HEF](https://www.heavyequipmentforums.com/threads/need-wiring-diagram-for-volvo-ec210-blc.57000/), BAJA).

### 2.3 Conectores

- **Dos conectores: "JA connector has 70 pins and JB has 16 pins"** (EC330B p.65, ALTA). La lámina EC210B-04-16 "VECU" también muestra "JA" y "JB", y el esquema EC210B-04-03 usa pines de JA1 a JA70 y de JB1 a JB16 (MEDIA).
- **Marca y serie del conector** (AMP, Deutsch u otro): **no confirmadas**. Se venden conectores de recambio ([eBay 384979664114](https://www.ebay.com/itm/384979664114), BAJA).
- **Alimentación**: según un foro, JB tiene "2 red and 2 black: jb7, jb8, jb15 & jb16" (BAJA). En el esquema EC210B-04-03 aparecen JB7, JB8, JB15 y JB16 cerca de "Battery relay" y "Key", lo que es coherente (MEDIA-BAJA).

### 2.4 Pinout

**No existe en las fuentes accesibles una tabla pin→señal fiable para la V-ECU.**

**Pines que aparecen en el esquema EC210B-04-03** (lista sin asignación fiable):
JA1, JA3, JA5, JA7, JA12, JA13, JA14, JA17, JA18, JA19, JA20, JA22, JA23, JA24, JA25, JA26, JA27, JA28, JA30, JA32, JA33, JA34, JA35, JA36, JA37, JA38, JA39, JA42, JA43, JA44, JA47, JA48, JA49, JA51, JA52, JA56, JA59, JA60, JA61, JA62, JA63, JA66, JA67, JA68, JA69, JA70; JB1, JB2, JB4, JB5, JB6, JB7, JB8, JB9, JB11, JB12, JB13, JB14, JB15, JB16.

**Cargas y entradas del mismo esquema:**
- Salidas: power shift valve, flow control valve, electroválvulas de power boost, velocidad de traslación y corte de conflux de pluma y brazo, B/float, rotator LH/RH, indicadores.
- Entradas: presostatos de traslación, implemento, martillo y B/float; interruptores de P/Max, auto-ralentí, boost/hammer/shear, interruptor de la palanca derecha, selector de velocidad de traslación, palanca de seguridad, Q/F y confirmación; interruptor de régimen; interruptor de caudal; señal de temperatura de aceite hidráulico.

**Asignaciones parciales probables** [MEDIA-BAJA; hay que verificarlas midiendo]:
- **JA39** = señal del **interruptor de régimen**, de 0,5 a 4,5 V. Aparece junto a "Engin RPM Ctrl SW", y un fragmento de búsqueda de otra lámina dice "JA39 (0.5~4.5)".
- **JA60**: aparece junto a "F27 20A".
- JB13/JB14 = J1939 H/L y JB6/JB12 = J1587 A/B (ver §1.2).

### 2.5 Funciones de la V-ECU

Fuente: EC210B-04-04 a -15, MEDIA; EC330B p.64-69, ALTA.
- **Régimen y modo**: el selector de 9 pasos fija a la vez rpm y modo. La V-ECU pide a la E-ECU el régimen en vacío ("Request Unload RPM").
  - **Modos F e I**: corriente fija al power shift.
  - **Modos P, H y G**: corriente fija en vacío. Con carga, la V-ECU **aumenta** la corriente ("Increased Current, Loaded RPM") para reducir el consumo de la bomba. Esto es el ESSPC.
- **Modo F**: activa el corte de conflux de pluma y brazo y el power boost, y corta la alimentación a la electroválvula de traslación rápida.
- **Auto-ralentí**: tras 5 s sin actividad pasa a modo I1. El retardo se ajusta entre 3 y 10 s con VCADS Pro.
- **Power boost**: la electroválvula sube la presión del sistema de 330 a 350 kgf/cm². Funciona con un pulsador (9 s durante la traslación) o de forma automática en modo F.
- **Arranque y parada seguros**: al arrancar pide el modo I2. Gestiona el relé de batería y guarda los datos de funcionamiento antes de quitar tensión (relé R4 "EMS data record").
- **Caudal X1** (opción), según la tabla de EC210B-04-13:

  | Paso | Caudal (lpm) | Corriente (mA) | Presión (kgf/cm²) |
  |---|---|---|---|
  | 1 | 200 | 260 | 7,8 |
  | 2 | 180 | 330 | 10,3 |
  | 3 | 160 | 370 | 13,1 |
  | 4 | 140 | 405 | 16,0 |
  | 5 | 120 | 435 | 18,8 |
  | 6 | 100 | 470 | 21,6 |
  | 7 | 80 | 505 | 24,4 |
  | 8 | 60 | 540 | 27,2 |
  | 9 | 40 | 600 | 30,0 |

- **Códigos ER de la pantalla** (EC210B-04-15): ER11 a ER14 y ER21 (V-ECU, EMS, J1939, J1587 y tensión alta de entrada de la V-ECU); **ER31 = power shift valve**; ER32 = flow control valve; ER42 a ER47 = motor (temperatura de sobrealimentación PID105, sensor de régimen SID22, presión de sobrealimentación PID102, presión de aceite, refrigerante, etc.).

---

## 3. E-ECU (EMS) del D6D EAE2

### 3.1 Identificación

- **Motor**: el manual del operador dice: *"electronically controlled fuel injection by EMS (Engine Management System), Volvo engine D6DEAE2"*.
  - Características: 6 cilindros en línea, 5,7 l, turbo con intercooler, 98 × 126 mm, relación de compresión 18,4:1.
  - **Bomba de inyección "MVS"**: sistema de bomba unitaria con electroválvula, una por cilindro. Encaja con la lámina ENG7-06, que habla de *"Solenoid valve on unit injection pump"*.
  - Potencia neta: 145 PS a 1900 rpm. Par máximo: 66 kgf·m a 1425 rpm.
  - Régimen: ralentí 800 ± 40 rpm, máximo en vacío 2000 ± 40 rpm.
  - Fuente: [Operator's Manual](https://www.tractorparts.com/PDFs/VOLVO_EC210B_OPERATIONS_MANUAL.PDF), p.8 y p.214. ALTA.
- La ficha comercial da 107 kW netos (ISO 9249) y 119 kW brutos (SAE J1995) a 1900 rpm, 647 N·m a 1425 rpm, y cumplimiento **EU Stage 2**. Allí aparece como "D6D EFE2", una variante de mercado ([Scribd 326541302](https://www.scribd.com/document/326541302/EC210B), MEDIA).
- **EAE2 frente a EAE3**: el sufijo "2" corresponde a Tier 2 / Stage II y el "3" a Tier 3 / Stage IIIA. La familia D6E (EC210C/EC220B) tiene versiones EAE2 y EAE3, ambas con EMS2. El D6D EAE2 es Tier 2 / Stage II.
  - Fuentes: resultado de búsqueda sobre el manual de la EC220B ([pdfcoffee](https://pdfcoffee.com/volvo-ec220b-manual-book-cd-pdf-pdf-free.html), MEDIA-BAJA, no leído completo); Mascus (BAJA).
- **Generación del EMS para el D6D**: los documentos Volvo de la EC210B dicen solo "EMS". La tabla de relés menciona *"EMS 1 driver"* (MEDIA-BAJA). **No se ha confirmado** si es "EMS1" o "EMS2", ni quién fabrica el hardware (Bosch EDC u otro). Un vendedor la llama "EDC engine control unit" (BAJA).
- **Referencias que circulan para la E-ECU del D6D en la EC210B** (todas BAJA y contradictorias):
  - **60100000 / 60100002**, con sufijos de programa P1 a P13: [eBay](https://www.ebay.de/itm/205594611175), [topvelsun](https://www.topvelsun.com/controller/ecu-control-unit-voe60100000-for-ec210b-ec240b-ec290b-ec240c-ec290c-ec220d-ec300d.html). Algunas listas la asocian al D6E.
  - **03161983** (remanufacturada): [FridayParts](https://www.fridayparts.com/controller-ecu-03161983-for-volvo-engine-d6d-excavator-ec210b-ec210blc-ec290blc-wheel-loader-l90e-l120e-l110f-l160e-l190f-l170f).
  - **20577131 / 20582958**: otras fuentes las asocian a EMS2 de D9A/D12D, así que son dudosas para el D6D.
  - Todos los vendedores dicen que **se programa por máquina y por motor**.
- **"VCE56003584"**: **no aparece en ninguna fuente pública.** El único caso parecido es un anuncio con "VCE56001204, D7D WAE2" junto a ECUs ([machineryline](https://machineryline.info/-/sale/control-units/backhoe-loader/Volvo/excavator-ECU-EDC-engine-control-unit-210-BLC-L120E-D6D-Con--17010415043750433400), BAJA). Eso sugiere que "VCE56xxxxxx + tipo de motor" es un patrón de etiqueta de Volvo CE para la ECU motor, probablemente un número de pieza o de conjunto o un identificador de software/dataset. **No confirmado.** "S/N E00747373" sería el número de serie de la unidad, también **sin confirmar**.
  - Con VCADS Pro o una SDU, el menú "MSW VERSION / DST1 VERSION / DST2 VERSION" muestra los números de software principal y de los datasets (ENG7-18, MEDIA). Es la forma de identificarla con certeza.

### 3.2 Conectores y pines

Lámina "Engine control system (E-ECU circuit)" EC210/160B-ENG7-06 [MEDIA]. La E-ECU tiene **dos conectores: "Connector A"** (motor: sensores e inyección) **y "Connector B"** (máquina). Los pines llegan como máximo al 36, lo que sugiere dos conectores de 36 vías, **sin confirmar**.

Asignación por coordenadas del texto del diagrama, **conector B**:

| Pin B | Señal | Confianza |
|---|---|---|
| **B1** | J1939 H (A) | MEDIA (también en EC210B-04-03) |
| **B2** | J1939 L (B) | MEDIA (ídem) |
| **B25** | J1708 A | MEDIA (ídem) |
| **B26** | J1708 B | MEDIA (ídem) |
| **B4** | **Emergency speed control** (entrada del interruptor de emergencia, vía F24) | MEDIA |
| B9, B10 | Masa (probable) | BAJA |
| B11, B12 | Alimentación (probable, vía F15 de 20 A y relé R3 "EMS power") | BAJA |
| B7, B17, B8, B3, B13 | Sensores de nivel de refrigerante, presión de admisión y temperatura de admisión (reparto exacto incierto) | BAJA |
| B31, B5 | Relé de precalentamiento / bobina de precalentamiento (incierto) | BAJA |

- **Conector A**: sensores de régimen de árbol de levas (en torno a A7/A18) y de cigüeñal (en torno a A31/A30); temperaturas de combustible, sobrealimentación y refrigerante; presiones de aceite y sobrealimentación; electroválvulas de las 6 bombas unitarias. Los números leídos son 7, 18, 31, 30, 13, 2, 25, 14, 3, 4, 5, 12, 11, 23, 22, 24, 35, 36 y 34, pero **su asignación no es fiable**.
- **Entrada de llave (contacto)**: en el esquema aparece "Key ACC" junto a B4, B9, B10, B11 y B12, sin un pin claro. **No confirmado.**
- **Entrada analógica de acelerador o régimen continuo**: **no aparece ninguna** en el diagrama. La única entrada de régimen cableada es "Emergency speed control" (B4), con dos consignas parametrizables por VCADS Pro.

---

## 4. Modo de emergencia: cómo funciona eléctricamente

Fuentes: EC210B-04-07 "Emergency Control", EC210B-04-20 "Emergency Switch / Auto Manual Switch", EC210B-04-21 "Resistor Box", ENG7-04 (MEDIA, OEM descifrado) y EC330B Service Training p.69 (ALTA).

**Texto Volvo** (EC330B p.69):
> "This function is for emergency operation when malfunction of data bus or V-ECU has occurred. If emergency switch is in neutral position, engine speed will be emergency low speed and maximum current will be supplied to power-shift valve from V-ECU. If emergency switch is up position, engine speed will be emergency high speed and power-shift valve current is set to the value that corresponds to 85% of the maximum pump input torque. When malfunction of V-ECU, Emergency switch control the engine speed and Auto-Manual switch decide power shift current with resistor box. Machine can use 85% of the maximum pump input torque. Emergency switch have emergency stop function when engine is still running after turning off the key-switch. ** Emergency low-high speed can be adjusted by VCADS Pro."
>
> Fuente: https://www.manualslib.com/manual/1639294/Volvo-Ec330b.html?page=69

**Valores EC210B** (lámina EC210B-04-07):
- **(1)** AUTO con fallo de bus y emergencia en neutral: 800 rpm; la V-ECU da **555 mA** al power shift. Para la EC160B la cifra es 580 mA.
- **(2)** **MANUAL ("Off VECU")**, emergencia en neutral: **800 rpm** y **340 mA**, a través de la Resistor Box.
- **(3)** MANUAL, emergencia arriba: **1900 rpm** y **340 mA**.
- **(4)** Emergencia abajo durante 2 s: **parada del motor**. La E-ECU para el motor aunque la llave no lo haga.

**Componentes:**
- **Resistor Box**: *"Rated resistance (at 25 °C) ≈ 60 Ω; Current value to power shift valve ≈ 340 mA"* (EC210B-04-21, MEDIA). El cálculo cuadra con una bobina de unos 17,5 Ω:
  - 28 V / (60 + 17,5) Ω ≈ 0,36 A.
  - 26 V / 77,5 Ω ≈ 0,34 A.
- **Interruptores Auto/Manual y de emergencia**: interruptores basculantes de 6 terminales, vistos desde abajo con contactos 1 a 6 (EC210B-04-20). El interruptor de emergencia tiene 3 posiciones: abajo momentánea, neutral y arriba. En el manual del operador son los n.º 25 y 26 de la p.70: *"If the V-ECU malfunction, this switch must be switched to Manual"*.
- **Alimentación**: F24 de 5 A, "Engine RPM manual control".
- **Señal eléctrica en B4**: **no documentada.** No se sabe si es nivel de tensión, contacto a masa o tensión por divisor. Prueba propuesta: con la llave en ON y el modo MANUAL, medir la tensión en B4 respecto a masa en neutral y en arriba. Después, mirar la continuidad de los 6 contactos del interruptor.

**Conclusión para el proyecto:**
- Hoy la máquina funciona en MANUAL: 1900 rpm y 340 mA fijos, es decir, el 85 % del par de bomba **sin ESSPC**. Si la carga supera el par del motor a 1900 rpm, este puede calarse o caer de régimen.
- **Palanca 1, potencia de bomba (lo más fácil y seguro)**: sustituir o puentear la Resistor Box con un **driver de corriente regulada**. 340 mA da el comportamiento actual, 450 mA el "modo F" y 555 mA el "modo I" (mínima potencia). No conviene bajar de unos 300 mA a 1900 rpm sin realimentación de régimen, para no ahogar el motor; P (215 mA) solo es seguro con ESSPC. Con un sensor de régimen (por ejemplo, leyendo EEC1 en el J1939, PGN 61444, que la E-ECU emite), el ESP32 podría implementar un ESSPC sencillo: si las rpm caen por debajo de la consigna, subir la corriente.
- **Palanca 2, régimen**: por B4 solo hay dos niveles (800 y 1900 rpm, ajustables con VCADS Pro). Para un régimen continuo hay que emular la petición J1939 de la V-ECU (ver §5).

---

## 5. Cómo se ordena el régimen del motor (V-ECU → E-ECU)

- **Hecho (MEDIA-ALTA)**: en modo AUTO la V-ECU envía a la E-ECU un "Engine speed (Request value)" por el enlace de control J1939, y la E-ECU devuelve el régimen real (ENG7-08; EC330B p.66). El dial no va cableado a la E-ECU, sino a la V-ECU: es un potenciómetro de 0,5 a 4,5 V.
- **No confirmado**: si el mensaje es el **TSC1 estándar** (PGN 0, "Torque/Speed Control 1", control override en modo de régimen) o uno propietario de Volvo, y qué dirección de origen acepta la E-ECU. Según la lámina EC210B-04-01, la V-ECU usa SA 17.
  - En camiones Volvo, IQAN informa de un control por TSC1 con "override = 1" y régimen en rpm, con parámetros habilitados por Volvo ([forum.iqan.se](https://forum.iqan.se/communities/1/topics/4475-rpm-control-with-tsc1-on-volvo-truck), BAJA, otra plataforma).
  - Muchas ECU solo aceptan TSC1 desde direcciones de origen configuradas ([Enovation Controls](https://support.enovationcontrols.com/hc/en-us/articles/18705454147219-Engine-TSC1-Throttling-and-Emissions-Messaging-Troubleshooting), MEDIA).
- **Recomendación práctica**:
  - (a) Capturar el tráfico J1939 de otra EC210B que funcione (500 kbit/s no está confirmado; lo habitual en J1939 de esa época es 250 kbit/s) y buscar los mensajes con SA 0x11 (17).
  - (b) Probar TSC1 desde SA 17 con el modo AUTO y la V-ECU desconectada, vigilando EEC1 (PGN 61444). Al ser el V-ECU ausente, la E-ECU probablemente registre un fallo de comunicación.
- **Tabla de modos y regímenes** (manual del operador p.61, ALTA; EC210B-04-05, MEDIA). Mercado no-USA, velocidad en vacío / con carga ±40 rpm:

  | Paso | Modo | rpm | Corriente power shift (±10 mA) | Presión secundaria |
  |---|---|---|---|---|
  | 9 | **P** (P/Max ON) | 2000 / 1900 | 215 (var.) | 3,8 kgf/cm² (54 psi) |
  | 9 | **H** | 1900 / 1800 | 250 (var.) | 5,8 kgf/cm² (82 psi) |
  | 8 | G1 | 1800 / 1700 | 290 (var.) | 8,1 kgf/cm² (115 psi) |
  | 7 | G2 | 1700 / 1600 | 290 (var.) | 8,1 kgf/cm² |
  | 6 | G3 | 1600 / 1500 | 290 (var.) | 8,1 kgf/cm² |
  | 5 | F1 | 1500 | 450 (fija) | 19,8 kgf/cm² (282 psi) |
  | 4 | F2 | 1400 | 450 | 19,8 kgf/cm² |
  | 3 | F3 | 1300 | 450 | 19,8 kgf/cm² |
  | 2 | I1 | 1000 | 555 | 28,5 kgf/cm² (405 psi) |
  | 1 | I2 | 800 | 555 | 28,5 kgf/cm² |

  - **USA** (manual del operador): no tiene modo P. H: 2000/1900 rpm y 220 mA. G1: 260 mA. G2/G3: 300 mA. F: 450 mA. I: 570 mA.
  - En la lámina EC210B-04-05 los regímenes de G2 y G3 difieren un poco según el mercado.
- **Interruptor de régimen** (EC210B-04-18, MEDIA): 4 pines.

  | Pin | Señal |
  |---|---|
  | 1 | Alimentación ("Power (B+)"; probablemente 5 V de referencia de la V-ECU, sin confirmar) |
  | 2 | Salida de señal |
  | 3 | Masa |
  | 4 | Masa de la malla |

  - Señal: **0,5 V en el paso 1, 2,5 V en el paso 5 y 4,5 V en el paso 9**, lineal. El interruptor de caudal X1 es idéntico.

---

## 6. Válvula proporcional de bomba (power shift)

- **Bomba principal**: Kawasaki **K3V112DT**, doble, de pistones axiales y plato inclinado, con control de potencia total. Caudal máximo 2 × 200 lpm. Presión 330/350 kgf/cm² (normal/boost). Bomba piloto de engranajes de 10 cc/rev, con alivio a 40 kgf/cm².
  - Fuentes: manual del operador p.214 (ALTA); [EC210B-10 Main Pump](https://www.scribd.com/document/461665854/EC210B-10) (MEDIA, descifrado).
- **Principio**: *"The valve regulates the secondary servo hydraulic pressure to the hydraulic pump regulators to control the swash plate angle and allowable pump output. The secondary pressure varies in proportion to the current... The proportional solenoid valve spool vibrates continuously..."* (EC330B p.61, ALTA). Este último punto implica que **necesita dither**.
- **Curva de la EC210B** (EC210B-10-12/-13, MEDIA): eje de corriente de 0 a unos 800 mA y presión secundaria de 0 a 50 kgf/cm². Puntos: 215 mA → 3,8; 250 mA → 5,8; 290 mA → 8,1; 450 mA → 19,8; 555 mA → 28,5 kgf/cm². La curva P-Q de la bomba baja al aumentar la corriente (curvas a 0, 215 y 555 mA).
- **Especificación eléctrica de la bobina**: **no hay un dato Volvo publicado.**
  - La válvula típica de las K3V es la Kawasaki **KDRDE5K**. Kawasaki da para ella *"Solenoid rating 0~0.7 A for DC24V"* y presión secundaria de 2, 3 o 4 MPa ([Kawasaki](https://global.kawasaki.com/en/industrial_equipment/hydraulic/valves/kdrde5k.html), ALTA para la KDRDE5K).
  - Un catálogo de Kawasaki da **17,5 Ω (24 V) / 3,2 Ω (12 V)** para 0,7 A / 1,6 A (fragmento de búsqueda de un catálogo en pdfcoffee, MEDIA).
  - Que la EC210B monte exactamente una KDRDE5K es una **inferencia**: la presión máxima en torno a 2,8 MPa y la resistencia de 60 Ω para 340 mA son coherentes, pero **hay que medir la resistencia de la bobina**.
- **Frecuencia de PWM y dither de Volvo**: **no encontradas.** Referencias genéricas: dither de 70 a 400 Hz con amplitud del 2 al 10 % de la corriente máxima (foros y blog técnico, BAJA-MEDIA).

---

## 7. Notas prácticas: controlar el solenoide a 24 V con ESP32 o Arduino

Son recomendaciones de ingeniería con fuentes de fabricantes. Todo debe validarse en banco antes de montarlo en la máquina.

### 7.1 Etapa de potencia y lazo de corriente

- **Hay que controlar corriente, no tensión ni duty fijo.** La resistencia del cobre sube alrededor de un 0,39 %/°C, de modo que entre 20 y 100 °C la corriente cae aproximadamente un 30 % si solo se fija el duty. Volvo regula en mA (±10 mA).
- **Topología recomendada**:
  - **Lado bajo**: MOSFET de nivel lógico, de 60 V o más (por los transitorios de 24 V), con la bobina entre +24 V conmutado y el drenador.
  - **Diodo de libre circulación** (rápido o Schottky, de 100 V o más y 1 A o más) en paralelo con la bobina. Hace falta para medir la corriente media de forma continua y para el comportamiento proporcional. **No usar un TVS solo**, porque la corriente decaería rápido y el dither no funcionaría bien.
  - **Medida de corriente**: shunt de 0,1 a 0,5 Ω con amplificador (INA180/INA240 o similar), o un lado alto con medidor integrado.
  - **Lazo PI** en el ESP32 a 1 kHz o más: PWM de 1 a 5 kHz más dither superpuesto de unos 100 a 250 Hz, con amplitud de ±5 a 10 % (unos ±30 a 50 mA).
  - Alternativa: **PWM "bajo" de 100 a 250 Hz** que hace a la vez de dither. Es el método clásico, aunque la corriente media depende entonces de la frecuencia (ver los hilos de [Arduino](https://forum.arduino.cc/t/dither-for-pwm-circuit-driving-a-proportional-solenoid/472906) y [EEVblog](https://www.eevblog.com/forum/projects/pwm-circuit-to-control-hydraulic-proportional-valve/), BAJA).
- **Fail-safe**: con el driver apagado (0 mA) la bomba entrega la **máxima potencia**, porque la presión secundaria es 0. Eso es lo contrario de seguro para el motor, que podría calarse. Medidas:
  - Mantener la Resistor Box como respaldo mediante un relé NC que la conecte si falla el controlador.
  - O usar un watchdog que vuelva a unos 340 mA fijos.
- **ICs dedicados** (MEDIA, fabricantes):
  - Infineon **TLE82453-3SA**: 3 canales, regulación de corriente hasta 1,5 A con 0,73 mA de resolución, dither triangular programable, SPI y diagnóstico ([Infineon](https://www.infineon.com/cms/en/product/automotive-system-ic/constant-current-control-ic-for-transmission/tle82453-3sa/)).
  - Infineon **TLE7241E**: 2 canales, 0 a 1 A, dither de 41 Hz a 1 kHz ([Infineon](https://www.infineon.com/cms/en/product/automotive-system-ic/constant-current-control-ic-for-transmission/tle7241e/)).
  - Encajan bien con un ESP32 por SPI. Hay que revisar su tensión máxima, porque están pensados para 12 V. Para 24 V puede ser preferible un predriver con MOSFET externo (TLE8242-2).

### 7.2 Módulos comerciales listos para usar (amplificadores de válvula proporcional)

- **EWM-A-PV (Diplomatic / Continental Hydraulics)**: carril DIN, 1 solenoide, entrada **0-10 V o 4-20 mA**, salida de 500 a 2600 mA (rango configurable), PWM de 61 a 2604 Hz, rampas y dither, configuración por USB ([PDF](https://dominga.lt/uploads/komponentai-pramonei-failai/2020I/ewm-a-pv-2243-335-151117.pdf), MEDIA). **Hay que comprobar que admite un ajuste de corriente máxima de unos 600 mA.** El mínimo de 500 mA del rango puede ser el fondo de escala mínimo; consultar el PDF.
- **Danfoss EHH-AMP-702** (enchufable, entrada 0-10 V, ganancia, rampa, banda muerta y dither) y tarjetas de carril DIN Danfoss ([Danfoss](https://powersource.danfoss.com/products/hydraulic-valves/industrial-valves/proportional-valve-electronics), MEDIA).
- **Hansa-Flex HK PAM 19 DIN-RAIL**: hasta 24 V DC y 2,6 A, con rampas, linealización, frecuencia y amplitud de dither y frecuencia de PWM ajustables ([Hansa-Flex](https://shop.hansa-flex.de/en_GB/hydraulic-components/valves/electronics-amplifier-controller-cables/hk-pam-19-din-rail/p/MAS_HK_PAM_19_DIN-RAIL), MEDIA).
- Con estos módulos el ESP32 solo genera 0-10 V (o un potenciómetro directo), y el lazo de corriente y el dither los resuelve el módulo. **Es la vía más rápida y robusta.**

### 7.3 Alimentación y protección en una máquina de 24 V

- **Load dump** según ISO 16750-2: en sistemas de 24 V sin supresión centralizada (Test A), el pico Us llega a 151-202 V. Con supresión (Test B) se limita a unos **58 V** para sistemas de 28 V ([TI SNOAAA1](https://ti.com/lit/pdf/snoaaa1), ALTA para el dato normativo; [Analog Devices](https://www.analog.com/en/resources/technical-articles/loaddump-protection-for-24v-automotive-applications.html)). El alternador de esta máquina es de 28 V / 80 A.
- **Recomendaciones**:
  - Fusible propio.
  - **Protección contra inversión de polaridad**: diodo ideal o controlador de MOSFET tipo LM74930-Q1 o LM74700-Q1.
  - **TVS** en la entrada, por ejemplo de la serie SMCJ/SM8S según el pulso. Una tensión de bloqueo de unos 33-36 V es habitual en 24 V, pero hay que dimensionarla para el load dump suprimido.
  - Conversor DC-DC de entrada amplia (hasta 60-100 V) para obtener 5 V/3,3 V.
  - Conectores sellados.
- **Interfaz con el bus de la máquina**:
  - Transceptor CAN aislado o tolerante a ±58 V en el bus (p. ej. TJA1043/TCAN1043, o un módulo aislado).
  - No añadir una tercera terminación de 120 Ω.
  - Entradas de 24 V con divisor y opto o protección.

---

## 8. Esquemas y documentos de referencia

| Documento | Contenido | Acceso | Fiab. |
|---|---|---|---|
| **EC210B Operator's Manual (ser. 14132-)** | Fusibles, interruptores, modos, códigos de error, especificaciones | [PDF completo](https://www.tractorparts.com/PDFs/VOLVO_EC210B_OPERATIONS_MANUAL.PDF) | ALTA |
| **EC210B-04 Electronic Control System** (23 láminas: -01 Overview, -03 Control Circuit, -07 Emergency Control, -16 VECU, -18 interruptor de régimen, -19 power shift, -20 interruptores de emergencia, -21 Resistor Box, -23 toma de servicio) | Arquitectura, esquema de control, emergencia | [Scribd 461665933](https://www.scribd.com/document/461665933/EC210B-04) | MEDIA (OEM descifrado) |
| **EC210/160B-ENG7 Engine control system** (-04 Emergency, -05 Control circuit, -06 E-ECU circuit, -08 ECU communication, -18/-19 Contronic) | Pines de la E-ECU, comunicación | [Scribd 428476774](https://www.scribd.com/document/428476774/Pages-from-EC210B-ENG-7-pdf) | MEDIA |
| **EC210B-10 Main pump** (-12 estructura y curva del power shift, -13 tabla de presiones) | Bomba y PSV | [Scribd 461665854](https://www.scribd.com/document/461665854/EC210B-10) | MEDIA |
| **Relay box / conectores EC210B** | Relés R1 a R12, conectores MAxx | [Scribd 364107615](https://www.scribd.com/document/364107615/Connector-Ec210b) | MEDIA |
| **EC330B Service Training** (misma generación B) | V-ECU (p.64-69), JA 70 / JB 16, emergencia, E-ECU (p.10, 20, 21) | [manualslib 1639294](https://www.manualslib.com/manual/1639294/Volvo-Ec330b.html) | ALTA |
| Índice del CD de servicio "EC160B/180B/210B/240B/290B/360B/460B" | Menú de láminas de formación | [pdfcoffee](https://pdfcoffee.com/ec160b-180b-210b-240b-290b-360b-460b-click-the-volvo-logo-in-the-lower-right-corner-to-return-to-this-menu-main-menu-pdf-free.html) (bloqueado para mí, 403) | - |
| Manual de servicio completo EC210B (grupo 37, esquemas con colores de cable) | **No accesible**: solo en webs de venta (emanualonline, servicepartmanuals, etc.) o Volvo PROSIS / VCADS | - | - |

---

## 9. Lo que NO se pudo confirmar (explícitamente)

1. **Pinout completo de la V-ECU** (JA de 70 vías y JB de 16): solo hay listas de pines sin asignación fiable. Las conjeturas son JA39 = dial de régimen; JB13/JB14 = CAN; JB6/JB12 = J1587; JB7, JB8, JB15 y JB16 = alimentación y masa.
2. **Marca y serie de los conectores** de la V-ECU y de la E-ECU, y el número exacto de vías de los conectores A y B de la E-ECU (posiblemente 2 × 36).
3. **Colores de cable** y numeración de cables: no encontrados.
4. **Dónde están las resistencias de terminación** del J1939 (dentro de una ECU o en el mazo).
5. **Formato del mensaje de petición de régimen** V-ECU→E-ECU (TSC1 estándar o propietario) y la velocidad del bus J1939 de la EC210B.
6. **Tipo de señal eléctrica de la entrada "Emergency speed control" (B4)** de la E-ECU y los contactos internos del interruptor de emergencia.
7. **Resistencia real de la bobina del power shift** de la EC210B, y la frecuencia de PWM y dither que usa la V-ECU. El dato de 17,5 Ω y 0,7 A es de la Kawasaki KDRDE5K genérica.
8. **Significado de "VCE56003584"** y del S/N E00747373; generación (EMS1 o EMS2) y fabricante del hardware de la E-ECU del D6D.
9. **Si 14560227 o 14390065 son V-ECU**: 14390065 aparece como conector de monitor, y 14560227 no aparece en ninguna fuente.
10. **Si existe una entrada analógica de acelerador en la E-ECU**: no aparece en el diagrama OEM, solo la entrada de emergencia de dos consignas.
