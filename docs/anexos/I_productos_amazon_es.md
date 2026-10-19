# Lista de compra en Amazon.es — controlador ESP32 (CAN J1939 rpm motor + relé "emergency speed") para excavadora Volvo 24 V

**Fecha de consulta:** 19-10-2026.
**Alcance (revisado):** sólo gestión de rpm del motor por CAN J1939 y un relé para conmutar la entrada de 24 V "emergency speed" de la E-ECU. La parte de válvula hidráulica queda aplazada: se han eliminado INA226, DAC 0–10 V, amplificador de válvula proporcional, conectores TE Econoseal y resistencias de potencia.
**Método:** Amazon.es bloquea la lectura automática de las fichas (página "fallback" sin precio o HTTP 503), así que los ASIN/URL se han verificado mediante resultados del buscador restringidos a `amazon.es`. Los precios marcados *según buscador* son los que aparecían en los fragmentos de búsqueda y pueden haber cambiado; donde no había precio visible se indica "no visible" y una estimación orientativa entre paréntesis. Todos los módulos son **pre-montados**. Los enlaces "enlace de búsqueda" (`/s?k=`) se dan sólo cuando no se ha podido verificar un ASIN.

> Ninguna ficha de Amazon es una hoja de datos: comprobar en cada una el chip real, la tensión de alimentación y el número de unidades del pack antes de comprar.

---

## 1. ESP32 DevKit V1 (ESP32-WROOM-32, 30 pines, USB) — PRIORITARIO

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| ESP32 DevKit V1 30 pines, pack 3 | Diymore – Set de 3 ESP32 (30 pines, versión estrecha, ESP-WROOM-32, compatible DevKit V1) | B0BY8J6VVM — https://www.amazon.es/dp/B0BY8J6VVM | no visible (≈ 20–25 € el pack) | Formato 30 pines "DevKit V1" (ancho 25,4 mm). Comprobar chip USB (CH340 en la mayoría de clones → driver CH340). |
| ESP32 DevKit V1 30 pines, pack 2 + 2 placas de bornes | ESP-32 WROOM-32 CH340 Type-C + ESP-32 DEVKIT V1 30PIN Power Boards (2 piezas) | B0D7MGPBD1 — https://www.amazon.es/dp/B0D7MGPBD1 | no visible (≈ 20–25 €) | **Incluye las placas de expansión de bornes de 30 pines del punto 2** (opción "todo en uno"). USB-C, CH340. |
| ESP32 DevKit V1 30 pines, pack 2 | Diymore 2 uds ESP32 Type-C, CH340, 30 pines | B0BS6R68H6 — https://www.amazon.es/dp/B0BS6R68H6 | no visible (≈ 15–18 €) | Idem. |
| Alternativa "de marca" (38 pines) | AZDelivery ESP32 NodeMCU Dev Kit C, CP2102 (1 ud / 3 uds) | B0821JM6J7 — https://www.amazon.es/dp/B0821JM6J7 (1 ud USB-C: B0D8WDDGC3) | 1 ud ≈ 11,99–13,99 €; 3 uds ≈ 25,99–27,99 € (según buscador) | **Es formato DevKitC de 38 pines**, no DevKit V1 de 30. Si se elige éste, la placa de bornes debe ser de 38 pines (diymore 3 uds 38 pines: B0CG8ZW8X5). Vendedor Prime. |

Enlace de búsqueda: https://www.amazon.es/s?k=ESP32+DevKit+V1+30+pines

## 2. Placa de expansión con bornes para ESP32 (30 pines) — PRIORITARIO

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Breakout bornes 30 pines | Ranuw ESP32 30 Pin Expansion Board / Shield DEVKIT-V1 Power Module | B0CLCQBX24 — https://www.amazon.es/dp/B0CLCQBX24 | no visible (≈ 8–12 €) | Bornes de tornillo para todos los GPIO + entrada de alimentación propia (5–12 V). Sólo para DevKit V1 **30 pines**. |
| Breakout bornes 30 pines, USB-C | ESP32 30 Pin Expansion Board DEVKIT-V1 Type-C | B0CN3YHJYF — https://www.amazon.es/dp/B0CN3YHJYF | no visible (≈ 8–12 €) | Igual, con USB-C auxiliar. |
| Breakout bornes 30 pines | UNFAIRZQ ESP32 30 Pin Expansion Board GPIO 30Pins | B0CH8C68BW — https://www.amazon.es/dp/B0CH8C68BW | no visible | Comprobar que el ancho de hilera coincide (30 vs 38 pines no son intercambiables). |
| Pack 2 uds | DUBEUYEW 2× ESP32 Breakout Board 30PIN | B0BP7NJ313 — https://www.amazon.es/dp/B0BP7NJ313 | no visible | Reseñas mencionan tornillos que se pasan de rosca: apretar con cuidado. |

## 3. Transceptor CAN 3,3 V — PRIORITARIO

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Waveshare SN65HVD230 CAN Board (original) | Waveshare SN65HVD230 Can Board, 3,3 V, protección ESD | B00KM6XMXO — https://www.amazon.es/dp/B00KM6XMXO | no visible (≈ 8–10 €; ficha 4,7★ / 165 valoraciones) | **Trae resistencia de terminación de 120 Ω soldada**: desoldarla si se conecta al bus J1939 de la máquina (ya terminado en ambos extremos). Alimentar a 3,3 V (no 5 V). Waveshare avisa de copias malas: comprar la ficha "Waveshare" o Luckfox. |
| SN65HVD230 (Luckfox oficial) | LUCKFOX SN65HVD230 CAN Communication Module 3,3 V | B0CNP17MCH — https://www.amazon.es/dp/B0CNP17MCH | no visible (≈ 8–10 €) | Misma placa, misma advertencia de 120 Ω. |
| SN65HVD230 genérico, pack 3 | Hailege 3 uds SN65HVD230 CAN Bus Transceiver | B0B1WW5XHV — https://www.amazon.es/dp/B0B1WW5XHV | ≈ 10–13 € el pack (según buscador) | Módulos "VP230": también llevan 120 Ω; verificar y quitar. J1939 va a 250 kbit/s: cualquiera sirve. |
| TJA1051 (CJMCU-1051), pack 2 | Youmile 2 uds CJMCU-1051 TJA1051 CAN Transceiver 3–5 V | B09TKZZT9M — https://www.amazon.es/dp/B09TKZZT9M (1 ud DollaTek: B07DK52YYG) | no visible (≈ 8–10 €) | Comprobar que el chip es **TJA1051T/3** (pin VIO para lógica 3,3 V); el TJA1051T "a secas" es lógica 5 V. El módulo se alimenta a 5 V. Comprobar si lleva 120 Ω. Más robusto en entorno vehículo que el SN65HVD230 (±40 V en bus). |

## 7. Módulo relé 1 canal, optoacoplado, disparo por nivel ALTO, compatible 3,3 V — PRIORITARIO (conmuta los 24 V al pin "emergency speed")

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Relé 1 canal 3 V/3,3 V, nivel alto, pack 6 | AYWHP 6 uds 3V Optocoupler Relay Module, High Level Trigger (EL817 + SRD-DC03V-SL-C) | B0DQL4SVN6 — https://www.amazon.es/dp/B0DQL4SVN6 | no visible (≈ 10–13 € el pack) | Contactos **10 A/250 VAC, 10 A/30 VDC**, NO/NC/COM en bornes → aptos para conmutar 24 V. La bobina de 3 V consume ≈ 120 mA: alimentar VCC desde el 3,3 V de la placa (no de un GPIO); la entrada IN va al GPIO a través del EL817. |
| Relé 1 canal 3 V, nivel alto, pack 5 | ARCELI 5 uds módulo relé 3 V aislamiento optoacoplador, disparo alto, para ESP | B0CLTZFWY4 — https://www.amazon.es/dp/B0CLTZFWY4 | no visible (≈ 9–12 €) | 10 A/30 VDC. Igual nota de consumo. |
| Relé 1 canal 3,3 V alto/bajo seleccionable | Módulo relé 3,3 V 1 canal alto/bajo ajustable (HUIMAIKEJI) | B07GD3F2QV — https://www.amazon.es/dp/B07GD3F2QV | no visible (≈ 5–7 €) | Contactos 10 A/28 VDC (al límite para 24 V + picos). Puente de selección H/L. |

> Nota: los módulos relé "24 V" (p. ej. B0H1LS1YB4, B0G6DBJYKP) tienen umbral de entrada 8,5–24 V: **no se disparan con 3,3 V**. Usar los de bobina 3 V de arriba alimentados desde el 3,3 V, o un módulo 5 V alimentado del DC-DC con disparo alto (muchos aceptan 3,3 V en IN, pero no está garantizado).

## 8. Módulo optoacoplador de entrada 24 V → 3,3 V (PC817, 4 canales) — PRIORITARIO (leer señales de 24 V de la máquina)

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Opto 4 canales PC817, pack 4 | ALMOCN 4 uds 4CH Optocoupler PC817 Isolation Board 3,6–30 V | B0B7D15YW5 — https://www.amazon.es/dp/B0B7D15YW5 | no visible (≈ 10–13 € el pack) | Entrada 3,6–24/30 V (vale para 24 V), salida 3,6–30 V → alimentar el lado de salida a 3,3 V. Salida ≈ 10 mA máx., ≤ 4 kHz. Comprobar inversión lógica de la salida. |
| Opto 4 canales PC817, 1 ud | ARCELI PC817 4 Channel Isolation Board 3,6–30 V | B07M78S8LB — https://www.amazon.es/dp/B07M78S8LB | no visible (≈ 5–7 €) | Igual. |
| Opto 4 canales PC817, pack 5 | Fasizi 5 uds PC817 4 Channel Optocoupler Isolation Board | B09Z2BP7SH — https://www.amazon.es/dp/B09Z2BP7SH | no visible | Igual. |
| Opto 4 bits 3,3 V ↔ 24 V (PLC) | 4 bit Optocoupler Isolator 3.3V to 24V PLC Signal Level Converter | B07Y8LNQ4M — https://www.amazon.es/dp/B07Y8LNQ4M | no visible (≈ 7–10 €) | Pensado justo para 24 V ↔ 3,3 V. |

## 9. Convertidor 24 V → 5 V para vehículo — PRIORITARIO

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Mean Well DDR-15G-5 (carril DIN, 9–36 V → 5 V/3 A) | MEAN WELL DDR-15G-5 DIN Rail Converter 5 V 3 A 15 W | B07B6553JY — https://www.amazon.es/dp/B07B6553JY (ficha alternativa "Original Mean Well DDR-15G": B091Y3TRZM) | no visible (≈ 25–30 €) | Aislado 4 kV, −40…+85 °C, cabe en la caja con carril DIN. **Entrada máx. 36 V**: añadir fusible 3 A y TVS (punto 10) aguas arriba. |
| Módulo automoción sellado 8–58 V → 5 V 3 A | DC-DC Converter Reductor 12/24/36/48 V → 5 V 3 A (GYVRM-K480503) | B07WSWMNN8 — https://www.amazon.es/dp/B07WSWMNN8 | no visible (≈ 10–15 €) | **Entrada 8–58 V** (mejor margen frente a transitorios de 24 V), no aislado, sellado, protección sobrecorriente/cortocircuito. Buena alternativa barata. |
| Módulo automoción sellado 9–35 V → 5 V 5 A | DROK DC-DC Buck 12/24 V → 5 V 5 A/25 W impermeable | B01851KJH4 — https://www.amazon.es/dp/B01851KJH4 | no visible (≈ 12–16 €) | **Entrada máx. 35 V**: poco margen; usar con TVS. |
| Módulo sellado 24 V → 5 V 5 A | Mumisuto DC-DC 12/24 V → 5 V 5 A 25 W, resina epoxi, −40…+85 °C | B09MTBF6NB — https://www.amazon.es/dp/B09MTBF6NB | no visible | Comprobar tensión máx. de entrada en la ficha. |
| Traco THN 10-4811WIR / TEN 5-4811WI (fuera de Amazon) | No existe el sufijo "WIR" en Mouser/RS/TME. Equivalentes 18–75 V → 5 V/2 A: **THN 10-4811WIR** RS España ref. 200-3456 ≈ 372,58 €/tubo de 10 (≈ 37 €/ud) https://es.rs-online.com/web/p/convertidores-dc-dc/2003456 ; TMR 10-4811WIR (RS UK £22,53; TME https://www.tme.eu/es/details/tmr10-4811wir/); TEN 5-4811WI (1 A) en TME https://www.tme.eu/es/details/ten5-4811wi/ (NRND → sustituto TDN 5-4811WI) | — | ≈ 25–37 €/ud | Entrada 18–75 V: la opción más robusta frente a picos de la red de 24 V. Sólo si se quiere "grado industrial". |
| Mean Well DDR-30G-5 | **No en amazon.es**; TME sin stock; RS ES sólo RSD-30G-5 (chasis) 46,01 € + IVA https://es.rs-online.com/web/p/convertidores-dc-dc/1408098 | — | — | El DDR-15G-5 (3 A) sobra para ESP32 + OLED + módulos. |

## 10. Diodo TVS SMCJ33A — sólo nota

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| SMCJ33A pack 40 | IDUTQUMW SMCJ33A (40 uds, SMC) | B0D1QHP3N8 — https://www.amazon.es/dp/B0D1QHP3N8 | no visible (≈ 6–9 €) | Marca genérica. Alternativa de marca: RS España Littelfuse SMCJ33A ref. 166-3683 (≈ 0,20 €/ud en bobina) https://es.rs-online.com/web/p/diodos-tvs/1663683 ; Farnell ES Diodes SMCJ33A-13-F 0,551 €/ud https://es.farnell.com/diodes-inc/smcj33a-13-f/diodo-tvs-unidir-33v-1-5kw-do/dp/3405097 ; Mouser ES https://www.mouser.es/ProductDetail/Vishay-Semiconductors/SMCJ33A . Vclamp ≈ 53 V: protege de surges pero no limita por debajo de los 36 V máx. del DDR-15G-5 (si se quiere eso, SMCJ30A o el módulo de 8–58 V). Es SMD: montarlo en los bornes del DC-DC con un trozo de cable o usar versión axial (P6KE33A / 1.5KE33A). |

## 11. Portafusibles en línea + fusibles de cuchilla 3 A

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Portafusibles en línea ATC/ATO, pack 5 | 5 portafusibles en línea ATC/ATO (+5 fusibles 35 A) | B09HL97VRQ — https://www.amazon.es/dp/B09HL97VRQ | no visible (≈ 8–10 €) | 12 V nominal / 32 V máx. Los fusibles incluidos son de 35 A: comprar 3 A aparte. |
| Portafusibles en línea estanco | Caja portafusibles cuchilla en línea 1–35 A, 12–32 V, impermeable | B0B59P7TXY — https://www.amazon.es/dp/B0B59P7TXY | no visible (≈ 6–8 €) | Apto 32 V. |
| Portafusibles + fusible (elegir 3 A) | Caja portafusibles estándar con cubierta, 2 A…40 A seleccionable | B0CRP52QXK — https://www.amazon.es/dp/B0CRP52QXK | no visible | Elegir variante "3A". |
| Surtido fusibles 2–35 A (120 uds) | Kit fusibles cuchilla estándar 2A/3A/5A/7,5A…35A | B0GP66MPRW — https://www.amazon.es/dp/B0GP66MPRW | no visible (≈ 8–12 €) | Incluye 3 A. |

## 12. Encoder rotativo KY-040 con botón

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| KY-040 pack 5 | WayinTop 5 uds Rotary Encoder KY-040 360° con pulsador | B07T3672VK — https://www.amazon.es/dp/B07T3672VK | ≈ 6–25 € según pack (según buscador) | Funciona a 3,3 V. Añadir 100 nF en CLK/DT/SW para antirrebote. |
| KY-040 con capuchón, pack 5 | cylewet 5 uds KY-040 15×16,5 mm con knob (CYT1062) | B06XQTHDRR — https://www.amazon.es/dp/B06XQTHDRR | no visible (≈ 8–10 €) | Incluye **knob**. |
| KY-040 (AZDelivery, Prime) | AZDelivery KY-040 Rotary Encoder Module | B082PYB3JN — https://www.amazon.es/dp/B082PYB3JN | no visible (≈ 5–7 €) | Sin knob (comprar knob eje D 6 mm aparte). |

## 13. OLED 0,96" SSD1306 I²C 128×64

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| OLED 0,96" SSD1306 I2C (AZDelivery, 1 ud) | AZDelivery 0,96" OLED Display I2C SSD1306 128×64 blanco | B01L9GC470 — https://www.amazon.es/dp/B01L9GC470 (multipack: B082M8VWLT) | no visible (≈ 7–9 €) | 3,3–5 V, dirección 0x3C. Prime. |
| OLED 0,96" pack 2 | TECNOIOT 2 uds OLED 128×64 I2C SSD1306 azul | B07JN2NHT4 — https://www.amazon.es/dp/B07JN2NHT4 | no visible (≈ 9–12 €) | La ficha menciona SSD1309 en un punto: **comprobar el controlador** (SH1106 necesita otra librería). |

## 14. Caja estanca IP65 ≈ 200×120×75 mm + prensaestopas M16/M20 IP68

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Caja ABS IP65 200×120×75 (tapa opaca) | Yanmis Caja de Conexiones ABS IP65 200×120×75 mm con accesorios | B07RQ5TRHK — https://www.amazon.es/dp/B07RQ5TRHK | ≈ 6–24 € (según buscador, rango de la familia) | ABS ignífugo, con junta y tornillos. |
| Caja ABS IP65 200×120×75 (blanca) | Tyenaza Outdoor Waterproof Box IP65 ABS 200×120×75 mm | B09BQN68M5 — https://www.amazon.es/dp/B09BQN68M5 | no visible (≈ 12–18 €) | Igual. |
| Caja 200×120×75 con bisagra + carril + prensaestopas PG13.5 | Caja Estanca Exterior "IP68" 200×120×75, 2 in 3 out | B0BRTMJXW4 — https://www.amazon.es/dp/B0BRTMJXW4 | no visible (≈ 18–24 €) | La ficha mezcla IP65/IP68: tratar como IP65. Trae carril guía (útil para el DDR-15G-5 y bornes DIN) y prensaestopas PG. |
| Caja tapa transparente (más grande) | Caja IP65 tapa transparente 276×150×87 mm | B0848Q8CQS — https://www.amazon.es/dp/B0848Q8CQS | no visible (≈ 20–25 €) | No se verificó ASIN de 200×120×75 con tapa transparente: enlace de búsqueda https://www.amazon.es/s?k=caja+estanca+IP65+200x120x75+tapa+transparente |
| Prensaestopas IP68 M12/M16/M20/M25 (32 uds) | ARPDJK 32 uds prensaestopas nylon IP68 3–15 mm con contratuerca | B07XF88KP9 — https://www.amazon.es/dp/B07XF88KP9 | no visible (≈ 12–15 €) | 8 de cada tamaño. |
| Prensaestopas IP68 (42 uds, 12×M16 + 12×M20) | Caianwin 42 Pack Cable Glands IP68 M12 M16 M20 M25 (PA66) | B0CYLPM7T7 — https://www.amazon.es/dp/B0CYLPM7T7 | no visible (≈ 14–18 €) | — |
| Sólo M16 (20 uds) | TEKONDA DLJT-M16 20 uds M16 IP68 4–8 mm, −40…+100 °C | B0CNGD4TT8 — https://www.amazon.es/dp/B0CNGD4TT8 | no visible (≈ 10 €) | Para cables de 4–8 mm. |

## 15. Kit conectores Deutsch DT + crimpadora (OPCIONAL)

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Kit DT 2/3/4/6/8/12 vías + crimpadora | JRready Deutsch DT Connector Crimp Tool Kit (DW5008-01) con ACT-HDT-16DT, contactos sólidos #16, 16–20 AWG | B0D942SYV3 — https://www.amazon.es/dp/B0D942SYV3 | rango de la familia 46–218 € (según buscador) | Crimpadora de 4 indentaciones (la correcta para contactos sólidos). |
| Kit DT 604 piezas + crimpadora | JRready DT Connector Kit 604 PCS con ACT-M202 | B0D2KB2RP6 — https://www.amazon.es/dp/B0D2KB2RP6 | no visible (≈ 100–130 €) | ACT-M202 cubre 12–22 AWG. |
| Kit DT 188 piezas (sin crimpadora) | IWISS 188 PCS Deutsch DT Gray Connector Kit, contactos sólidos #16 | B098SZZX8Z — https://www.amazon.es/dp/B098SZZX8Z | no visible (≈ 45–60 €) | Necesita crimpadora de 4 indentaciones. 13 A máx. |
| Kit DT 416 piezas + crimpadora + extractor | Deutsch DT 416 pcs Connector Kit con crimpadora 14–20 AWG y extractor | B0C8JVY732 — https://www.amazon.es/dp/B0C8JVY732 | ≈ 218 € (según buscador) | El más completo. |
| Kit DT 338 piezas (económico) | yomoe Kit Conectores DT Deutsch 338 piezas con crimpadora y extractor | B0D2MQXPSG — https://www.amazon.es/dp/B0D2MQXPSG | no visible (≈ 60–80 €) | Genérico: comprobar que la crimpadora es de 4 indentaciones. |

## 16. Crimpadora para terminales abiertos 0,5–1,5 mm² (OPCIONAL)

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Engineer PA-21 | Engineer PA-21 universal crimping tool (Japón) | B002L6HJ8W — https://www.amazon.es/dp/B002L6HJ8W | ≈ 42,99 € (según buscador) | No es de carraca, pero es la mejor para terminales open-barrel 18–26 AWG (Dupont, JST, terminales de automoción pequeños). |
| IWISS SN-28B (carraca) | iCrimp/IWISS SN-28B Ratcheting Crimper Dupont/JST | B01A0SAQ3W — https://www.amazon.es/dp/B01A0SAQ3W | no visible (≈ 20–25 €) | 0,1–1,0 mm² (28–18 AWG). |
| IWISS IWS-2820M (carraca) | IWISS IWS-2820M Mini Open Barrel Crimp Tool AWG 28–20 | B078WNZ9FW — https://www.amazon.es/dp/B078WNZ9FW | no visible (≈ 25–30 €) | 0,08–0,5 mm²; sólo JST/Molex pequeños, **no para 1–1,5 mm²**. |

## 18. Cable FLRY, termorretráctil adhesivo, tubo corrugado

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| FLRY-B 0,5 mm², 5 colores × 5 m | AUPROTEC Vehicle Cable 0,50 mm² 5 colores set 5 m FLRY-B | B01FHCER9U — https://www.amazon.es/dp/B01FHCER9U | no visible (≈ 12–15 €) | DIN 72551/ISO 6722, Ø 1,4–1,6 mm, −40…+105 °C. Para CAN usar par trenzado (trenzar a mano 2 colores) o cable CAN apantallado. |
| FLRY-B 1 mm² (por color, 5 m) | Cable automoción FLRY-B 1 mm² (colores seleccionables) | B078ZTPX2L — https://www.amazon.es/dp/B078ZTPX2L | no visible (≈ 4–6 €/color) | Para +24 V/GND. Alternativa 10 m: https://www.amazon.es/s?k=FLRY-B+1mm%C2%B2 |
| FLRY-B 0,5 mm² 10 m negro | 10 m cable vehículo FLRY-B 0,5 mm² negro | B088X2N9X7 — https://www.amazon.es/dp/B088X2N9X7 | no visible (≈ 5 €) | — |
| Termorretráctil 3:1 con adhesivo, surtido | ISOLATECH 142 piezas 3:1 negro/rojo con pegamento interior (8,3 m) | B088QK1BG5 — https://www.amazon.es/dp/B088QK1BG5 | no visible (≈ 12–15 €) | Doble pared, sellado estanco. |
| Termorretráctil 3:1 adhesivo, 400 piezas | Eventronic 400 piezas termorretráctil 3:1 impermeable con adhesivo | B0B48C59G7 — https://www.amazon.es/dp/B0B48C59G7 | no visible (≈ 15–20 €) | — |
| Tubo corrugado abierto 13 mm | Tubo corrugado flexible abierto Ø 13 mm para cableado coche | B00I04AAV2 — https://www.amazon.es/dp/B00I04AAV2 | ≈ 1,33 €/m (según buscador) | — |
| Tubo corrugado abierto NW10, 10 m | Kalitec tubo corrugado ranurado NW10 abierto 10 m (AD 12,7 / ID 10 mm) | B08M6FDVRN — https://www.amazon.es/dp/B08M6FDVRN | no visible (≈ 10–12 €) | PP modificado, −40…+150 °C. También NW16. |
| Tubo corrugado cerrado 10 mm, 5 m | AUPROTEC tubo corrugado sin ranura Ø int. 10 mm, 5 m, UV | B00VJYZ4XY — https://www.amazon.es/dp/B00VJYZ4XY | no visible (≈ 8 €) | — |

## 19. Fuente de banco 24 V ≥ 2 A

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Fuente carril DIN 24 V 5 A | Mean Well NDR-120-24 (120 W, 24 V, 5 A) | B07BFCCPVB — https://www.amazon.es/dp/B07BFCCPVB | ≈ 28 € (según buscador) | Salida ajustable 24–28 V; sin limitación de corriente ajustable (hiccup). Ideal como "red de 24 V" de pruebas en el banco. |
| Fuente carril DIN 24 V 2,5 A | Mean Well HDR-60-24 (60 W, 24 V, 2,5 A) | B06XWRLCDJ — https://www.amazon.es/dp/B06XWRLCDJ | no visible (≈ 20–25 €; HDR-30-24 ≈ 16,60 €) | Compacta. |
| Fuente de laboratorio 0–30 V / 0–5 A | RUZIZAO 30 V 5 A 150 W con encoder, 3 dígitos | B0C6K4LDV3 — https://www.amazon.es/dp/B0C6K4LDV3 | ≈ 40 € (según buscador) | **Limitación de corriente ajustable** (protege la electrónica en las primeras pruebas). Reseña ES: protección de cortocircuito "regular". |
| Fuente de laboratorio 0–30 V / 0–5 A (más seria) | MC POWER LBN-305, ajuste fino/grueso, limitación de corriente | B00XIP3X9E — https://www.amazon.es/dp/B00XIP3X9E | no visible (≈ 70–90 €) | — |

## 20. Adaptador USB-CAN para PC — ESENCIAL (sniffing J1939 y validación)

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| **Opción A (recomendada): CANable Pro aislado (ADM3053)** | DKSooozs CANable USB-CAN Candlelight ADM3053 versión aislada CANABLE Pro | B0CP29RZRP — https://www.amazon.es/dp/B0CP29RZRP (mismo producto con otras marcas: B0C4TN3KXH, B0CHR9FSTT, B0CSYPGZMW) | no visible (≈ 25–35 €) | Aislamiento 2500 V (importante en máquina). Firmware candleLight (gs_usb → SocketCAN nativo en Linux, sin drivers; en Windows con Cangaroo/SavvyCAN/python-can). Puente para 120 Ω: **desactivar** al conectarse al bus de la máquina. |
| **Opción B: DSD TECH (CANable con soporte)** | DSD TECH SH-C30A USB to CAN Adapter, open hardware Canable | B0BQ5G3KLR — https://www.amazon.es/dp/B0BQ5G3KLR (versión cable SH-C30L: B0G387Y3J9; aislado + CAN-FD SH-C31G: B0FHHCSZY8) | no visible (SH-C30A ≈ 25–30 €; SH-C31G ≈ 40–50 €) | Marca con documentación y librería Python. Reseña: el SH-C31G puede necesitar flashear slcan para Cangaroo en Windows. |
| **Opción C: Innomaker USB2CAN (aislado, muy bien soportado en Linux/Windows)** | InnoMaker USB to CAN Converter (1 canal, 3000 V aislamiento, DB9, 20 kbps–1 Mbps) | B0956NV6CM — https://www.amazon.es/dp/B0956NV6CM (otra ficha 1 canal: B07Q812QK8; versión cable USB2CAN-C basada en CANable: B09K3LL93Q; doble canal USB2CAN-X2: B09FLQM7QH) | ≈ 33–81 € según modelo (según buscador) | SocketCAN automático en Linux, driver Windows oficial, modos normal/silencioso/loopback (el **modo silencioso** es ideal para escuchar J1939 sin perturbar). Terminación 120 Ω por jumper. Adaptador DB9→bornes de Innomaker: B0BD7CDQ31. Alguna ficha de 1 canal aparece sin stock: comprobar. |
| Opción D: CANable V2.0 (CAN-FD) | CANABLE V2.0 S PRO USB to CAN Adapter CANFD slcan/SocketCAN/CANdleLight | B0DP9N6TB8 — https://www.amazon.es/dp/B0DP9N6TB8 (MKS CANable V2 Pro: B0FWBDT6Q1) | no visible (≈ 20–30 €) | No aislado (V2.0 S); CAN-FD no hace falta para J1939. |
| Opción E: CANable no aislado (TJA1051T/3) | Bluerare CANable USB-CAN Candlelight TJA1051T/3 no aislado | B0CJR7VZ8V — https://www.amazon.es/dp/B0CJR7VZ8V (equiv. B0C1RFZBVD) | no visible (≈ 15–20 €) | El más barato; sin aislamiento galvánico. |
| PEAK PCAN-USB (IPEH-002021/002022) | **Sólo clones "compatibles"** en amazon.es (p. ej. B0D56TM41P, B0F4PD7WKW, B0D56SGV2B) | https://www.amazon.es/dp/B0D56TM41P | ≈ 237 € y más (según buscador; fichas incoherentes) | **No recomendado**: no son PEAK originales; el PCAN-USB genuino (≈ 200–250 € + IVA) se compra en PEAK-System o distribuidores (RS/Farnell). Para este proyecto un CANable aislado basta. |
| "USB-CAN Analyzer" chino (CH340, COM virtual) | Q-BAIHE / Garosa USB to CAN Analyzer | B017N7YEAO — https://www.amazon.es/dp/B017N7YEAO (B07XQ3MJFK) | no visible (≈ 15–25 €) | No es SocketCAN; software Windows propio (reseñas: inestable a 1 Mbps). Funciona con python-can (driver "seeedstudio"). Sólo como última opción. |

## 21. Extractores de terminales + bornes carril DIN

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Kit extractores 76 piezas | 76pcs Terminal Removal Tool Kit (Hossom) | B0C16VB4DG — https://www.amazon.es/dp/B0C16VB4DG | ≈ 15,19 € (según buscador); 3,8★ (57) | 28 simples + 30 dobles + 18 de carcasa. |
| Kit extractores 70 piezas | Kit extracción terminales coche 70 piezas con expulsor de clavijas | B0927B29TG — https://www.amazon.es/dp/B0927B29TG | no visible (≈ 15–18 €) | — |
| Bornes carril DIN tornillo UK-2.5B (kit) | Kit bornes carril DIN UK-2.5B con carril, topes y puentes | B07Y7BCRST — https://www.amazon.es/dp/B07Y7BCRST | no visible (≈ 12–18 €) | 600 V, 2,5 mm². |
| Bornes carril DIN push-in (kit 10 uds) | CTRICALVER Kit bornes push-in verdes 10 uds con carril, marcador y puentes 2/3/4/5P | B0BF9VCML2 — https://www.amazon.es/dp/B0BF9VCML2 | no visible (≈ 15–20 €) | Push-in 0,08–4 mm² (ideal para FLRY). |
| Bornes 1 entrada / 2 salidas (ST2.5-TWIN) | SRJQXH DIN Rail Terminal Block one-in-two-out ST2.5TWIN con carril 20 cm | B0BJZ8SQFX — https://www.amazon.es/dp/B0BJZ8SQFX | no visible (≈ 15 €) | Para distribuir +24 V / GND. |

## 22. Relé 12/24 V de automoción para conmutar 24 V sobre una línea de señal (NUEVO)

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| **Opción preferente: el mismo módulo del punto 7** | AYWHP 6 uds relé 3 V opto, nivel alto (B0DQL4SVN6) o ARCELI 5 uds (B0CLTZFWY4) | https://www.amazon.es/dp/B0DQL4SVN6 | ≈ 10–13 € el pack | Contactos 10 A/30 VDC, NO/NC: conmuta los 24 V al pin "emergency speed" directamente desde el ESP32 (3,3 V). Lo más simple y aislado por opto. |
| Relé automoción 24 V SPDT 5 pines con base precableada (pack 3) | Aiqeer 3 uds relé coche 5 pines 24 V 40 A SPDT con base de arnés | B0CKYHZLTS — https://www.amazon.es/dp/B0CKYHZLTS | no visible (≈ 12–15 €) | Relé "de máquina" (87/87a/30/85/86) si se prefiere algo robusto montado fuera de la caja. **Bobina 24 V (≈ 70–100 mA): no se excita desde el ESP32** → gobernarlo con el módulo relé 3 V del punto 7 o un módulo opto/MOSFET. |
| Relé automoción 24 V 20/10 A 5 pines | Partuto relé multiusos 24 V 20/10 A 5 pines | B0DB2FRNMH — https://www.amazon.es/dp/B0DB2FRNMH | no visible (≈ 6–8 €) | Igual nota. Base aparte: B0GYX3MNXQ. |
| Módulo relé 1 canal 24 V opto (alto/bajo) | Módulo relé 24 V 1 canal optoacoplado H/L (p. ej. B0H1LS1YB4, Helilyco 10 uds B0G6DBJYKP) | https://www.amazon.es/dp/B0H1LS1YB4 | no visible (≈ 5–8 €) | Umbral de entrada 8,5–24 V: **no sirve para disparo directo desde 3,3 V**; sólo si la señal de mando ya es de 24 V. |

## 23. Sondas back-probe / pines de prueba para conectores (NUEVO)

| Artículo | Producto en Amazon.es | ASIN / URL | Precio aprox. | Notas |
|---|---|---|---|---|
| Kit 92 piezas cables de prueba automoción (incluye agujas back-probe) | Vomeko Kit de Cables de Prueba de multímetro 92 piezas, diagnóstico automotriz | B0DJT9HMGK — https://www.amazon.es/dp/B0DJT9HMGK (equiv. B0BVFSVSZW, B0CLH58SGS) | no visible (≈ 25–35 €) | Agujas back-probe, puentes 1:1 para conectores, cocodrilos, banana 4 mm. Lo más completo para pinchar el conector de la E-ECU sin dañarlo. |
| Sondas de aguja 2 mm (par) | DIKACA puntas de prueba 2 mm sonda automotriz sin daño (2 uds) | B0G4LD1FM8 — https://www.amazon.es/dp/B0G4LD1FM8 | no visible (≈ 8–12 €) | Punta ≈ 1 mm, conector 2 mm (puede requerir adaptador 2→4 mm para el multímetro). |
| Sondas perforadoras con clip 4 mm (P5010) | Leopacat P5010 4 mm clips perforadores de aislamiento | B0CR484WL4 — https://www.amazon.es/dp/B0CR484WL4 | no visible (≈ 10–15 €) | Perforan el aislamiento: sellar después con termorretráctil adhesivo; preferir back-probe en el conector. |
| Set accesorios multímetro (ganchos, cocodrilos, puntas) | AstroAI 8 accesorios cables de prueba | B0H72WX5XT — https://www.amazon.es/dp/B0H72WX5XT | no visible (≈ 12–15 €) | Complemento (30 VAC/60 VDC, 19 A). |

Enlace de búsqueda: https://www.amazon.es/s?k=sondas+back+probe+automoci%C3%B3n

---

## Presupuesto estimado (lista reducida)

Precios orientativos (IVA incl.) a 19-10-2026; la mayoría sin precio verificado en la ficha, estimados por rangos habituales de amazon.es.

| Bloque | Artículos | Estimación |
|---|---|---|
| Núcleo electrónico | 1 ESP32 (pack 2–3) · 2 breakout bornes · 3 transceptor CAN (×2) · 7 módulos relé (pack) · 8 opto 4 ch · 9 DC-DC (DDR-15G-5 o módulo sellado) · 10 TVS · 12 encoder · 13 OLED | **≈ 100–140 €** |
| Instalación en máquina | 11 portafusibles + fusibles · 14 caja IP65 + prensaestopas · 18 cable FLRY + termorretráctil + corrugado · 21 bornes DIN + extractores · 22 relé automoción con base | **≈ 110–160 €** |
| Herramientas de diagnóstico (esenciales) | 20 USB-CAN aislado (CANable Pro o Innomaker) · 23 kit back-probe · 19 fuente 24 V (NDR-120-24 o lab 30 V/5 A) | **≈ 85–150 €** |
| **Subtotal sin opcionales** | | **≈ 295–450 €** |
| Opcionales | 15 kit Deutsch DT con crimpadora (46–130 €) · 16 Engineer PA-21 (≈ 43 €) o SN-28B (≈ 22 €) | **+ 70–175 €** |
| **Total con opcionales** | | **≈ 365–625 €** |

Notas de presupuesto:
- La elección más cara dentro del núcleo es el DC-DC: DDR-15G-5 (≈ 25–30 €) frente al módulo sellado 8–58 V (≈ 10–15 €); si se opta por Traco en RS (≈ 37 €/ud, tubo de 10 → 372 €) el total sube notablemente, no se recomienda para una unidad.
- Si ya se dispone de multímetro con puntas y de una fuente de 24 V, el bloque de diagnóstico baja a ≈ 30–50 € (sólo el USB-CAN).
- Comprar en packs (ESP32 ×3, CAN ×3, relés ×5–6) da repuestos a coste casi nulo; es lo que asumen los rangos.
