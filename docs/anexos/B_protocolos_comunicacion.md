# Investigación: protocolos V-ECU ↔ E-ECU, Volvo EC210B (motor D6D EAE2)

Fecha: 2026-10-19. Objetivo: reemplazar o emular la V-ECU (MID 187) de una Volvo EC210B que se comunica con la E-ECU del motor "VOLVO VCE56003584 D6D EAE2".

**Leyenda de fiabilidad**
- **ALTA**: documento oficial Volvo/Volvo Penta, norma SAE, o documentación oficial del fabricante del chip.
- **MEDIA**: documento de un fabricante de controladores, o varios terceros que coinciden.
- **BAJA**: listados de vendedores, foros, blogs o páginas con errores visibles.

**Leyenda de estado**
- **[CONFIRMADO]**: lo dice textualmente la fuente citada.
- **[INFERIDO]**: deducido de fuentes de productos relacionados. Hay que verificarlo en la máquina.
- **[NO ENCONTRADO]**: no hay información pública.

> **Advertencia general.** No he encontrado ningún documento público de Volvo CE con la especificación J1939 de la E-ECU del EC210B. Los detalles de mensajes (TSC1, VP70) vienen de la *Electrical Interface Specification* de Volvo Penta para motores con EMS. Es la misma familia de sistemas Volvo (EMS/EMS2), pero es otra aplicación. Antes de usarlos en la máquina hay que validarlos capturando tráfico (sniffing).

---

## 0. Resumen para el objetivo inmediato: regular las rpm sin V-ECU

1. **La máquina tiene un modo manual de fábrica para cuando falla la V-ECU** [CONFIRMADO, ALTA]. El manual del operador del EC210B, número de serie 14132 en adelante, describe dos mandos ([PDF](https://www.tractorparts.com/PDFs/VOLVO_EC210B_OPERATIONS_MANUAL.PDF)):
   - **Interruptor 25, "Automatic / manual selector switch"**: "If the V-ECU malfunction, this switch must be switched to Manual position". Tras la reparación hay que volver a Auto y reiniciar la máquina.
   - **Interruptor 26, "Emergency engine speed control switch"**, con tres posiciones:
     - 0 = parada del motor (si se mantiene más de 3 s).
     - 1 = ralentí ("idle I2 mode", sin carga).
     - 2 = alta ("H mode (no load)"; en Norteamérica, G1).
   - El fusible **F24 (5 A) "Engine RPM manual control"** alimenta este circuito.
   - El "modo emergencia / máxima potencia" que usa ahora el usuario es casi con seguridad esta posición 2 del modo Manual.
   - [INFERIDO] Probablemente el interruptor de emergencia va cableado directamente a entradas discretas de la E-ECU. La E-ECU tendría así un selector de régimen por hardware, independiente del CAN. No he encontrado el esquema eléctrico que lo confirme.
2. **Mandar las rpm por CAN.** El método estándar en los EMS de Volvo es **TSC1 (PGN 0)** en modo de control de velocidad, enviado cada **10 ms**.
   - El EMS de Volvo Penta solo acepta TSC1 de **SA 0x03 (transmisión) y SA 0x11 (controlador OEM)** en BB1. En BB2 también acepta 0x18, 0xE6 y 0xEA [CONFIRMADO para Volvo Penta EMS, ALTA; [INFERIDO] para la E-ECU del EC210B].
   - Identificadores de 29 bits: **0x0C000003** o **0x0C000011** (prioridad 3, PGN 0, destino 0x00, SA 0x03/0x11).
   - No sé qué SA usa la V-ECU del EC210B **[NO ENCONTRADO]**. Ver §3.
3. **Volvo tiene un mensaje propietario de velocidad y estado: VP70 "VP Status".**
   - ID 0x0CFF4611, PGN 65350 (0xFF46), recibido cada 20 ms.
   - Lleva "Accelerator pedal position" de 0 a 100 % (0 = ralentí, 100 = máximo), además de petición de arranque, parada, ralentí y precalentamiento.
   - Volvo Penta: "If no valid VP70 messages are received, engine speed will be set to idle speed". TSC1 tiene prioridad sobre VP70.
   - [CONFIRMADO para Volvo Penta EMS, ALTA; [INFERIDO]/desconocido si el EMS del EC210B usa VP70. Volvo CE tenía una V-ECU propia y es probable que usara otros mensajes propietarios.]
4. **Autenticación o inmovilizador: no he encontrado ninguna prueba** de que la E-ECU del EC210B exija autenticación a la V-ECU [NO ENCONTRADO]. El documento de Volvo Penta sobre la interfaz OEM no menciona handshake: basta enviar TSC1 desde una SA permitida.
5. **Regular la potencia hidráulica es otra vía, quizá más simple.**
   - La potencia de la bomba la fija la V-ECU con la **corriente de la válvula proporcional "power shift"** (V-ECU PPID 1190, código ER31).
   - El manual da la corriente por modo, ±10 mA: P 215 mA, H 250 mA, G1 290 mA … F1 450 mA, I1 570 mA (tabla fuera de Norteamérica). En la tabla norteamericana la H es de 220 mA.
   - Por tanto, un driver PWM con lazo de corriente (ESP32 + MOSFET + shunt) sobre esa válvula regularía la potencia de la bomba sin tocar el CAN del motor.
   - [CONFIRMADO: valores de corriente, ALTA; [INFERIDO]: estrategia de implementación.]

---

## 1. Buses entre V-ECU y E-ECU

| Hecho | Estado | Fiabilidad | Fuente |
|---|---|---|---|
| E-ECU y V-ECU se enlazan por **SAE J1939 (CAN)** como "control link" y por **SAE J1708/J1587** como "information link" | CONFIRMADO (títulos de capítulos del manual de servicio: "SAE J1939_CAN control link, description and measuring", "SAE J1708_1587 information link, description and measuring", "V-ECU SAE J1939/CAN control link") | MEDIA-ALTA (índice de un manual de servicio Volvo de la serie EC210; el listado mezcla B y C) | https://aplusmanual.com/433/volvo-ec210-series-excavators-service-repair-manual |
| El manual de servicio EC160B-EC290B muestra un diagrama con J1939 (CAN) como enlace de control y J1587 (J1708) como enlace de información hacia la VECU | CONFIRMADO (según el extracto del buscador; la página devuelve 403) | MEDIA | https://manualmachine.com/volvo/ec160b/4535011-service-manual/ |
| El operador puede leer el estado del motor desde la V-ECU "by the data connection between EMS (Engine Management System) and V-ECU". Motor: "Volvo engine D6DEAE2", inyección electrónica controlada por "EMS" | CONFIRMADO | ALTA (manual del operador EC210B) | https://www.tractorparts.com/PDFs/VOLVO_EC210B_OPERATIONS_MANUAL.PDF |
| J1939 en Volvo: **250 kbit/s**, identificadores de 29 bits | CONFIRMADO en camiones Volvo / Volvo Penta; [INFERIDO] en EC210B | ALTA (documentos Volvo de camión y Penta) | https://www.volvotrucks.us/media/vtna/files/shared/body-builder/manuals/section-3-volvo-vehicle-accessory-connector-rp1226-final.pdf ; https://www.marinpro.com/Cms_Data/Contents/powerhouse/Folders/Accessories/AccessoryFiles/~contents/4YD2DR3WYE3MEBNA/OpenCAN_InstallGuideline_rev_1.pdf |
| J1587/J1708: 9600 baud, RS-485 diferencial | Norma SAE J1708 (conocimiento general, no verificado en una fuente de esta búsqueda) | ALTA (norma) | SAE J1708 |
| **Terminación**: 120 Ω en cada extremo. "The EMS has built-in terminations" (Volvo Penta EMS) | CONFIRMADO en Volvo Penta EMS; [INFERIDO] en EC210B | ALTA | OpenCAN_InstallGuideline (marinpro, enlace arriba) |
| Camiones Volvo: resistencia del bus entre 50 y 70 Ω; cada terminador entre 110 y 130 Ω | CONFIRMADO en camiones | ALTA | https://www.volvotrucks.us/media/vtna/files/shared/body-builder/manuals/2025/section-3-electrical-electronic-control-unit.pdf |
| Topología y terminación exactas del EC210B (qué nodos llevan 120 Ω: E-ECU, V-ECU o resistencia en el mazo) | NO ENCONTRADO | – | Hay que medir: con la máquina apagada, unos 60 Ω entre CAN-H y CAN-L significa que el bus está bien terminado. Si se mide unos 120 Ω al quitar la V-ECU, la V-ECU tenía uno de los terminadores y el emulador debe incluir 120 Ω |

**Nodos del EC210B** según el índice del manual de servicio: E-ECU (MID 128), V-ECU (MID 187), I-ECU (cuadro de instrumentos, MID 140), W-ECU (MID 142, telemática) y ECC (climatización, MID no encontrado).

---

## 2. MIDs (J1587) y direcciones de origen J1939

| Unidad | MID J1587 | SA J1939 | Estado / fuente |
|---|---|---|---|
| E-ECU (motor) | **128** | **0x00** (en Volvo Penta EMS: "EMS (Engine) 0 / 00h"; según DEIF y otras fuentes el EMS no hace address claim y siempre usa 0x00, aunque responde a la petición de address claim) | MID: CONFIRMADO (índice del manual, "E-ECU MID 128 … replacing"). SA 0x00: CONFIRMADO en Volvo Penta EMS, ALTA; [INFERIDO] en EC210B |
| V-ECU (vehículo) | **187** | **NO ENCONTRADO** | MID: CONFIRMADO ("V-ECU MID 187 non-programmed, replacing"). Fuente: aplusmanual (enlace arriba) |
| I-ECU (instrumentos) | **140** | NO ENCONTRADO (el valor por defecto SAE para Instrument Cluster es 0x17 = 23, pero no está confirmado aquí) | MID: CONFIRMADO, aplusmanual |
| W-ECU (inalámbrica) | **142** | NO ENCONTRADO | CONFIRMADO, aplusmanual |
| TECU (transmisión) en Volvo Penta | – | 0x03 | ALTA, solo Volvo Penta |
| Controlador OEM en Volvo Penta | – | 0x11 (17) | ALTA, solo Volvo Penta |
| BBM en Volvo Penta | – | 0xE6 (230) | ALTA, solo Volvo Penta |

Notas:
- En camiones Volvo, MID 144 es la VECU. **No aplica a Volvo CE**, que usa MID 187 [CONFIRMADO por el índice del manual EC210].
- Varias fuentes de terceros listan "Volvo → SA 3" como dirección habitual de TSC1, entre ellas la tabla de Enovation Controls (MEDIA): https://support.enovationcontrols.com/hc/en-us/articles/18705454147219-Engine-TSC1-Throttling-and-Emissions-Messaging-Troubleshooting
- La SA real de la V-ECU del EC210B solo se puede saber de dos maneras:
  - Capturar el bus de una máquina con V-ECU funcionando.
  - Enviar al global (0xFF) un Request PGN 59904 pidiendo el PGN 60928 (Address Claimed) y observar la respuesta.

---

## 3. Mensajes que la E-ECU espera recibir (control)

### 3.1 TSC1, Torque/Speed Control 1, PGN 0 (0x0000)

**Datos específicos de Volvo** (Volvo Penta EMS, *Electrical Interface Specification* 47706587, 05-2015) [ALTA, aplicabilidad al EC210B INFERIDA]. Fuente: https://www.marinpro.com/Cms_Data/Contents/powerhouse/Folders/Accessories/AccessoryFiles/~contents/4YD2DR3WYE3MEBNA/OpenCAN_InstallGuideline_rev_1.pdf
- Identificadores aceptados: `0xC000003, 0xC000011, 0xC0000E6 or 0xC0000EA`, es decir, prioridad 3, PDU1, DA = 0x00 y SA = 03, 11, E6 o EA.
- En BB1: "TSC1 messages can be received from the following source addresses: TECU (transmission) 3 / 03h, OEM (controller) 17 / 11h".
- "The expected Tx rate for 'Transmission rate' is 10ms." El ritmo de recepción "Rx rate defined in SPN 3349".
- Señales usadas: SPN 695 Engine override control mode, SPN 897 Override control mode priority, SPN 898 Engine requested speed/speed limit, SPN 518 Engine requested torque/torque limit, SPN 3350 Control purpose.
- "The TSC1 message can be used to request speed/torque instead of the VP70 message."
- "NOTICE! All unused signals must be set to 'Not available'. All unused bits in the messages used must be set to 1."
- Prioridad de la transmisión: "When controlling the engine speed from the gearbox (SA = 0x03) it always have the highest priority". Fuente: https://www.dieselgeneratortech.com/generator-sets/Volvo-Penta-genset-engine-electrical-interface.html (MEDIA, resumen de documentos de Volvo Penta).
- Con SA 0x03, 0x11 o 0xE6 se puede controlar continuamente la velocidad y el par. Con 0x11 también se puede limitar el par o la velocidad. "The TSC1 message has priority over the pedal position that is sent with the VP status message". Fuente: https://www.dieselgeneratortech.com/diesel-engines/More-Available-Control-Functions-of-Volvo-Engine.html (MEDIA).
- Timeout: no he encontrado el valor numérico para Volvo. [INFERIDO] En J1939-71 el motor abandona el override si deja de recibir TSC1 durante un tiempo del orden de 2 periodos o más. En la práctica, enviar sin interrupción cada 10 ms.

**Disposición de bytes de TSC1** según SAE J1939-71. Lo confirma parcialmente el protocolo CAN de Hatz, que da ID 0x0C000003, SPN 695 en byte1/bit1, "0 = disabled, 1 = speed control", SPN 898 en bytes 2-3 a 0,125 rpm/bit y ciclo de 10 ms: https://dsp.hatz.com/images/docu-files/SPNFMI-CAN/H50_CAN-Protokoll.pdf (ALTA para el formato estándar). El resto viene de J1939-71 (conocimiento de la norma, ALTA, no verificado línea a línea en esta búsqueda).

| Byte / bits | SPN | Nombre | Valores |
|---|---|---|---|
| 1, bits 1-2 | 695 | Engine Override Control Mode | 00 sin override, **01 control de velocidad**, 10 control de par, 11 límite de velocidad/par |
| 1, bits 3-4 | 696 | Engine Requested Speed Control Conditions | 00 transitorio optimizado (driveline desacoplado), … 11 si no aplica |
| 1, bits 5-6 | 897 | Override Control Mode Priority | 00 máxima … 11 mínima |
| 1, bits 7-8 | – | (reservado o no definido según versión) | 11 |
| 2-3 | 898 | Engine Requested Speed / Speed Limit | 0,125 rpm/bit, offset 0, little-endian (ejemplo: 1800 rpm = 14400 = 0x3840, byte2 = 0x40 y byte3 = 0x38) |
| 4 | 518 | Engine Requested Torque / Torque Limit | 1 %/bit, offset -125 (0xFF = no disponible) |
| 5, bits 1-3 | 3349 | TSC1 Transmission Rate | 111 = no disponible o por defecto |
| 5, bits 4-8 | 3350 | Control Purpose | 31 = "temporary powertrain control" (el TSC1 clásico) |
| 6-7 | – | (en versiones nuevas: par alta resolución, etc.) | 0xFF |
| 8, bits 1-4 / 5-8 | 4206 / 4207 | Message counter / checksum (J1939-71 desde 2010 aprox.) | Un EMS de la época del D6D (unos 2005-2008) casi seguro no lo valida [INFERIDO]. Rellenar con 0xFF |

Sobre SPN 3350, "Control purpose": un foro de IQAN explica que su canal TSC1 lo fija a 31: https://forum.iqan.se/communities/1/topics/935-adjust-spn-3350-tsc1-control-purpose (MEDIA).

**Trama de ejemplo** [INFERIDA, no probada en la máquina]: 1500 rpm desde SA 0x11:
`ID 0x0C000011  DLC 8  data: F1 E0 2E FF FF FF FF FF`
- Byte1 = 0xF1: modo 01 (velocidad), resto de bits a 1. Ajustar la prioridad (bits 5-6) si se quiere un valor distinto de "baja".
- 1500/0,125 = 12000 = 0x2EE0.
- Algunos motores exigen que la prioridad no sea "11". Probar 0xC1 (prioridad 00 = máxima) o 0xD1.

### 3.2 VP70 "VP Status", PGN 65350 (0xFF46), propietario de Volvo Penta EMS

Fuente: la misma *Electrical Interface Specification* 47706587 (marinpro, ALTA). Aplicabilidad al EC210B: **desconocida**.

| Campo | Posición | Longitud | Valores |
|---|---|---|---|
| ID | 0x0CFF4611 (prioridad 3, PGN 65350, SA 0x11) | 8 bytes | Rx 20 ms |
| Start request | 1.1 | 2 bits | 0 inactivo / 1 activo / 2 error / 3 n/d |
| Stop request | 1.3 | 2 bits | ídem ("results in instant engine stop") |
| Governor mode select | 1.5 | 2 bits | 0 modo velocidad / 1 modo par / 3 n/d |
| Idle speed select | 1.7 | 2 bits | 0 régimen normal / 1 ralentí |
| Frequency select | 2.1 | 2 bits | 1500/1800 rpm (solo grupos electrógenos) |
| Preheat request | 2.5 | 2 bits | 0 / 1 |
| Engine restored operation | 2.7 | 2 bits | override de protecciones |
| Accelerator pedal position | 3.1 | (el documento dice "2 bits", pero el rango 0x0000-0x03FF implica 16 bits en bytes 3-4) | 0x0000-0x03FF = 0-100 %, 0,097752 %/bit |
| Disable fuel | 5.1 | 2 bits | solo grupos electrógenos |

- Comportamiento: "If no valid VP70 messages are received, engine speed will be set to idle speed." Con fallo de pedal, el valor solo se acepta de nuevo tras recibir 0 %.
- Mensaje de respuesta: VP71, ID 0x0CFF4700, PGN 65351, Tx 50 ms (running indication, restored operation, "Engine power down ack").

### 3.3 Otros mensajes que la V-ECU del EC210B pudiera enviar

| Función | Estado |
|---|---|
| Petición de rpm por pasos (selector de 10 posiciones, modos P/H/G/F/I) | La V-ECU convierte el paso en una consigna de rpm. Tabla de rpm en §0 y en el manual (página 63): P 2000/1900, H 1900/1800, G1 1800/1700, G2 1700, G3 1600, F1 1500, F2 1400, F3 1300, I1 1000, I2 800 rpm (±40). Cómo se transmite la consigna (TSC1 o mensaje propietario): **NO ENCONTRADO** |
| Auto-idle (baja a ralentí tras 5 s sin operar) | La lógica está en la V-ECU [CONFIRMADO, manual del operador]. Mensaje: NO ENCONTRADO |
| Petición de parada del motor | En modo manual, la posición 0 del interruptor de emergencia mantenida más de 3 s. Por CAN: NO ENCONTRADO (en Volvo Penta es VP70 "Stop request") |
| Precalentamiento | La E-ECU controla el relé de precalentamiento (PID 45, SID 70 en MID 128) [CONFIRMADO por los códigos]. No se sabe si hace falta una petición por bus |
| Heartbeat o inmovilizador | **NO ENCONTRADO**. Ninguna fuente menciona autenticación V-ECU↔E-ECU en el EC210B |
| Qué pasa si faltan mensajes | La E-ECU registra **MID 128 SID 231 FMI 9 (ER13-09) "J1939 communication failure"** y en el EC210B se pasa a modo manual. En Volvo Penta, sin VP70 el motor va a ralentí. Las rpm por defecto de la E-ECU del EC210B en modo Auto sin V-ECU: **NO ENCONTRADO** |

---

## 4. Mensajes que emite la E-ECU (broadcast)

Datos de Volvo Penta EMS, BB1, documento 47706587 [ALTA; [INFERIDO] que el EMS del EC210B emita un conjunto parecido]. Las escalas son las de SAE J1939-71 (conocimiento de la norma, ALTA).

| ID | PGN | Nombre | Periodo | SPN principales y escala |
|---|---|---|---|---|
| 0x0CF00400 | 61444 (0xF004) | EEC1 | 20 ms | 190 Engine speed (bytes 4-5, 0,125 rpm/bit); 513 Actual torque (byte 3, 1 %, -125); 512 Driver's demand torque (byte 2); 1675 Starter mode |
| 0x0CF00300 | 61443 (0xF003) | EEC2 | 50 ms | 91 Accelerator pedal position (byte 2, 0,4 %/bit); 92 Percent load at current speed (byte 3, 1 %/bit) |
| 0x18FEDF00 | 65247 | EEC3 | 250 ms | 514 Nominal friction torque; 100 Oil pressure (en el documento de Volvo; según el estándar va en EFL/P1); 94, 109, 111 |
| 0x18FEEE00 | 65262 (0xFEEE) | ET1 | 1000 ms | 110 Coolant temp (byte 1, 1 °C/bit, -40); 175 Oil temp (bytes 3-4, 0,03125 °C/bit, -273) |
| 0x18FEE500 | 65253 | HOURS | 10000 ms (Volvo se desvía del estándar, que lo da a petición) | 247 Total hours (bytes 1-4, 0,05 h/bit) |
| 0x18FEF600 | 65270 | IC1 | 500 ms | 102 Boost (byte 2, 2 kPa/bit); 105 Intake manifold temp (byte 3, 1 °C, -40); 106, 173 |
| 0x18FEE900 | 65257 (en el documento aparece "64777", parece una errata) | LFC | 100 ms | 182 Trip fuel, 250 Total fuel (0,5 L/bit) |
| 0x18FEF200 | 65266 | LFE | 100 ms | 183 Fuel rate (0,05 L/h por bit) |
| 0x18FEE300 | 65251 | EC1 | 5000 ms o a petición | 188, 528-534, 539-544: mapa de régimen y par, ralentí, ralentí alto, par de referencia |
| 0x18FEF700 | 65271 | VEP1 | 1000 ms | 158 Keyswitch battery potential |
| 0x18FECA00 | 65226 | DM1 | 1000 ms | DTC activos (SPN/FMI, lamp status); usa TP.CM/TP.DT (0x18ECFF00 / 0x18EBFF00) si hay más de uno |
| — | 65263 | EFL/P1 | — | No aparece en la lista del documento de Volvo Penta (100 Oil pressure va en EEC3 en ese documento) |

Acepta Request PGN (59904): IDs 0x18EA0003, 0x18EA0011, 0x18EA00E6 y 0x18EA00EA.

En J1587, la E-ECU (MID 128) emite PIDs estándar: 190 rpm, 110 temperatura de refrigerante, 100 presión de aceite, 194 diagnóstico, etc. El EC210B usa J1587 sobre todo para diagnóstico e información (VCADS, I-ECU) [INFERIDO a partir de "information link"].

---

## 5. Formato de diagnóstico de Volvo y códigos relevantes

**Formato**
- J1587/J1708: **MID** (unidad de mando) + **PID** (parámetro), **PPID** (parámetro propietario de Volvo), **SID** (subsistema) o **PSID** (subsistema propietario de Volvo) + **FMI** (0-15, modo de fallo).
- Volvo CE convierte estos códigos a su notación de componente: **ER13-09**, **SW2701-03**, etc. La conversión se describe en el capítulo "SAE code, conversion to component designation, E-ECU / V-ECU / I-ECU" del manual de servicio: https://aplusmanual.com/433/volvo-ec210-series-excavators-service-repair-manual
- En J1939 los fallos van en DM1 como SPN+FMI.

**Códigos de comunicación.** Fuente principal: https://sinocmp.com/blogs/repair-technology/volvo-excavator-fault-codes-list (BAJA-MEDIA: blog de un vendedor con algunas contradicciones internas). Los códigos ER coinciden con https://www.emersoneims.com/faults/plant/volvo-ce-ec-series-e-ecu-and-v-ecu y https://www.ampleresiliencesoft.com/gcjx/251226.html.

| MID | SID/PSID | FMI | Código Volvo | Descripción |
|---|---|---|---|---|
| 128 | SID 231 | 9 | ER13-09 | Communication J1939, communication failure |
| 128 | SID 231 | 11 | ER13-11 | Communication J1939, other fault |
| 128 | SID 231 | 12 | ER13-12 | Communication J1939, faulty unit/component |
| 128 | SID 250 | 12 | ER14-12 | Communication J1587, faulty unit/component |
| 128 | SID 240 / 253 | 2 | ER12-02 | E-ECU program/memory, intermittent data |
| 128 | SID 254 | 12 | ER12-12 | E-ECU faulty |
| 128 | PID 158 | 0/1 | ER4E-00/01 | Tensión de alimentación de la E-ECU |
| 187 | SID 231 | 9 / 12 | ER13-09/12 | J1939, fallo de comunicación / componente (vista de la V-ECU) |
| 187 | SID 250 | 9 / 12 | ER14-09/12 | J1587, fallo de comunicación / componente |
| 187 | SID 240 / 253 | 2 | ER11-02 | V-ECU, datos intermitentes |
| 187 | PPID 1133 | 3/4 | SW2701-03/04 | Selector de régimen (potenciómetro), tensión alta o baja |
| 187 | PPID 1190 | 3/4/5 | ER31-03/04/05 | Válvula proporcional power shift (bomba) |
| 128 | PSID 201 | 9 | – | "Data link": la E-ECU no recibe por J1939 lo que espera de la unidad del vehículo. Fuente: Scribd "128 PSID 201" (BAJA; puede ser de camión). https://www.scribd.com/document/442981848/128-PSID-201 |
| 187 | PSID 200 | 9 / 12 | – | Data link V-ECU (FMI 9: J1939; FMI 12: J1587 según una fuente; otra fuente lo atribuye a baja tensión). BAJA: https://www.scribd.com/document/701692092/187-PSID-200 ; https://www.justanswer.com/construction-and-road-equipment/7gzhq-volvo-ec210-error-code-187-ppid-1191.html |

**Pista sobre el tipo de E-ECU.** Los códigos MID 128 del EC210B incluyen:
- SID 1-6 "injector solenoid valves" (MA2301-2306).
- SID 21 sensor de árbol de levas y SID 22 sensor de volante.
- PID 45 y SID 70 para el precalentamiento.

[INFERIDO] Es un EMS con bombas unitarias de solenoide. El D6D deriva de un Deutz BF6M2012C con bombas unitarias Bosch (fuentes BAJAS: https://www.fridayparts.com/fuel-injector-nozzle-assembly-for-engine-volvo-d6d-deutz-bf6m2012c-replaces-bosch-0445750003 ; Service Information "Deutz 200 D6D EOE2" en https://www.slideshare.net/slideshow/volvo-l60f-engine-description-service-manual-pdf/285027118). No es el EDC4 de Volvo Penta TAD72xVE, que usa varilla de cremallera con actuador.

El hardware de la E-ECU EC210B (VOE 60100002 / 20577135 / 20577131) **pertenece a la misma familia de números que las ECU EMS2 de Volvo Penta TAD650-760VE (60100000/60100001)** [INFERIDO a partir de listados de venta, BAJA]:
- https://shandongweiyang.en.made-in-china.com/product/qZUtflFxsLYA/China-Volvo-Penta-Engine-ECU-60100001-for-Tad660ve-Tad650ve-Tad750ve-Tad760ve-D7e240uebrake.html
- https://www.amazon.com/UOYETIB-20577131-VOE60100002-Controller-Excavator/dp/B0C73G79Y1

Esto apoya, sin confirmarla, la idea de que el protocolo Volvo Penta EMS/EMS2 es una referencia válida. El número "VCE56003584" del usuario no aparece en ninguna fuente pública [NO ENCONTRADO].

---

## 6. Herramientas

| Herramienta | Uso | Fuente / fiabilidad |
|---|---|---|
| **VCADS Pro** (Volvo CE, generación B) | Diagnóstico, "VCADS Pro, 17030-3 Parameter, programming", descarga de software a las ECU | Índice del manual EC210, MEDIA-ALTA: https://aplusmanual.com/433/volvo-ec210-series-excavators-service-repair-manual |
| **Tech Tool / Premium Tech Tool (PTT)** | Sucesor de VCADS; para la serie B sigue usándose VCADS en muchos casos | Foros, BAJA |
| **Matris** | Lectura de datos de uso y operación (histogramas) de la V-ECU/E-ECU | Volvo, MEDIA (conocimiento general) |
| **Vocom 88890020** | Interfaz USB a J1708/J1939 para VCADS y PTT | Conocimiento general, MEDIA |
| **VODIA** | Herramienta de Volvo Penta (EMS, EDC4) | ALTA: https://www.volvogroup.com/en/news-and-media/news/2003/may/news-20664.html |
| **python-can, can-j1939 (Python), SavvyCAN, cangaroo, Wireshark** | Captura y análisis. SavvyCAN y cangaroo abren DBC | Proyectos open source, ALTA como herramientas |
| **DBC J1939** genéricos | p. ej. https://github.com/arthithadee/J1939-DBC-Database , https://github.com/Konik-ai/j1939_dbc | Sin PGN propietarios de Volvo. **No he encontrado ningún DBC público de Volvo CE ni de Volvo Penta EMS2** |
| Ingeniería inversa de Volvo CE o Penta | **NO ENCONTRADO** ningún proyecto público que decodifique la V-ECU o E-ECU de Volvo CE | – |

---

## 7. Programación y configuración

- El índice del manual de servicio separa dos procedimientos [CONFIRMADO, MEDIA-ALTA]: **"V-ECU MID 187 non-programmed, replacing"** y **"V-ECU MID 187 pre-programmed, replacing"**. Existe lo mismo para E-ECU (MID 128) e I-ECU (MID 140). También están "Software parameters, description" y "VCADS Pro … Parameter, programming". Conclusión: una V-ECU nueva sin programar necesita descarga de software y parámetros con VCADS Pro desde la central de Volvo, ligados al número de serie de la máquina.
- Los vendedores de E-ECU y V-ECU insisten en que hace falta programarlas con el modelo de máquina y la placa del motor (BAJA). Ejemplo: https://www.ebay.com/itm/387350498892
- Una V-ECU emulada no puede "programarse" con VCADS. Las funciones de la E-ECU que dependen de parámetros de máquina, como límites o curvas, siguen en la E-ECU, que mantiene su propia programación.
- Chassis ID o emparejamiento V-ECU↔E-ECU: **NO ENCONTRADO**. No hay pruebas de que la E-ECU compruebe una identidad de la V-ECU.

---

## 8. Implementación con ESP32 o Arduino (TSC1 a 250 kbit/s)

### 8.1 Hardware

**ESP32 (TWAI)**
- El controlador CAN interno (TWAI) admite tramas extendidas de 29 bits [ALTA]: https://docs.espressif.com/projects/esp-idf/en/v4.3/esp32/api-reference/peripherals/twai.html
- Necesita transceptor externo. Espressif cita los SN65HVD23x (3,3 V) para ISO 11898-2 [ALTA].
  - Alternativas de 3,3 V: **SN65HVD230**, **TCAN1051HV-3V3**, **TJA1051T/3** (versión /3 con VIO de 3,3 V).
  - **No usar el TJA1050 a pelo con el ESP32**: es de 5 V y su RXD es de 5 V [conocimiento general, MEDIA].
- Configuración: `TWAI_TIMING_CONFIG_250KBITS()`, filtro "accept all" para sniffing y `TWAI_MODE_NORMAL` para transmitir.

**Arduino + MCP2515**
- Comprobar el cristal del módulo. Los módulos azules baratos suelen llevar **8 MHz**. Con la librería autowp/coddingtonbear hay que llamar a `setBitrate(CAN_250KBPS, MCP_8MHZ)`; si se omite el reloj, asume 16 MHz y el bitrate sale a la mitad [MEDIA]:
  - https://github.com/coddingtonbear/arduino-mcp2515
  - https://forum.opencyphal.org/t/gui-tool-for-sending-cyphal-command-to-development-board/1973?page=2
  - https://github.com/Mebus/CAN_BUS_Shield-1
- Para tramas de 29 bits con autowp: `frame.can_id = 0x0C000011 | CAN_EFF_FLAG`.

### 8.2 Pilas J1939 y librerías

| Proyecto | Plataforma | Notas | Fuente |
|---|---|---|---|
| **Open-SAE-J1939** (Daniel Mårtensson) | C portable (Arduino, STM32, PC) | Address claim, TP, DM1, MIT | https://github.com/DanielMartensson/Open-SAE-J1939 |
| **ARD1939** (Copperhill) | Arduino / ESP32 | Address claim completo, TP, request. Precompilado | https://copperhilltech.com/blog/sae-j1939-programming-with-arduino-address-claim-procedure-sae-j193981/ |
| **ESP32-Arduino-CAN** | ESP32 (TWAI) | Solo CAN 11/29 bits, sin J1939 | https://github.com/sdp8483/ESP32-Arduino-CAN |
| **arduino-mcp2515** (autowp/coddingtonbear) | MCP2515 | Solo CAN | https://github.com/coddingtonbear/arduino-mcp2515 |
| **python-can + can-j1939** | PC (para sniffing y pruebas con adaptador USB-CAN) | – | PyPI / GitHub |

No he encontrado ningún proyecto público que envíe TSC1 específicamente con ESP32 [NO ENCONTRADO]. TSC1 son 8 bytes; basta enviarlo periódicamente con un temporizador de 10 ms.

### 8.3 Address claim

- El EMS de Volvo usa SA fija 0x00 y no hace address claim.
- Si el emulador transmite como 0x11 o 0x03, en la práctica basta con no chocar con otro nodo que use esa SA.
- Lo correcto es emitir PGN 60928 (Address Claimed, ID 0x18EEFF11) con un NAME de 64 bits al arrancar y responder a peticiones de 60928.
- Si se mantiene la V-ECU original conectada (aunque esté averiada) y emite con la misma SA, habrá conflicto. Hay que desconectarla.

### 8.4 Riesgos y precauciones

- **Bus-off.** Un nodo pasa a bus-off cuando su TEC (contador de errores de transmisión) llega a 256. En TWAI hay que llamar a `twai_initiate_recovery()` y vigilar las alertas `TWAI_ALERT_BUS_OFF` y `TWAI_ALERT_BUS_RECOVERED`. Hay informes de bloqueos a 250 kbit/s que se resuelven activando las workarounds de erratas en menuconfig (MEDIA): https://esp32.com/viewtopic.php?p=102003
- **Nodo solo en el bus.** Un controlador CAN que transmite sin que nadie le dé ACK acumula errores. Copperhill lo advierte (MEDIA): https://copperhilltech.com/blog/tag/TWAI
- **Bitrate.** Un nodo mal configurado (500k frente a 250k, o el cristal mal declarado) genera error frames y puede tumbar el bus mientras el motor está en marcha. Primero conectar en modo escucha (`TWAI_MODE_LISTEN_ONLY`) y confirmar que se recibe EEC1 (0x0CF00400).
- **24 V.** El sistema de la EC210B es de 24 V. Hacen falta:
  - Un DC-DC aislado o automotriz con protección frente a load-dump (ISO 7637/ISO 16750).
  - TVS en la alimentación.
  - Transceptor tolerante a fallos de ±58 V en el bus (p. ej. TCAN1051HV, SN65HVD1050 o ISO1042 aislado) o, como mínimo, TVS en CAN-H y CAN-L (p. ej. PESD2CAN).
  - Masa común con la E-ECU, o transceptor aislado.
  - [Conocimiento general de ingeniería, MEDIA]
- **Terminación.** Si la V-ECU tenía un terminador y se retira, añadir 120 Ω en el emulador. Medir antes, como se explica en §1.
- **Seguridad funcional.**
  - Al soltar el TSC1 (parar de enviarlo), el motor vuelve a su consigna por defecto. Mantener un watchdog que deje de transmitir si el ESP32 se cuelga.
  - Limitar por software la consigna a la tabla de la máquina (800-2000 rpm).
  - Probar con la máquina estacionada y los mandos hidráulicos bloqueados.
- **Modo manual.** No se sabe si la E-ECU acepta TSC1 con el selector en "Manual". [INFERIDO] Lo más probable es que en Manual la E-ECU priorice las entradas cableadas del interruptor de emergencia. Probar en Auto con el emulador conectado.

---

## 9. Plan de verificación recomendado

1. Medir la terminación CAN (§1) e identificar los pines CAN-H/L y J1587 A/B en el conector de la V-ECU, según el esquema del manual de servicio.
2. Conectar en solo escucha a 250 kbit/s y registrar los IDs con SA 0x00 (EEC1, ET1, DM1, etc.).
3. Si es posible, capturar una máquina EC210B que funcione (con V-ECU) para conocer la SA de la V-ECU y si usa TSC1, VP70 u otros PGN propietarios (0xFFxx, 0xEFxx).
4. Enviar a 0x00 una petición del PGN 65251 (EC1): ID 0x18EA0011, datos `E3 FE 00`.
   - SPN 3344 indica si el motor admite TSC1 de ritmo variable.
   - SPN 188 da el ralentí y SPN 532 el ralentí alto.
5. Enviar TSC1 desde SA 0x11 (y luego 0x03) en modo velocidad, con consignas pequeñas cercanas al ralentí. Comprobar en EEC1 (SPN 190) que las rpm siguen la consigna.
6. Revisar el DM1 de la E-ECU para ver si aparecen SID 231 o PSID 201.

---

## 10. Lagunas que siguen abiertas

- La SA J1939 de la V-ECU del EC210B y el contenido exacto de sus mensajes a la E-ECU.
- Si la E-ECU del EC210B (D6D EAE2) acepta TSC1 desde 0x11 o 0x03 igual que el EMS de Volvo Penta.
- Las rpm por defecto de la E-ECU en modo Auto sin V-ECU, y el cableado exacto del interruptor de emergencia hasta la E-ECU (¿entradas digitales? ¿analógicas?).
- La existencia de una entrada analógica o PWM de acelerador en la E-ECU del EC210B. En Volvo Penta EMS/EDC4 existe un potenciómetro, pero en el CIU o en la variante "potentiometer". En la E-ECU del EC210B solo está confirmado el selector de emergencia de 3 posiciones.
- El significado de la referencia "VCE56003584".
