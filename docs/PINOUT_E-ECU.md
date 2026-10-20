# Pinout de la E-ECU Volvo 03161983 (D6D EAE2) y conexión al ESP32

Diagrama: [`pinout_E-ECU_conector_B_ESP32.svg`](pinout_E-ECU_conector_B_ESP32.svg) · [`.png`](pinout_E-ECU_conector_B_ESP32.png)

**Fuentes**
- Circuito OEM "EECU Electric Circuit (EC160B/180B/210B/240B/290B)", boletín Volvo CE UPDATE EC160B~460B (`esquemas/d12_EC210B_EECU_electric_circuit_EC160B-290B-07.png`) — **ALTA**, es exactamente esta E-ECU.
- Tablas "EECU/EA" y "EECU/EB Connector" del manual Volvo Trucks *Vectro II*, PV776-144528 (`esquemas/d12_VectroII_EECU_connector_EA_pinout_D12B-C-024.png`, `…EB_pinout_D12B-C-025.png`) — **ALTA** para la familia de hardware; las funciones de camión se dan como referencia y coinciden en todos los pines que la excavadora usa.
- Esquema L120E SCH31 (misma E-ECU): colores de cable del conector EB — **ALTA**.

**Disposición física** (dibujo W3000945 del manual Volvo): tres filas de 12 cavidades, pestaña de cierre arriba; **fila superior 1–12, fila central 13–24, fila inferior 25–36**, numeradas de izquierda a derecha. Conector **A = negro** (motor), **B = rojo** (máquina). Confirmar con los números moldeados en el conector real.

---

## 1. Conector B (rojo, lado máquina)

| Pin | Función en la excavadora (OEM EC210B) | Función en camión D12 (referencia) | Color (L120E / camión) | Uso en el proyecto |
|---|---|---|---|---|
| **1** | **J1939 CAN H** | Data link J1939 CAN HI | amarillo (Y) | **→ CANH del transceptor** |
| **2** | **J1939 CAN L** | Data link J1939 CAN LO | verde (GN) | **→ CANL del transceptor** |
| 3 | Temperatura de aire de admisión | Ambient air temperature | BL/Y | no tocar |
| **4** | **Emergency speed control** (24 V = régimen alto) | Buffered idle validation switch (< 4 V ralentí, > 8 V acelerado) | rosa (P) | opcional: leer con divisor → GPIO35 |
| 5 | Retorno de la bobina de precalentamiento | Preheat sense 1 | R / GN | no tocar |
| 6 | — | no usado | | |
| 7 | Nivel de refrigerante | Coolant level warning | BL/SB | no tocar |
| 8 | Común (−) de nivel de refrigerante / sensor de admisión | Air filter, coolant level common | GR/W | no tocar |
| **9** | **Masa** | Ground (−) | blanco (W) / SB-W | **→ GND común del ESP32** |
| **10** | **Masa** | Ground (−) | blanco (W) / SB-W | (mismo nodo que 9) |
| **11** | **+24 V** (desde relé R3 "EMS power", F15 20 A) | Power supply (+) | R/SB · R/W | solo referencia; **no alimentar el ESP32 aquí** |
| **12** | **+24 V** | Power supply (+) | R/SB · R/W | ídem |
| 13 | Sensor de admisión (temperatura, común) | Ambient air temp common (−) | VO/W | no tocar |
| 14–16 | — | 14–15 no usado; 16 preheat sense 2 | | |
| 17 | Presión de admisión | Air filter indicator | BL/R | no tocar |
| 18–23 | — | 21 cooling fan control; resto no usado | | |
| 24 | Línea a la toma de servicio / programación de fábrica | Factory programming (EOL) | Y/SB | **nunca conectar** |
| **25** | **J1708 / J1587 A (+)** | Data link J1708 (+) | gris (GR) | no necesario (diagnóstico) |
| **26** | **J1708 / J1587 B (−)** | Data link J1708 (−) | naranja (OR) | no necesario |
| 27–30 | — | no usado | | |
| 31 | Relé de precalentamiento (masa de la bobina del relé) | Preheat relay coil ground | BL/R | no tocar |
| 32–34 | — | no usado | | |
| 35–36 | — | EPG1 / EPG2 control (freno motor, camión) | | |

Observaciones:
- **No hay pin de llave/contacto.** La E-ECU se alimenta por el relé R3 y recibe la posición de la llave **por J1939 desde la V-ECU**. Es una de las cosas que un emulador completo de V-ECU tendría que enviar.
- **Terminación interna confirmada:** B1–B2 en la E-ECU suelta = **117 Ω** (medido en el taller, 2026-10-20).
- Sin V-ECU en el bus, la E-ECU registra **SID 231 / PSID 201** (pérdida de comunicación con la V-ECU) y usa la entrada B4 como "limp home".

## 2. Conector A (negro, lado motor) — solo para referencia, no se toca

| Pin | Función (camión D12; la excavadora coincide en lo dibujado) |
|---|---|
| 1 | Temperatura de aceite |
| 2 | Temperatura de sobrealimentación |
| 3 | Presión de sobrealimentación |
| 4 | Común (+) presión aceite/sobrealimentación |
| 5 | Común (−) sensores de presión y temperatura |
| 7 / 18 | Sensor de posición árbol de levas (+ / −) |
| 11, 22, 23 | Inyectores cil. 1, 2, 3 (−) |
| 12 | Común inyectores 1–3 (**+90 V**) |
| 13 | Temperatura de combustible |
| 14 | Presión de aceite |
| 24 | Común inyectores 4–6 (**+90 V**) |
| 25 | Temperatura de refrigerante |
| 30 / 31 | Sensor de régimen cigüeñal (+ / −) |
| 34, 35, 36 | Inyectores cil. 4, 5, 6 (−) |

> Los pines de inyector llevan **90 V**: no medir ni conectar nada en el conector A con el motor en marcha.

---

## 3. Conexión al ESP32

| Señal | Conector B | ESP32 / módulo | Notas |
|---|---|---|---|
| CAN H | **B1** (amarillo) | CANH del **CAN Pal** (TJA1051T/3) | H y L trenzados, derivación < 1 m |
| CAN L | **B2** (verde) | CANL del CAN Pal | **Interruptor de terminación del CAN Pal en OFF** (con un SN65HVD230, quitar su resistencia de 120 Ω) |
| Masa del CAN | **B10** (o B9) | Borne GND del CAN Pal | Va en el mismo cable que H/L (3 hilos): referencia común con la E-ECU |
| CAN TX / RX / SLNT | — | **G17** → TX · **G18** ← RX · **G4** → SLNT | Transceptor a 3,3 V; SLNT en alto = silencio por hardware (firmware por defecto) |
| Masa de la placa ESP32 | mismo punto que la E-ECU (B9/B10 o perno de chasis junto a la E-ECU) | Borne GND de la placa | Masa única; no alimentar otros equipos desde B9/B10 |
| Estado emergencia (opcional) | **B4** | Optoacoplador 24 V → 3,3 V, OUT1 → **G35** | Solo lectura; alternativa: divisor 100 kΩ / 10 kΩ + Zener 3,3 V |
| +24 V | **no** desde B11/B12 | Borne VCC de la placa ESP32_Relay X1 desde +24 V tras la llave (JB7/JB8 del mazo V-ECU o caja de fusibles) con fusible de 3 A | B11/B12 solo viven con el relé R3 activo |
| J1708 | B25 / B26 | no se conecta | Solo diagnóstico/VCADS; si hiciera falta, MAX3485 a 9600 baud |

**Dónde pinchar el CAN, por orden de preferencia**
1. **Mazo de la V-ECU (conector JB)**: **JB14 (H) / JB6 (L)** — es donde irá el ESP32 de todos modos (válvula, alimentación). Es una derivación del mismo par que llega a B1/B2 y al panel. **JB13 y JB5 son las mallas** de los cables J1587 y J1939: no tocarlas ni puentearlas con CAN.
2. **Conector B de la E-ECU (B1/B2)**: con un pigtail en "Y"; es el punto más cercano al motor y el único imprescindible si no se usa el mazo de la V-ECU.
3. Panel 21C1/21C2.

**Comprobaciones antes de conectar**
1. Batería desconectada. Verificar colores (B1 amarillo, B2 verde) y numeración moldeada.
2. Resistencia B1–B2 con la E-ECU montada: ≈60 Ω con las dos terminaciones (E-ECU y panel); ≈120 Ω si el panel de esta máquina (MDU) no termina el bus → poner la terminación del CAN Pal (o del SH-C30A) en ON. Sin V-ECU el bus no se parte: no hay que puentear nada.
3. Con contacto: tensión CAN H ≈2,5–3,5 V y CAN L ≈1,5–2,5 V respecto a masa (reposo ≈2,5 V).
4. Firmware v0.1 (entorno `esp32dev`): TWAI en `LISTEN_ONLY` a 250 kbit/s y SLNT en alto: debe recibir EEC1 (ID `0x0CF00400`) cada 20 ms con el motor en marcha.
5. Nunca transmitir con la V-ECU original conectada; nunca aplicar tensión a B4, B24 ni a pines de sensores.
