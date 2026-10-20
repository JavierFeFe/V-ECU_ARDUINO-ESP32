# Conectores para el proyecto ESP32 ↔ mazo Volvo EC210B (2002) — identificación y compra

Fecha: 2026-10-19. Escala de fiabilidad de cada identificación: **CONFIRMADO** (hoja de datos del fabricante o documento Volvo/Kawasaki), **PROBABLE** (varias fuentes concordantes pero sin hoja de datos), **DESCONOCIDO** (no se ha podido identificar con fuentes; se propone alternativa). Las URL de vendedores son listados vivos: los precios son los vistos hoy (USD salvo que se indique) y cambian.

> **Corrección posterior (2026-10-20):** las asignaciones de JB13/JB14/JB5 de este informe están superadas. Según el circuito OEM "Control Circuit (EC160B~EC460B)", el J1939 de la V-ECU es **JB14 (H) / JB6 (L)**, derivación del mismo par que une la E-ECU (B1/B2) con el panel; **JB13 y JB5 son las mallas** de los cables J1587 y J1939. Sin V-ECU el bus no se parte y no hay que puentear nada. Ver `docs/INVESTIGACION_V-ECU_EC210B.md` §3.

Nota de alcance: eBay bloquea la lectura automatizada (403), por lo que los precios de eBay proceden de los extractos de búsqueda, no de la ficha completa. Scribd no entregó texto. Varias respuestas se apoyan en los hallazgos ya documentados en `research_familia_eecu.md` y `research_penta_tad.md` (misma carpeta), que se citan donde procede.

---

## Resumen ejecutivo

| Ítem | Identificación | Fiabilidad | Qué comprar / alternativa |
|---|---|---|---|
| A. E-ECU 03161983/60100002/20577135 — 2 conectores de 36 vías (3×12) | Fabricante/serie **no identificado**. Foto del contraconector aftermarket: carcasa rectangular con **palanca giratoria amarilla** (CPA/ayuda de inserción), una carcasa **negra** y otra **gris** (codificación), cavidades para terminales planos tipo 2,8 mm o similar. | DESCONOCIDO (fabricante) / CONFIRMADO (que existe pigtail aftermarket) | Pigtail aftermarket SINOCMP "Volvo Controller Engine ECU Connector Plug 60100000" (par de conectores con cables ya crimpados) **US$ 259**, o canibalizar una E-ECU averiada. Pedir al concesionario Volvo CE el nº VOE del "contact housing" por nº de serie (grupo 37 del catálogo). |
| B. V-ECU 14518349 — JA (70) + JB (16) | Familia **no identificada** (sin hoja de datos). Se vende el contraconector aftermarket con pigtail. | DESCONOCIDO (fabricante) / CONFIRMADO (pigtail disponible) | eBay "Vecu Controller Connector Plug 14518349 14594697" **US$ 163,77 + 29,99 envío**; DeedParts (precio bajo consulta); Amazon.com SINOCMP B06W9JF7XT. V-ECU reacondicionada **US$ 330** (donante para arrancar cabeceras). No aparecen V-ECU usadas/averiadas baratas. |
| C1. Bobina Kawasaki KDRDE5K (válvula proporcional / power-shift) | **TE/AMP Econoseal J Mark II (+)**, 2 vías, paso 4,8 mm. En la válvula va la **cap housing 174354-2** con terminal macho **173706-1**. El contraconector de mazo es el **plug 174352-2** con terminales hembra **173707-1** (0,5–1,25 mm², AWG 20-16) y junta unifilar **1-172888-3** (ø aislamiento 2,0–2,6 mm). | CONFIRMADO (hoja Kawasaki + TE) | TE 174352-2 + 2× 173707-1 + 2× 1-172888-3. RS/Farnell/Mouser/DigiKey/TME. |
| C2. Conector de la "Resistor Box" EC210B | **No encontrado** en ninguna fuente pública. | DESCONOCIDO | Identificar in situ (foto/marcas) o puentear la caja: es una resistencia de 60 Ω nominales en serie con la válvula power-shift para el modo manual. |
| D1. Toma de servicio 8 pines (VCADS/MATRIS, en cabina sobre la radio) | Volvo CE 8 pines **sólo lleva J1708/J1587 + alimentación**: GND, +24 V, J1708+/-; **no lleva CAN J1939** (en el esquema L120E el par CAN va a la I-ECU/V-ECU, no a la toma IA/IB). | PROBABLE (tabla DrewLinQ + esquema L120E) | Para CAN hay que pinchar en el mazo: E-ECU **B1 (CAN-H)/B2 (CAN-L)**; V-ECU **JB13 (H)/JB14 (L)**. |
| D2. Genéricos | Deutsch DT/DTM, crimpadora, transceptores CAN, caja estanca | CONFIRMADO | Ver §D. |

---

## A. E-ECU Volvo CE (D6D) 03161983 / 60100002 / 20577135 — conectores "A" (negro, motor) y "B" (rojo/gris, vehículo), 36 vías

### A.1 Qué se sabe del hardware
- La E-ECU es la misma plataforma hardware que la EECU VECTRO II de camión Volvo D12/D7C (Lucas Varity, Reino Unido) y, según los reparadores, la fabrica hoy **Delphi/TRW** (Unitech Electronics la atribuye a Delphi Electronics & Safety; SINOCMP describe el 60100000 como "TRW ECU") — **PROBABLE**. Fuentes: https://www.unitechelectronics.ca/volvo-ecm-20577135-p02-repair-tested-and-rebuilt/ ; https://sinocmp.com/products/voe-60100002-volvo-ec210blc-ec210b-ecu
- Pinout útil del conector B (lado vehículo) ya confirmado en `research_familia_eecu.md` (dos fuentes Volvo): **B1 = CAN-H, B2 = CAN-L (J1939), B25/B26 = J1587 A/B, B9/B10 = masa, B11/B12 = +24 V**. — **CONFIRMADO**.
- La E-ECU **no es un EMR2 estándar**: el EMR2 Deutz usa un conector de vehículo de **25 polos** (Deutz "EMR 2 System Description", manualslib p.25: https://www.manualslib.com/manual/1706173/Deutz-Emr-2.html?page=25), mientras que la E-ECU Volvo lleva 2×36. Por tanto **no sirven** los contraconectores EMR2 de Deutz/JLG. — **CONFIRMADO**.

### A.2 Identificación del conector (fabricante/serie)
- **Resultado: DESCONOCIDO.** Ninguna de las ~40 búsquedas (en inglés, alemán, ruso) devolvió un número de pieza TE/Delphi/FCI/Bosch para el conector de 36 vías de la EECU D12/E-ECU D6D, ni un kit de reparación Volvo ("VOE" o "20xxxxxx") para él. Tampoco aparece en los boletines Volvo Trucks de reparación de conectores (que sí dan pin/zócalo/sello para otros conectores, p. ej. VGT: https://static.nhtsa.gov/odi/tsbs/2012/SB-10044246-5144.pdf).
- Descartados por verificación: Delphi Micro-Pack 100W/36 vías (sin palanca), Deutsch DRC (70 vías, no 36), kits Volvo 20429842/20429843 (son los **62 vías** del EMS2 D13: https://www.duallane.com/volvo-engine-harness-gray-plug-housing-20429843), FCI 211PC (sin resultados), TE 1-1703639-1 (no verificable).
- **Pista física fiable (foto del pigtail aftermarket, ver imagen en `dl/sino_eecu_plug.jpg`)**: dos carcasas rectangulares idénticas, una **negra** y otra **gris**, con **palanca giratoria amarilla con cubo redondo** (ayuda de acoplamiento/CPA), 3 filas de cavidades pequeñas (compatibles con terminales planos ≈2,8 mm o "Timer" 1,5/2,8), salida de cable con capuchón trasero. Con esa foto y las marcas moldeadas en la carcasa original (normalmente llevan logotipo del fabricante y nº de pieza en la cara trasera) un distribuidor (TE/Aptiv) puede identificarlo en minutos. **Acción recomendada: fotografiar la cara trasera del conector original de la máquina y buscar el nº moldeado.**

### A.3 Dónde comprar hoy (sin conocer el fabricante)
| Opción | Enlace | Precio | Notas |
|---|---|---|---|
| Pigtail aftermarket: par de conectores (negro + gris) con ~36 cables cada uno ya crimpados y sellados | https://sinocmp.com/products/volvo-controller-connector-plug-for-ec210-ec240-ec210b-ecu-60100000 | **US$ 259,00** | "Volvo Controller Engine ECU Connector Plug for EC210 EC240 EC210B ECU 60100000". Es la vía más rápida: los cables ya traen terminal y junta; sólo hay que empalmar/soldar al lado ESP32. Confirmar con el vendedor que incluye los **dos** conectores (la foto muestra ambos). — CONFIRMADO que existe; compatibilidad por nº de ECU (BAJA, vendedor). |
| Mazo motor completo D6D (incluye los dos conectores de la E-ECU + conectores de sensores) | https://wdpart.com/products/14512670-14513137-14512406-ecu-wiring-harness-for-volvo-d6d-d7d-ec210b-ec240b-ec290b ; https://www.vankeparts.com/vankeparts-volvo-excavator-ec210b-ecu-wiring-harness-d6d-engine-high-quality-part-no-14512406 ; eBay 14513137: https://www.ebay.de/itm/315613534843 | consultar (típ. 150–400 US$) | Nº Volvo 14512406 / 14512670 / 14513137. Útil si se quiere un mazo "sacrificable" para cortar los conectores con cola de cable. |
| E-ECU averiada/usada como donante (cabeceras lado ECU para el banco de pruebas) | eBay búsqueda "60100002 20577135 ECU" (p. ej. https://www.ebay.com/itm/374932661615 , https://www.ebay.com/itm/387350498892); Machineryline (Lituania, unidades nuevas+usadas): https://machineryline.com/-/control-units/Volvo/EC-210--c2334tm2819m4521 | nuevas programadas 380–1.300 US$; usadas: preguntar | No se ha encontrado ninguna E-ECU anunciada como "averiada/para piezas". Pedir a desguaces de maquinaria (Machineryline, Mascus) una unidad "sin programa/para piezas". |
| Concesionario Volvo CE | Catálogo de piezas por PIN de la máquina, grupo 37 (sistema eléctrico), "contact housing"/"terminal" del mazo motor | — | Volvo sí vende "repair terminals" (terminal pre-crimpado en 15 cm de cable) para la mayoría de conectores; es la forma de obtener el terminal y la herramienta correctos sin conocer el fabricante. |

**Terminales/crimpadora**: no identificables sin el fabricante. Si se compra el pigtail SINOCMP no hacen falta (ya vienen crimpados). Si se canibaliza un mazo original, extraer los terminales con un juego de extractores universales (p. ej. "terminal removal tool kit 76 pcs", 15–25 € en Amazon.es) y reutilizarlos soldando el cable nuevo.

**Variantes de color/codificación**: la ECU lleva un conector **negro (A, motor)** y otro **rojo (B, vehículo)** según el enunciado; el pigtail aftermarket muestra negro + **gris**. Las dos carcasas son mecánicamente codificadas (no intercambiables). Para el proyecto sólo interesa el **B (vehículo)**: CAN B1/B2, J1587 B25/B26, alimentación B11/B12, masa B9/B10.

---

## B. V-ECU 14518349 / 14594697 / 14531360 / 14514090 — conectores JA (70 vías) y JB (16 vías)

### B.1 Identificación
- **Fabricante/serie: DESCONOCIDO.** Ninguna fuente pública (listados, foros HEF, manuales accesibles) nombra la familia del conector de 70 vías. Las búsquedas por Deutsch DRC 70 vías (DRC12-70PA/DRC16-70SA) no lo vinculan a Volvo; la foto de DeedParts (baja resolución, `dl/deed_vecu_plug.jpg`) muestra una carcasa negra alargada con muchas cavidades y cables de colores, no Deutsch DRC (que es redondo-rectangular con tuerca).
- Pines de bus ya confirmados (`research_familia_eecu.md`, Volvo CE Korea EC210B-04): **JB13 = CAN-H, JB14 = CAN-L, JB5 = J1587 A, JB12 = J1587 B**; alimentación de la V-ECU: F13 10 A y F25 60 A. — **CONFIRMADO**.

### B.2 Dónde comprar el contraconector (lado mazo)
| Vendedor | Enlace | Precio | Notas |
|---|---|---|---|
| eBay (Shenzhen, "CMP Heavy Equipment Parts") "Vecu Controller Connector Plug 14518349 14594697 For Volvo EC210B EC240B EC290B" | https://www.ebay.com/itm/384979664114 (también https://www.ebay.com/itm/387283763976 , https://www.ebay.de/itm/375584859654) | **US$ 163,77** (antes 174,22) + **US$ 29,99** envío; 9 uds. | Usa los números de la propia V-ECU, no del conector. Pedir foto con recuento de pines (70+16) antes de comprar. — CONFIRMADO listado. |
| Amazon.com SINOCMP "Controller Connector Plug Wire for Volvo VOE 14518349" | https://www.amazon.com/VOE-14518349-Controller-Plug-Excavator/dp/B06W9JF7XT | consultar (no accesible hoy, error 500) | Mismo producto con pigtail. |
| DeedParts "Vecu Controller Connector Plug for Volvo EC210B, EC240B, EC290B" | https://www.deedparts.com/vecu-controller-connector-plug-for-volvo-ec210b-ec240b-ec290b.html | precio bajo consulta (email) | Aftermarket China. |
| Mazo de cabina/VECU original (incluye JA/JB con cola de cable) | eBay 14524053 "Kabelbaum für Volvo EC210B…" https://www.ebay.de/itm/387233625844 ; 14644021 https://www.ebay.de/itm/386354377675 | consultar | Alternativa para cortar los conectores con 20–30 cm de cable y empalmar. |

**Cabeceras lado ECU (PCB header) sueltas**: **no se venden**; sólo se obtienen de una V-ECU donante.

### B.3 V-ECU usada/averiada como donante — precios vistos
| Listado | Precio | Estado |
|---|---|---|
| eBay.de autogentechno0, "Programmed EC210B VECU 14518349", reacondicionada | **≈ US$ 330** | refurbished — https://www.ebay.de/itm/146727654917 |
| eBay cmppartsusa (HK) 14518349 | US$ 260,37 + 19,99 | nueva aftermarket — https://www.ebay.com/itm/157088641238 |
| eBay SINOCMP 14518349 | US$ 360–380 | nueva, 6 meses garantía — https://www.ebay.de/itm/384600458999 |
| eBay 14531360 (EC210B compatible) | US$ 458,49 | nueva — https://www.ebay.de/itm/135067490378 |
| Fridayparts VOE14518349 | consultar | https://www.fridayparts.com/for-volvo-excavator-ec240b-ec290b-ec330b-ec360b-ec460b-ec700b-ec700bhr-controller-voe14518349 |
| Machineryline (Lituania): "V-ECU 14531360 / 14518349 / 14594697 … NEW+USED units" | consultar | https://machineryline.info/-/sale/control-units/backhoe-loader/Volvo/excavator-ECU-EDC-engine-control-unit-210-BLC-L120E-D6D-Con--17010415043750433400 |

**Conclusión B**: no hay V-ECU "para piezas" baratas anunciadas (mínimo visto ≈ 260–330 US$). Para el proyecto es más barato el pigtail del contraconector (≈ 165 US$) que canibalizar; la V-ECU donante sólo compensa si se quiere además un banco de pruebas con la unidad original.

---

## C. Kawasaki KDRDE5K (válvula proporcional) y Resistor Box

### C.1 Conector de la bobina KDRDE5K — **CONFIRMADO**
Hoja Kawasaki "Electric Proportional and Directional Pilot Control Valves" (https://www.kawasakihydraulics.com/app/uploads/2019/10/Electric-Proportional-and-Directional-Pilot-Valves-Kawasaki-1.pdf), texto extraído:
- "TYPE OF CONNECTOR: EQUIVALENT TO ECONOSEAL J SERIES CONNECTORS MARK(+) CAP HOUSING"
- "CAP HOUSING: 174354-2" (en la válvula) · "TERMINAL: 173706-1" (macho, en la válvula)
- Eléctrico (modelo 24 V, p. ej. KDRDE5K-31/30C50-143-T): **700 mA nominal, 17,5 Ω a 20 °C, 20,4–27,6 V, dither recomendado 80 Hz / 200 mA p-p, 17 W**. Versión 12 V: 1,6 A. Sin polaridad (proporcional).

Contraconector lado mazo (TE Connectivity, serie **Econoseal J Mark II (+)**, 2 vías, paso 4,8 mm, IP sellado):

| Pieza | TE nº | Función | Dónde | Precio aprox. |
|---|---|---|---|---|
| Plug housing 2 vías (hembra, lado mazo) | **174352-2** (negro) | contraconector de 174354-2 (hoja TE: "070 ECONOSEAL MARK-2 PLUG 2P", 18,5 A, -30…105 °C) https://www.te.com/en/product-174352-2.html | Heilind https://estore.heilind.com/amp174352-2.html ; Element14/Farnell (buscar 174352-2); DigiKey (174352-2 "no longer available" en DigiKey ES — buscar en Mouser/TME/RS) | ≈ 0,5–1,5 € |
| Terminal hembra | **173707-1** | receptáculo 1,8 mm, **0,5–1,25 mm² (AWG 20-16)**, ø aisl. 2,0–2,7 mm, estañado https://www.te.com/en/product-173707-1.html | RS "EconoSeal J Mark II Female" https://uk.rs-online.com/web/p/automotive-connector-terminals/7122037 ; TE China datasheet https://www.te.com.cn/chn-zh/product-173707-1.datasheet.pdf | ≈ 0,2–0,5 €/ud |
| Junta unifilar (SWS) | **1-172888-3** | silicona, cavidad 4,4 mm, cable ø 2,0–2,6 mm (hoja: https://www.zoro.com/static/cms/enhanced_pdf/Waldom%20Electronics_productxx1xx172888xx3.datasheetxx614b93.pdf) | RS (bolsa 1000, 0,151 €/ud) https://fr.rs-online.com/web/p/joints-de-connecteur-automobile/1613783 ; RS "Seal Plug" https://uk.rs-online.com/web/p/automotive-connector-seals/7199652 | ≈ 0,15 €/ud |
| Cap housing (si se quiere el lado válvula para banco) | 174354-2 | https://www.te.com.cn/chn-zh/product-174354-2.datasheet.pdf ; Element14 https://www.element14.cn/en-CN/amp-te-connectivity/174354-2/housing-econoseal-2way/dp/1772827 ; Octopart $0,47 https://octopart.com/part/te-connectivity/174354-2 | — | ≈ 0,5 € |
| Terminal macho (lado válvula) | 173706-1 | 0,5–1,25 mm² https://uk.rs-online.com/web/p/crimp-contacts/6806952 | RS | ≈ 0,3 € |

Crimpado: terminales abiertos tipo "F" (crimp conductor + crimp sobre la junta). Vale cualquier crimpadora de trinquete para terminales abiertos no aislados de 0,5–1,5 mm² con mordaza de doble crimp (p. ej. Engineer PA-21 o IWISS IWS-2820/SN-28B; 25–45 € en Amazon.es). TE no publica en la ficha la herramienta manual; el aplicador industrial no es necesario para 2 contactos.

**Notas**: Volvo también vende la válvula completa y su conector dentro del mazo de la bomba (nº Volvo del solenoide power-shift: ver "Proportional solenoid valve (power shift), replacing" en el manual). Comprobar en la máquina que el conector es efectivamente el de 2 vías con cap 174354-2 (algunas KDRDE5K para otros OEM montan Deutsch DT04-2P). — La identificación es CONFIRMADA para el estándar Kawasaki; la variante montada por Volvo es PROBABLE.

### C.2 Conector de la "Resistor Box" EC210B — **DESCONOCIDO**
- Ninguna búsqueda (inglés/español) devolvió el nº de pieza de la caja de resistencia ni de su conector. Lo que sí está documentado (`research_familia_eecu.md`, Volvo CE Korea EC210B-04): es una **resistencia de 60 Ω nominales (25 °C)** en serie con la válvula power-shift, activa sólo en modo manual (switch Auto/Manual) y da ≈340 mA. Para el proyecto ESP32 (que controlará la válvula por PWM) la caja **puede dejarse en el circuito manual de emergencia** y no hace falta su conector.
- Si se necesita, identificarlo in situ: previsiblemente un conector sellado de 2 vías de la familia usada en el resto del mazo de cabina (Deutsch DT o AMP Superseal 1.5), ambos trivialmente reemplazables (ver §D).

---

## D. Toma de servicio y material genérico

### D.1 Toma de servicio 8 pines del EC210B ("28 Service socket (VCADS Pro, SDU, MATRIS), a la izquierda sobre la radio" — manual del operador EC210B, p.72)
- Tabla de conectores "Volvo Construction Equipment – 8 and 14-Pin" (DrewLinQ/Opus "Industry Connectors Reference", p.8: https://opusivs.com/wp-content/uploads/2023/12/DrewLinQ_Industry_Connectors_Reference_OpusBranded.pdf): **8 pines: 1 = GND, 8 = +Bat, 4 = J1708+, 7 = J1708-**; **14 pines: 14 = GND, 13 = +Bat, 8 = J1708+, 9 = J1708-**. **No lista ningún pin CAN.** — PROBABLE (documento de fabricante de interfaces, no de Volvo).
- Esquema Volvo L120E Sch24 (misma generación, `dl/L120E_MENY.txt`): la toma de servicio es doble, **IA (14 vías)** e **IB (8 vías)**. IB: pin 1 = 15EA-14 (+24 V tras fusible FU14 5 A), pin 2 = Y/R (J1708 A), pin 3 = Y/SB (J1708 B), pin 4 = BL/Y "2135" (línea desde E-ECU EB24, probablemente K-line/SERDIA), pin 8 = masa. IA: 8/9 = J1708 A/B, 13 = +24 V, 14 = masa, IA1–IA7 = líneas a la I-ECU (P3.19…P2.1, display/MATRIS). **El par CAN J1939 (hilos BL/W + BL, con terminador R702 120 Ω en la I-ECU) no llega a IA/IB**. — PROBABLE para el EC210B (es el L120E; el EC210B 2002 pre-14132 lleva MDU en lugar de I-ECU, pero la misma filosofía: VCADS Pro habla con las ECUs por J1708/J1587, no por CAN).
- Pinout genérico de la toma 8 pines de camión Volvo (pinoutguide: 1 GND, 4 J1708+, 7 J1708-, 8 +24 V) coincide con la de Volvo CE: https://pinoutguide.com/CarElectronics/Volvo_truck_8_pole_diagno_pinout.shtml
- **Conclusión**: la toma de servicio **sirve para J1587/J1708 (9,6 kb/s) y alimentación, no para CAN**. Para leer/inyectar J1939 hay que pinchar en el mazo: **E-ECU B1/B2** o **V-ECU JB13/JB14** (par trenzado amarillo/verde), respetando los dos terminadores de 120 Ω existentes (uno en la E-ECU/I-ECU y otro en la V-ECU/MDU) — no añadir un tercero.
- Conector físico de la toma: no se ha podido confirmar el nº Deutsch/Volvo del zócalo 8 pines CE (los cables VCADS 88890180/88890304 son "8-pin rectangular Volvo", no Deutsch HD10-9). Si se quiere un enchufe para J1587: cable adaptador "Volvo 8 pin" (p. ej. https://www.ebay.de/itm/284400900348 , 15–30 €) y cortar.

### D.2 Deutsch DT / DTM (para los empalmes nuevos ESP32 ↔ mazo)
| Qué | Enlace | Precio |
|---|---|---|
| Carcasas sueltas DT04-12PA / DT06-12SA (RS España) | https://es.rs-online.com/web/b/deutsch/ (DT06-12SA 5,99 € + IVA; DT04-12PA 4,48 € + IVA) | 4–6 € |
| Kit DT 2/3/4/6/8/12 vías con crimpadora de trinquete (216 pzas) | Amazon (ASIN B0F3TM6BGH, seguimiento camelcamelcamel) https://camelcamelcamel.com/product/B0F3TM6BGH — buscar "kit conectores Deutsch DT crimpadora" en Amazon.es | ≈ 35–45 € |
| Kit pigtails DT 200 pzas | https://www.fridayparts.com/200-pcs-deutsch-dt-connector-pigtail-kit | consultar |
| Crimpadora oficial Deutsch HDT-48-00 (contactos sólidos 12-16-20) | RS https://uk.rs-online.com/web/p/products/425973 (£463 + IVA; RS AT 556 € + IVA); Farnell IE https://ie.farnell.com/deutsch/hdt-48-00/crimp-tool-dt-hd-size-12-16-20/dp/1817060 ; Crimp Supply US$ 513 https://crimpsupply.com/deutsch-20-12-ga-production-crimp-tool-hdt-48-00.html | 500–670 € |
| Crimpadora económica para contactos sólidos DT (IWISS HD-2612D / JRready NEW-DT2 / iCrimp) | buscar "IWISS HD-2612D" o "JRready NEW-DT2" en Amazon.es; historial de precio https://www.pricebefore.com/iwiss-hd-2612d-solid-contacts-crimping-t54371.html | ≈ 40–70 € |
| Kit DTP/DTHD con HDT-48-00 (Buy Deutsch) | https://www.buydeutsch.com/collections/tools/products/dtp-dthd-gy-ck | US$ 698 |

Consejo: para pocos conectores, kit de 216 pzas con crimpadora de trinquete (contactos estampados) es suficiente; para contactos sólidos hace falta HDT-48-00 o clon de 4 indentaciones.

### D.3 Transceptores CAN para ESP32 (3,3 V)
| Pieza | Enlaces | Precio |
|---|---|---|
| Waveshare "SN65HVD230 CAN Board" (3,3 V, ESD, SKU 3945) | Waveshare https://www.waveshare.com/sn65hvd230-can-board.htm (US$ 4,99); Tinytronics NL https://www.tinytronics.nl/nl/communicatie-en-signalen/serieel/can-bus/sn65hvd230-can-board (4,75 €); Electrokit SE https://www.electrokit.com/en/can-bus-transceiver-sn65hvd230 (79 SEK); Eckstein DE https://eckstein-shop.de/sn65hvd230-can-board_1 ; Amazon.es: buscar "SN65HVD230 CAN módulo" (≈ 6–9 €/ud, packs de 3–5) | 5–9 € |
| TI SN65HVD230DR (chip SOIC-8, 3,3 V) | RS https://kr.rs-online.com/web/p/can-interface-ics/2184566P ; Mouser ES: buscar "SN65HVD230DR" (595-SN65HVD230DR) — Mouser devolvía 503 hoy; TI: https://www.ti.com/product/es-mx/SN65HVD230 | ≈ 2–3 € |
| NXP TJA1051T/3,118 (5 V alimentación, **E/S 3,3 V**, hasta 5 Mb/s, mejor inmunidad que SN65HVD230) | RS IT https://it.rs-online.com/web/p/interfacce-can-ci/2194672P (1,43 €/ud a 50 uds); Mouser ES: buscar "TJA1051T/3,118" (771-TJA1051T/3118) ≈ 1,2 US$; agregadores: https://www.oemstrade.com/search/tja1051t%2F3%2C118 | ≈ 1,2–1,5 € |
| Módulo TJA1051T/3 montado | buscar "TJA1051T/3 module 3.3V" en AliExpress/Amazon.es | 3–6 € |

Recomendación: en entorno de 24 V con mucho ruido (excavadora) usar **TJA1051T/3** (alimentación 5 V, TXD/RXD 3,3 V) con GND común y sin terminador adicional (el bus ya tiene 2×120 Ω).

### D.4 Caja estanca
- Caja ABS/PC IP67 ≈ 200×120×75 mm con tapa transparente u opaca: buscar "caja estanca IP67 ABS 200x120x75" en Amazon.es (≈ 12–20 €) o RS España (Hammond 1554/1555, Fibox PC, 20–40 €). Pasacables M16/M20 IP68 y prensaestopas para 2–6 mm (≈ 8 € / 10 uds). Para el conector Deutsch de entrada usar un DT de brida (DT04-12PA-L012 / "flange", kit 12 vías 14 AWG ≈ 20 US$ eBay https://www.ebay.com/p/1853334298).

---

## Lo que NO se ha podido confirmar (y qué hacer)
1. **Fabricante y nº de pieza de los conectores de 36 vías de la E-ECU (y de la EECU D12)** — DESCONOCIDO. Solución práctica: (a) pigtail SINOCMP 259 US$ (ya crimpado), (b) mazo motor 14512406 de desguace/aftermarket y cortar con cola, (c) leer el nº moldeado en la carcasa original y pedirlo a TE/Aptiv/distribuidor, (d) "repair terminal" por concesionario Volvo CE.
2. **Familia del conector JA/JB de la V-ECU** — DESCONOCIDO. Solución: pigtail eBay 164 US$ + envío, o mazo de cabina 14524053.
3. **Conector de la Resistor Box** — DESCONOCIDO; no es necesario para el proyecto.
4. **Nº de pieza del zócalo de la toma de servicio 8 pines** — no confirmado; y **la toma no lleva CAN** (PROBABLE), por lo que el acceso CAN debe hacerse en E-ECU B1/B2 o V-ECU JB13/JB14.

## Fuentes principales
- Kawasaki KDRDE5K hoja técnica: https://www.kawasakihydraulics.com/app/uploads/2019/10/Electric-Proportional-and-Directional-Pilot-Valves-Kawasaki-1.pdf ; página de producto https://www.kawasakihydraulics.com/product/kdrde5k-kwe5k/
- TE 174352-2: https://www.te.com/en/product-174352-2.html ; 174354-2: https://www.te.com.cn/chn-zh/product-174354-2.datasheet.pdf ; 173707-1: https://www.te.com/en/product-173707-1.html ; 173706-1: https://www.te.com.cn/chn-zh/product-173706-1.datasheet.pdf ; 1-172888-3: hoja Waldom/Zoro (arriba)
- SINOCMP E-ECU plug: https://sinocmp.com/products/volvo-controller-connector-plug-for-ec210-ec240-ec210b-ecu-60100000
- eBay V-ECU plug: https://www.ebay.com/itm/384979664114 ; https://www.ebay.de/itm/375584859654
- DrewLinQ Industry Connectors Reference (Volvo CE 8/14 pin): https://opusivs.com/wp-content/uploads/2023/12/DrewLinQ_Industry_Connectors_Reference_OpusBranded.pdf
- Volvo L120E "3 Electrical System" (Sch24/Sch31, toma IA/IB, E-ECU EA/EB): copia local `dl/L120E_MENY.pdf`
- Deutz EMR 2 System Description (25 polos, descarta EMR2): https://www.manualslib.com/manual/1706173/Deutz-Emr-2.html?page=25
- Unitech (Delphi): https://www.unitechelectronics.ca/volvo-ecm-20577135-p02-repair-tested-and-rebuilt/
- Duallane 62 vías EMS2 (descartado): https://www.duallane.com/volvo-engine-harness-gray-plug-housing-20429843
- Deutsch HDT-48-00: https://uk.rs-online.com/web/p/products/425973 ; DT en RS ES: https://es.rs-online.com/web/b/deutsch/
- Waveshare SN65HVD230: https://www.waveshare.com/sn65hvd230-can-board.htm ; TJA1051T/3 RS: https://it.rs-online.com/web/p/interfacce-can-ci/2194672P
