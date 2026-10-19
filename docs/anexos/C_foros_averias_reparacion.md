# Investigación en foros y fuentes: V-ECU Volvo EC210B (familia EC140B–EC460B) con E-ECU D6D EAE2

Fecha: 2026-10-19. Máquina objetivo: Volvo EC210B, E-ECU "VOLVO VCE56003584 D6D EAE2" (S/N E00747373).

## 0. Cómo leer este documento (limitaciones de la investigación)

- **Fiabilidad:** ALTA = documentación Volvo (manual de operador o de servicio); MEDIA = servicio técnico o profesional con datos concretos, o varias fuentes independientes que coinciden; BAJA = un solo usuario de foro, Q&A tipo JustAnswer, anuncio de vendedor o blog de códigos de terceros.
- **Acceso:** heavyequipmentforums.com, Scribd, JustAnswer, manualmachine.com, pdfcoffee.com, exkavator.ru, elektroda.pl, eBay y YouTube devolvieron 403/503/captcha a las descargas directas, también con curl. Para esas fuentes, el contenido y las citas salen de los fragmentos que devuelve el buscador, así que pueden estar parafraseados o recortados. Las citas son textos cortos en el idioma original. Leí directamente varias páginas de manualslib (manual de operador EC210B), páginas de muestra en PDF del manual de servicio EC210B LC, kawasaki.com, fridayparts, studiomaszyn.pl, elektronika.com.pl, largoautospb.ru y sinocmp.
- **Separación de hechos y anécdotas:** cada sección distingue **[VERIFICADO]** (documento Volvo o fabricante) de **[ANECDÓTICO]** (foro o vendedor). Las conclusiones de ingeniería que son mías, no de una fuente, van marcadas como **[INFERENCIA]**.
- No encontré el número VCE56003584 en ninguna fuente pública. Tampoco encontré ningún emulador de V-ECU publicado.

---

## 1. PRIORIDAD: funcionamiento sin V-ECU (modo manual o emergencia) y cómo regularlo

### 1.1 Cómo funciona el modo manual o emergencia según Volvo [VERIFICADO, ALTA]

Fuente: manual de operador EC210B, sección Switches (manualslib, págs. 62, 71 y 72): https://www.manualslib.com/manual/1664987/Volvo-Ec210b.html?page=62, ?page=71, ?page=72

- La lista de interruptores de cabina incluye el **25 "Automatic / manual selector switch"** y el **26 "Emergency engine speed control switch"**.
- Sobre el interruptor 25: *"If the V-ECU malfunction, this switch must be switched to Manual position."* También dice *"To turn manual mode to auto mode after changing or repairing damaged part, the machine must be restarted."* Pos. 1 = manual, pos. 2 = automático.
- El interruptor 26 tiene 3 posiciones:
  - **Pos. 0:** parada del motor. Sirve si el motor sigue en marcha con la llave en OFF, y lo para si se mantiene más de 3 s.
  - **Pos. 1:** ralentí, *"idle mode with no load"*.
  - **Pos. 2:** alta velocidad, *"H mode with no load"* (en Norteamérica, modo G1).
  - Es decir, **sin V-ECU solo hay dos regímenes de motor (bajo y alto)**, sin pasos intermedios.
- Fusibles (pág. 183, OCR algo degradado):
  - F13 10 A = V-ECU; F25 (¿60 A?) = V-ECU
  - F15 20 A = E-ECU; F1 10 A = I-ECU
  - **F24 5 A = "engine RPM manual control"**: el circuito de régimen manual tiene su propio fusible.
  - https://www.manualslib.com/manual/1664987/Volvo-Ec210b.html?page=183

### 1.2 Valores de servicio: rpm y corriente de la válvula proporcional power shift por modo [VERIFICADO, ALTA]

Fuente: manual de servicio Volvo "Current/pressure, specifications", perfil "EXC, EC210B LC [GB]". Está en las páginas de muestra PDF de https://www.aservicemanualpdf.com/Samplepages/SM-Volvo%20EC210B%20LC%20Excavator%20Service%20Repair%20Manual.pdf (texto extraído con pdftotext; el documento trae dos tablas).

**Tabla 1 (EC210B LC, "Except North America")**, incluida la fila del interruptor de emergencia:

| Rotary switch | Modo | rpm motor sin carga / con carga (±40) | Corriente válvula (mA, ±20) sin carga/carga | Presión secundaria sin carga kgf/cm² (psi) | Conflux cut-off |
|---|---|---|---|---|---|
| 9 | Power max P | 2000 / >1900 | 215 / variable | 3.8 (54) | OFF |
| 9 | Heavy H | 1900 / >1800 | 250 / variable | 5.8 (82) | OFF |
| 8 | General G1 | 1800 / >1700 | 290 / variable | 8.1 (115) | OFF |
| 7 | G2 | 1700 / >1600 | – | – | |
| 6 | G3 | 1600 / >1500 | – | – | |
| 5 | Fine F1 | 1500 | 450 | 19.8 (282) | ON |
| 4 | F2 | 1400 | | | |
| 3 | F3 | 1300 | | | |
| 2 | Idle I1 | 1000 | 555 | 28.5 (405) | OFF |
| 1 | I2 | 800 | | | |
| **Emergency switch** | **High** | **1900** | **340** | | |
| **Emergency switch** | **Low** | **800** | | | |

- La tabla de Norteamérica es igual pero desplazada (H = 2000 rpm, 215 mA), con la misma fila de emergencia: **High 1900 rpm / 340 mA; Low 800 rpm**.
- La segunda tabla del mismo documento (probablemente otra variante o rango de serie; el texto no lo aclara) da valores algo distintos y no tiene fila de emergencia:
  - P 1900 rpm / 215 mA / 2.9 kgf/cm²
  - H 1850 / 245
  - G1 1800 / 275 / 6.0
  - G2 y G3 320 mA / 9.2
  - F1 1400 / 505 / 22.8
  - I1 1000 / 595 / 30.6
- Nota del manual: *"Valve secondary pressure at various current may differ from the specifications according to the external condition."*

El manual de operador (manualslib pág. 63) confirma la misma lógica con tolerancia ±10 mA: P 215, H 250, G1 290, F1 450; en Norteamérica I1 570. https://www.manualslib.com/manual/1664987/Volvo-Ec210b.html?page=63

**Puntos clave para el proyecto [INFERENCIA, basada en las tablas]:**
- La relación es inversa: **más corriente en la válvula power shift → más presión secundaria → menos par o potencia absorbida por la bomba**. P (máxima potencia) usa 215 mA e Idle 555–595 mA.
- Por tanto, **0 mA (V-ECU ausente y sin alimentación alternativa) equivale a la máxima absorción de la bomba**, por encima incluso de P. Así lo describe el usuario ("atascado en máxima potencia").
- **Volvo especifica 340 mA en emergencia "High"**, un punto entre G1 (290) y F1 (450). Es decir, en emergencia de fábrica la bomba debería quedar limitada por debajo de P/H. Si en la máquina del usuario el modo emergencia da "máxima potencia", hay que comprobar si esos 340 mA están llegando a la válvula (ver 1.3).

### 1.3 Cómo se generan los 340 mA en modo manual: la "Resistor Box" [ANECDÓTICO + esquema parcial, MEDIA]

- **HEF, "Volvo EC240B excavator showing no signal to EMC"** (https://www.heavyequipmentforums.com/threads/volvo-ec240b-excavator-showing-no-signal-to-emc.64418/):
  - Un forero veterano describe que el lado "auto" del interruptor auto/manual lleva la señal PWM de la bomba generada por la V-ECU.
  - En manual, la corriente pasa por el interruptor al solenoide PWM de la bomba y vuelve **"through a resistor and to ground"**.
  - Recomienda comprobar que hay tensión de batería en un conector en modo auto y que sale por otro. No da el valor del resistor.
- **Esquemas del manual de servicio EC160B–EC460B** ("UPDATE – EC160B~460B – 03/04", vistos solo como texto OCR vía buscador):
  - Aparecen "Emergency switch", "Power Shift valve" y **"Resistor Box"** en el mismo circuito, más una línea "VECU status" y "Emergency control SW" hacia la E-ECU.
  - Fuentes: https://manualmachine.com/volvo/ec160b/4535011-service-manual/ y https://pdfcoffee.com/ec160b-180b-210b-240b-290b-360b-460b-click-the-volvo-logo-in-the-lower-right-corner-to-return-to-this-menu-main-menu-pdf-free.html (ambas bloqueadas para lectura directa).
- **[INFERENCIA]** Con la bobina de 17,5 Ω a 20 °C (ver 1.4) y 340 mA, la resistencia total del lazo sería unos 71 Ω a 24 V y unos 82 Ω a 28 V con el alternador cargando. Eso da una "resistor box" de **≈55–65 Ω** que disiparía ≈6–8 W.
  - Este valor **no está confirmado por ninguna fuente**: hay que medirlo en la máquina.
  - Por ser un circuito resistivo, la corriente varía con la tensión de batería y con la temperatura de la bobina (el cobre sube ≈0,4 %/°C).
- **Diagnóstico propuesto [INFERENCIA]:** en emergencia High, medir la corriente en serie con el conector de la válvula power shift.
  - Si da 0 mA: buscar resistor box abierta, conector, fusible F24 o el contacto del interruptor auto/manual (varias fuentes citan sus pines corroídos).
  - Si da unos 340 mA y aun así la máquina "va a tope", el problema está en otro sitio, por ejemplo en el regulador de la bomba.

### 1.4 Parámetros eléctricos de la válvula power shift (Kawasaki KDRDE5K) [VERIFICADO fabricante + ANECDÓTICO coincidente]

- **Kawasaki KDRDE5K** (válvula reductora proporcional para controlar el ángulo de bombas de caudal variable):
  - Solenoide **0–0,7 A a 24 V DC** (0–1,6 A a 12 V); presión secundaria 2/3/4 MPa.
  - https://global.kawasaki.com/en/industrial_equipment/hydraulic/valves/kdrde5k.html — ALTA
  - Según el resumen del buscador, el catálogo Kawasaki da **17,5 Ω a 20 °C**. No lo verifiqué directamente; el PDF es https://global.kawasaki.com/en/industrial_equipment/hydraulic/pdf/Catalog_pdf27.pdf (MEDIA).
- Medidas de usuarios:
  - **EC240B:** "PPV resistance of 17.5 ohms"; 24,2 V en la V-ECU con contacto y 27,2 V con el motor en marcha. https://mail.heavyequipmentforums.com/posts/1370873/ — BAJA-MEDIA, coincide con Kawasaki.
  - **EC240BNLC (ER31):** un técnico de JustAnswer dice que el solenoide junto a la bomba mide "about 17 ohms". https://www.justanswer.com/construction-and-road-equipment/absdw-er-31-error-engine-speed-go-down-when.html — BAJA.
  - **EC210:** presión de la válvula reductora unos 450–550 psi a ralentí bajo y unos 50 psi a ralentí alto; resistencia unos 17,5 Ω. https://www.justanswer.com/heavy-equipment/5h8oo-dan-ec-210-ser12409-problem-hyd-pulls.html — BAJA. Concuerda en tendencia con la tabla Volvo: 405 psi en I1 y 54 psi en P.
  - Un forero de HEF sobre un EC210 que "tira el motor": la presión de control debería variar "roughly 100 to 400 psi". BAJA.
- **Proveedores rusos:** venden el solenoide de la bomba principal K3V112DT para EC210B LC como VOE14604266 / VOE14574269 (fabricante HanDok, Corea). https://hydro-help.ru/solinoid-gidravliceskij-nasos-osnovnoj-k3v112dt-ekskavator-gusenicnyj-volvo-ec210b-lc — BAJA (catálogo de vendedor).
- **Umbral de fallo:** un blog de terceros afirma que ER31-03 (alta tensión) salta si la corriente de salida supera 740 mA. Sin confirmar (BAJA).
- **Códigos de la válvula power shift** (MID 187, PPID 1190): ER31-03 alta tensión, ER31-04 baja tensión, ER31-05 circuito abierto. https://sinocmp.com/blogs/repair-technology/volvo-excavator-fault-codes-list — BAJA-MEDIA; varias listas coinciden.
- **Válvula de control de caudal** (opción X1, martillo o cizalla; PPID 1191, ER32-03/04/05): según la misma lista, ER32-03 se activa con más de 14 V en **JA56**. Con ER32-04/05 la bomba queda a caudal máximo, y con ER32-03 a caudal mínimo.

### 1.5 Experiencias de uso prolongado en manual o emergencia [ANECDÓTICO]

| Afirmación | Fuente | Fiab. |
|---|---|---|
| El modo manual "will only allow high and low idle, and 80% hydraulic pump flow, but okay to run machine" (EC210B 2006) | https://www.justanswer.com/heavy-equipment/5hwkg-06-ec210b-hoe-thought-fuel-filters-plugged-thats.html | BAJA |
| En manual "you will just lose all convenience functions and be limited to 90% of machine power and two throttle settings" | JustAnswer EC160BLC https://www.justanswer.com/construction-and-road-equipment/cbwc0-2006-volvo-ec160blc-won-t-start-manual.html y HEF EC240B | BAJA |
| "By switching to manual you by-pass the machine V-ECU in the cab and just use the E-ECU behind the cabin" (EC140BLC) | https://www.heavyequipmentforums.com/threads/volvo-ec140blc-throttle-issue.106470/ | BAJA |
| EC140BLC 2002: en manual desaparece el ER11, "but the engine still operates at full speed/throttle" (sin resolución) | JustAnswer a5u9p https://www.justanswer.com/construction-and-road-equipment/a5u9p-2002-volvo-ec140-blc-excavator-recent-months.html | BAJA |
| **EC210BLC con D6D EAE2 que solo funciona en manual: bajo carga a unos 1900 rpm el motor se cala, sin humo negro.** Cambió la bomba de combustible (4 → 6 bar). Sin respuesta visible | HEF "EC210BLC volvo running on manual mode" https://www.heavyequipmentforums.com/threads/ec210blc-volvo-running-on-manual-mode.106024/ (el buscador asocia el texto a este hilo, aunque el título devuelto difería) | BAJA |
| EC210CL: en manual el dial no sube rpm, con PSID 201-09. "If you quickly switch it to auto mode and turn idle up over 1700 rpms it will usually idle almost indefinitely. But if you put it under load it will give you the red engine malfunction shut down screen and derate rpms" | https://mail.heavyequipmentforums.com/threads/volvo-ec210cl-throttle-dial-wont-work-in-manual-code-psid-201-09.122528/ | BAJA (modelo C) |
| EC240B: en manual arranca y funciona; en auto aparece "no signal to ECU". El concesionario cambió ECU, V-ECU, mazo motor e interruptor auto/manual sin resultado. Con un puente en el relé arrancó; la salida de la V-ECU daba unos 13 V y el borne del relé solo 8 V | HEF 81299 https://www.heavyequipmentforums.com/threads/volvo-ec240b.81299/ | BAJA |
| EC210B LC: con el interruptor de emergencia activo el selector de rpm no funciona; responden "187 is the MID for V-ECU" | HEF https://www.heavyequipmentforums.com/threads/need-wiring-diagram-for-volvo-ec210-blc.57000/ | BAJA |
| Auto-idle: el manual de operador lo vincula a la lógica de la V-ECU (5 s sin mover palancas, pedales ni dial). En manual no hay pasos intermedios ni ralentí automático | manualslib pág. 64 | ALTA para la función; la pérdida en manual es [INFERENCIA] |

**Sobrecalentamiento y consumo:** no encontré reportes específicos de consumo o temperatura en uso prolongado en emergencia. Volvo (material comercial) indica que bajar dos escalones dentro de G reduce el consumo hasta un 10 %, así que operar siempre a unos 1900 rpm tiene un coste de combustible. https://www.volvoce.com/united-states/en-us/resources/blog/2018/how-excavator-work-modes-can-boost-productivity-and-reduce-costs/ (MEDIA, no técnico).

**Calado bajo carga:** la explicación coherente con lo anterior [INFERENCIA] es una válvula power shift a 0 mA (bomba al máximo) con el motor a 1900 rpm y sin el "speed sensing" de la V-ECU, que en modo auto sube la corriente para reducir la bomba cuando cae el régimen. Un forero de HEF lo describe así: "A power-shift signal reduces pump flow to decrease hydraulic horsepower to match available engine horsepower". https://www.heavyequipmentforums.com/threads/volvo-engine-problem-ec210.20147/ — BAJA.

### 1.6 Soluciones DIY y precedentes para regular la bomba sin V-ECU

**Precedentes de fábrica en otras marcas [VERIFICADO en sus manuales vía fragmentos, MEDIA]:**
- **Hyundai R210LC-7 y otros:** "emergency resistor" que se conecta al CN-47 *"in case of failure of the CPU controller"*. Fija la presión de la EPPR y la máquina opera como en "S-mode".
  - Hay que desconectarlo cuando la CPU funciona: *"The resistor must be disconnected whenever the controller CPU is operating."*
  - https://www.scribd.com/document/440901204/Hyundai-R210LC-7-shop-manual y https://www.scribd.com/document/637779540/Trening-Bagera-7-i-7a
- **CAT 320 B/C:** el "backup switch" de cabina anula el control del ECM y deja la máquina a un nivel de potencia fijo; el controlador sube la corriente de la PRV para "destroke" la bomba. https://www.justanswer.com/construction-and-road-equipment/uweyx-cat-excavator-load-sensing-issues.html — BAJA.
- Volvo B usa el mismo principio (resistor box + 340 mA, sección 1.3).

**DIY propuesto [INFERENCIA de ingeniería; no encontré a nadie que lo haya publicado para Volvo]:**
1. **Driver de corriente constante ajustable 0–600 mA** sobre la bobina de 17,5 Ω, con potenciómetro o selector de escalones que reproduzca 215 / 250 / 290 / 340 / 450 / 555 mA.
   - Se prefiere corriente constante (lazo cerrado con shunt) a PWM de duty fijo, porque la resistencia de la bobina cambia con la temperatura.
   - Fallo seguro: si el driver falla, la corriente cae a 0 mA, que equivale a bomba al máximo (lo mismo que ahora). Conviene alternativamente mantener la resistor box en paralelo por conmutación.
   - **Frecuencia de PWM y dither: sin datos Volvo/Kawasaki encontrados.** El catálogo Kawasaki de drivers (Catalog_pdf27) puede incluirlos; consultar.
2. **Opción mínima:** sustituir o complementar la resistor box por un reóstato de potencia (≈30–150 Ω, más de 15 W) o por resistencias conmutadas, siguiendo el precedente Hyundai. La corriente dependerá de la tensión de batería.
3. **Régimen del motor:** en manual el E-ECU solo recibe bajo o alto por cableado (interruptor 26 / F24). Para rpm intermedias habría que:
   - (a) emular por J1939 la petición de régimen de la V-ECU (ver sección 5), o
   - (b) averiguar si la entrada de emergencia del E-ECU acepta algo más que dos niveles. No hay datos públicos.
   - Ejemplos genéricos de TSC1 DIY: https://github.com/UncleAndy123/j1939-engine-panel (Cummins, con gateway USB) y https://microcontrol-germany.github.io/j1939-stack/j1939_example_ecu1.html — MEDIA como referencia de protocolo, no de Volvo.
   - Para controladores comerciales tipo "throttle controller" de excavadora (los de motor paso a paso de Komatsu, Hitachi o el EC210 sin B) no encontré ninguno aplicable al EC210B, cuyo motor es electrónico.

---

## 2. Fallos típicos de la V-ECU en EC210B / EC240B / EC290B / EC140B

### 2.1 Síntomas y códigos

**[VERIFICADO / MEDIA, listas de códigos coincidentes]** MID 187 = V-ECU, MID 128 = E-ECU, MID 140 = I-ECU. Códigos de la V-ECU (MID 187):
- ER11-02: datos intermitentes o incorrectos de la V-ECU
- ER13-09/12 (SID 231): fallo de comunicación J1939
- ER14-09/12 (SID 250): fallo de comunicación J1587
- ER21-00/01 (SID 251): tensión de batería en la V-ECU alta o baja (un documento dice "below 18V")
- ER31 (PPID 1190): power shift
- ER32 (PPID 1191): control de caudal
- SW2701 (PPID 1133): interruptor de régimen

Códigos de la E-ECU (MID 128):
- ER12-02 / ER12-12 (SID 240/253/254): fallo interno de la E-ECU
- ER4E (PID 158): alimentación
- ER43 (SID 22): sensor de régimen del volante

Fuentes: https://sinocmp.com/blogs/repair-technology/volvo-excavator-fault-codes-list, http://es.escavadeiraparts.com/info/volvo-ec210b-fault-code-33300337.html (ES), https://www.scribd.com/document/438347653/187-SID-251.

**Texto de servicio citado en foros (PSID 201-09, E-ECU):** *"The engine control unit (E-ECU) registers: that bus communication is missing with V-ECU on CAN/J1939"*, con FMI 9 y aviso amarillo central. Causas listadas:
- circuito abierto en el mazo
- J1939 cortocircuitado a tensión o a masa
- las dos líneas cortocircuitadas entre sí
- interferencias

Fuentes: HEF EC210CL (122528) y kopaczka.pl (EW160C, PL). MEDIA.

**Para EW160B (Scribd, "Error code"):** causas de un fallo E-ECU/V-ECU relacionado:
- *"Both J1939 or J1587 are disconnected from V-ECU or T-ECU"*
- *"No power supplied to V-ECU..."*
- *"Poor ground connection..."*
- *"Contact resistance in ECU connectors"*

Fuente: https://www.scribd.com/document/814203409/Error-code — MEDIA.

**Síntomas reportados [ANECDÓTICO]:**
- Código "187 (ecu no signal)": la máquina funciona pero sin control del acelerador y queda en ralentí. Fuente: JustAnswer 6vqw3.
- La I-ECU muestra "no signal to ECU/EMC". Un técnico de concesionario (DSK) lo explicó así: **la E-ECU no recibe la "clock signal" de la V-ECU, es decir, la V-ECU "no está viva"**. Fuente: HEF "volvo ec240 b ecu problems" https://www.heavyequipmentforums.com/threads/volvo-ec240-b-ecu-problems.59371/. BAJA, pero relevante para el emulador: **la E-ECU espera mensajes periódicos de la V-ECU**.
- Fusibles que se funden; un usuario lo resolvió desconectando la V-ECU y poniendo un fusible nuevo. BAJA.
- Arranque fallido, apagados, fallos de traslación o de giro. JustAnswer EC140BLC: "all B series machines experienced failures around 3000-6000 hours"; otro hilo habla de unas 3500 h. BAJA.
- Servicio polaco (elektronika.com.pl), síntomas listados:
  - "brak możliwości uruchomienia silnika"
  - "praca koparki w trybie awaryjnym"
  - "brak reakcji na pedał gazu"
  - "brak komunikacji kasety z testerem diagnostycznym"
  - Fuente: https://elektronika.com.pl/uslugi/zakres-uslug/naprawa-elektroniki-w-pojazdach-uzytkowych-i-rolniczych/volvo/naprawa-kaset-sterujacych-koparek-kolowych-gasienicowych-volvo/ — MEDIA.

### 2.2 Causas raíz reportadas [ANECDÓTICO salvo indicación]

- **Contactos internos o chip con zócalo:** un técnico de JustAnswer (EC290BLC) dice:
  - *"every model in this series has experienced problems with the internal connections, where the chips lose contact or exhibit high resistance. The new version features a soldered main chip"*
  - Bajo la tapa metálica, en unidades antiguas "the CPU located in the corner will be removable rather than soldered".
  - Fuente: https://www.justanswer.com/construction-and-road-equipment/kfbnr-ec290blc-volvo-excavator-don-t-break-box.html — BAJA.
  - Lo corrobora un caso de EC140BLC: se abrió la unidad, se limpió la oxidación y se reasentó el microchip, con arreglo temporal (JustAnswer a5u9p).
  - Un dueño de EC240B oyó de su técnico Volvo que "something vibrated loose" (HEF 59371).
- **Humedad y corrosión en conectores detrás del asiento:** "black or green contamination" en los conectores de detrás del asiento; el mazo roza contra tornillos con el movimiento del asiento; corrosión en la placa de la I-ECU. Fuentes: JustAnswer 6vqw3 y dfm8k.
- **Alimentación:**
  - Relés de la caja sobre las baterías: según HEF "Volvo ec210b" 46725, "relays 3&4 control power to the E-ECU", y cambiarlos lo resolvió.
  - Agua atrapada bajo la caja de relés.
  - Baterías que caen bajo carga.
  - Arranques con pinzas o rayos que dañan ECUs (HEF L120E).
  - "ghost codes" por alimentación inestable.
  - Alternador: escobilla dañada asociada a 187 SID 250/231 en EW180B (JustAnswer ES).
- **Interruptor auto/manual:** pines corroídos o cables rotos. HEF 1370873 recomienda limpiarlo; JustAnswer 6vqw3.
- **Mazo motor:** conexión mala en el conector grande del mazo motor que impedía la inyección en un EC240B. https://community.heavyvehicleinspection.com/thread/volvo-ec240b-bogging-down — BAJA.
- **Contra-ejemplo:** "I had the dealer install a new V-ECM, but there were no results!" (JustAnswer 6vqw3). Antes de condenar la V-ECU hay que revisar el mazo.
- **Fallos internos citados por un servicio profesional (studiomaszyn.pl):**
  - "uszkodzona płyta sterownika, przepalone układy scalone, uszkodzona magistrala danych, zawilgocenie"
  - Fuente: https://studiomaszyn.pl/naprawa-elektroniki/volvo/ — MEDIA.
- **Taller de reparación USA (ecmrepairusa), síntomas de la V-ECU 14518349:** fusibles fundidos, sin comunicación, apagado del motor, entrada de aceite o agua, "injector driver faults". MEDIA-BAJA (marketing).
- **Drivers de solenoides proporcionales quemados:** no encontré ningún reporte explícito de placa quemada en la salida power shift. Hay una advertencia de vendedor: "a shorted plug can burn out the controller", así que hay que revisar el conector antes de montar la unidad nueva (BAJA).

---

## 3. Enfoques de reparación

### 3.1 Reparación de placa
- Servicios con reparación por correo:
  - Polonia: studiomaszyn.pl, elektronika.com.pl, mechatronika.pomorze.pl
  - Rusia: largoautospb.ru, "ремонт блока управления VECU 14518349", precio a convenir. https://www.largoautospb.ru/remont-ebu-vecu-ekskavator-volvo.php
  - EE. UU.: ecmrepairusa, 14518349 por **US$957**, diagnóstico de US$200 si no es reparable; la unidad vuelve "prepared for reinstallation into the same machinery". https://ecmrepairusa.com/product/voe14518349-volvo-excavator-vecu-v-vecu-ecu-contoller-repair-service/
- Ninguna fuente identifica componentes concretos (referencias de CI) que fallen en la V-ECU B. **No encontrado.**

### 3.2 Clonado de EEPROM o flash
- studiomaszyn.pl (MEDIA): *"jesteśmy w stanie przegrać zawartość procesorów lub pamięci flash/eeprom do sterownika dawcy z innej maszyny"*. Afirman que así se conservan los datos y la configuración originales sin recodificar.
- Servicio ruso td-truck (camiones, extrapolable con cautela): "новый блок пустой… старый блок лучше сохранить и перенести прошивку".
- No encontré volcados ni hilos técnicos sobre la MCU o EEPROM de la V-ECU EC210B en mhhauto ni digital-kaos.

### 3.3 V-ECU usada o nueva: programación
- Los vendedores venden la V-ECU "programmed" y piden la placa de modelo o el número de serie de la máquina: *"different models use different programs"* (fridayparts 14518349; BAJA-MEDIA).
- JustAnswer EC290BLC: *"The ECU comes blank unless you specify your serial number and request it to be preprogrammed"*; el coste ronda **US$4000** según varios posts. BAJA.
- Documento de actualización Volvo EC160B–460B (fragmento vía buscador): **"Code Lock (Anti-theft) setting is saved at the VECU"**; también describe la programación de parámetros de la VECU. https://pdfcoffee.com/ec160b-180b-210b-240b-290b-360b-460b-click-the-volvo-logo-in-the-lower-right-corner-to-return-to-this-menu-main-menu-pdf-free.html — MEDIA.
- Boletín Volvo (E-ECU): reprogramación con **VCADS Pro**; los pedidos y la reprogramación dependen del número de serie y de la fecha de producción. https://www.scribd.com/document/581311237/128sid231 — MEDIA (solo fragmento).
- Parámetros Volvo en general (manual VCADS): hay "Customer parameters" (locales) y "Vehicle parameters" (requieren conexión a la VDA de Volvo). Fuente: https://www.scribd.com/document/75959914/VCADS-User-Manual-Volvo — MEDIA.
- Digital-kaos (camiones): con VCADS se pueden ver los parámetros pero no transferirlos entre ECUs. https://www.digital-kaos.co.uk/forums/showthread.php/199119-Volvo-Flash-files-for-programming-new-ecm — BAJA.

### 3.4 Números de pieza (de vendedores; BAJA-MEDIA, verificar en catálogo)

| Pieza | Números |
|---|---|
| V-ECU serie B | 14518349, 14514090, 14531360, 14594697; 14594707 (C/D) |
| "Cab controller" | 20577135 (algunos lo listan como V-ECU, otros como E-ECU) |
| E-ECU D6D/D7D | 60100000, 60100001, 60100002, 20577131, 20582958, 03161983 |
| I-ECU / monitor | **14390065**, 14636301, 14527149, 14515555 |

- **Ojo:** el **14390065** que menciona el proyecto como "V-ECU antigua" aparece en todos los anuncios como **I-ECU / monitor** (o como su conector), no como V-ECU. https://www.fridayparts.com/monitor-plug-connector-of-ecu-voe14390065-voe14636301-for-volvo-excavator-ec210-ec240-ec290-ec360-ec140
- Un anuncio de sinocmp describe la 60100000 como "TRW engine control unit". BAJA.

### 3.5 Emuladores o controladores universales
- **No encontré a nadie que haya publicado un emulador de V-ECU** para Volvo EC B, ni controladores universales específicos.

---

## 4. Conectores

- **V-ECU serie B (EC210B):** dos conectores, **JA** (grande) y **JB** (pequeño).
  - HEF, sobre la ubicación: "Behind the seat next to the HVAC box is your VECU" y el "little one" **JB tiene 2 rojos y 2 negros: JB7, JB8, JB15, JB16 (rojo = +, negro = masa)**.
  - JA14/JA15 aparecen como masas y JA56 como salida de la válvula de control de caudal (lista de códigos).
  - Fuentes: https://www.heavyequipmentforums.com/threads/need-wiring-diagram-for-volvo-ec210-blc.57000/ y sinocmp. BAJA-MEDIA.
  - Otro post interpreta "187 251 1" como baja alimentación de la VECU en "VB 15 & 16". BAJA.
- **V-ECU serie D (EC380D):** conector **VA de 70 pines + VB de 16 pines** (Volvo "V-ECU, I/O List"). https://www.scribd.com/document/577472120/ec380d-vec — MEDIA, otra generación.
- **E-ECU EMS:** no encontré la referencia del conector del D6D EAE2.
  - Hay pistas de camiones con EMS2.2 (dos conectores EA/EB) en mhhauto, y de un adaptador "62Pin… EMS2.2-2.3-2.4".
  - **No confirmado para D6D.**
- **Conectores de recambio:** se venden "VECU controller connector plug 14518349/14594697" y conectores de la 60100000, sin número de pieza Deutsch/TE.
  - https://www.ebay.com/itm/384979664114 y https://sinocmp.com/products/volvo-controller-connector-plug-for-ec210-ec240-ec210b-ecu-60100000
  - **No encontré números de pieza de carcasas ni terminales (Deutsch, AMP) para la V-ECU B.** Hay que identificarlos físicamente.
- **Adaptación entre versiones de V-ECU:** no encontré experiencias publicadas.

---

## 5. Comportamiento de la E-ECU D6D (EMS) sin V-ECU

- **[VERIFICADO, manual de operador]** La máquina está diseñada para funcionar con la V-ECU averiada: interruptor 25 en Manual y régimen solo por el interruptor 26 (bajo 800 rpm o alto unos 1900 rpm con 340 mA en power shift). El usuario confirma que su máquina arranca y funciona así.
- **Inmovilizador / Code Lock:** según el documento de actualización (MEDIA), el código antirrobo se guarda en la VECU. No encontré que la E-ECU D6D tenga un inmovilizador propio que impida el arranque en manual.
  - Hilo de digital-kaos (camiones): "if the truck is older without immobilizer you dont need to reprogram the ecu". BAJA.
- **En modo AUTO sin V-ECU:** la I-ECU muestra "no signal to ECU". La E-ECU registra PSID 201-09, *"bus communication is missing with V-ECU on CAN/J1939"*. Según los foros, la falta del "clock signal" o heartbeat de la V-ECU es lo que se detecta.
- **TSC1 / petición de régimen:** no hay documentación pública de cómo la V-ECU pide el régimen a la E-ECU en el EC210B (PGN, SA, mensaje propietario o TSC1).
  - Analogía con Volvo Penta EMS2 (MEDIA, otra calibración): TSC1 anula el pedal de VP Status; arbitraje por prioridad; SA 0x03 tiene prioridad máxima.
  - En EMS2.3, "if no valid VP70 messages are received, engine speed is set to idle".
  - Fuentes: https://www.dieselgeneratortech.com/diesel-engines/More-Available-Control-Functions-of-Volvo-Engine.html y https://pdfcoffee.com/download/electrical-interface-specification-ems2347706487en-pdf-free.html.
  - **[INFERENCIA]** Para emular la V-ECU habrá que capturar con un sniffer el tráfico J1939/J1587 de una máquina EC210B sana en modo auto (todos los PGN con SA de la V-ECU, su periodicidad y su respuesta a los cambios de dial). Las fuentes públicas no lo documentan.

---

## 6. Bus CAN J1939 y J1587/J1708: medidas

- **Resistencia del bus:** unos 60 Ω entre CAN-H y CAN-L con el sistema sin tensión (2 × 120 Ω). 120 Ω indica que falta un terminador; unos 40 Ω, que sobra uno.
  - Usuario de EW140B: "I checked all the bus wiring and 60 ohms resistance".
  - Fuentes: https://community.heavyvehicleinspection.com/thread/volvo-ew140b-comms-problem-and-no-travel (BAJA-MEDIA) y el boletín NHTSA de camión https://static.nhtsa.gov/odi/tsbs/2020/MC-10172045-0001.pdf (ALTA, pero de camión).
  - En la Volvo L90E (cargadora), el terminador está detrás del panel de instrumentos; mide 60 Ω conectado y 120 Ω desconectado. HEF https://www.heavyequipmentforums.com/threads/volvo-l90e-e-ecu-problem.75453/ — BAJA.
  - **Ubicación de los terminadores en el EC210B: no encontrada.**
- **Daños de mazo:**
  - Mazo pellizcado bajo el retén de la plataforma de la cabina cerca de la V-ECU (EW140B).
  - Roce con el movimiento del asiento.
  - Roce contra la tapa de la caja de baterías.
  - Cortocircuitos en los pasamuros del conector de la E-ECU entre pares CAN (L90E).
  - "I just had a communication wire broken" (EC210).
  - No encontré casos de roedores ni de mazo de pluma en EC210B.
- **Procedimiento típico citado:**
  1. Con la batería desconectada, medir 60 Ω.
  2. Comprobar continuidad de cada hilo y descartar cortos a masa o a +24 V.
  3. Con contacto, medir las tensiones CAN-H y CAN-L (en camiones Volvo/Daimler unos 2,3–2,5 V en reposo). El valor para EC210B no está confirmado.
  4. Desconectar las ECUs una a una.
  5. Verificar alimentación, masa e IGN de la V-ECU (24 V con contacto y unos 27 V en marcha, EC240B).

---

## 7. Procedimientos de diagnóstico citados

- **Manual de servicio** (índice, servicepartmanuals / aplusmanual):
  - "Proportional solenoid valve, measuring and adjustment"
  - "Proportional solenoid valve (power shift), replacing"
  - "Emergency engine speed control switch, description/specifications"
  - Medición recorriendo los modos P → H → G → F → I y comprobando corriente y presión secundaria a ralentí bajo y alto.
- **Toma de servicio** (interruptor 28) para VCADS Pro, SDU o MATRIS (manual de operador, pág. 73). ALTA.
- **Antes de soldar:** desconectar la V-ECU, la E-ECU y la I-ECU (manual de servicio EC210B LC, muestra PDF). ALTA.
- **Orden recomendado por foros:**
  1. Leer los códigos (MID / PSID / FMI).
  2. Fusibles F1, F13, F15, F24 y F25, y relés de la caja de baterías (intercambiar los R3/R4).
  3. Conectores detrás del asiento y del interruptor auto/manual.
  4. Alimentación y masa de la V-ECU (JB7, JB8, JB15, JB16).
  5. Bus a 60 Ω.
  6. Solo entonces, V-ECU.

---

## 8. Resumen de lagunas
- Valor real de la "resistor box" de emergencia y su ubicación.
- Pinout completo del JA de la V-ECU B.
- Mensajes J1939 V-ECU → E-ECU (PGN, SA, periodicidad).
- Frecuencia PWM y dither de Volvo para la válvula power shift.
- Conector y pinout de la E-ECU D6D EAE2.
- El significado del P/N VCE56003584.
- No existe ningún emulador público.
