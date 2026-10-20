# Captura del bus J1939 con el portátil

Fase 1 de [`CONTROL_RPM.md`](CONTROL_RPM.md): **escuchar** el bus CAN de la máquina, sin transmitir nada, para saber qué publica la E-ECU, qué averías marca sin V-ECU y cuánto par da con y sin carga. Con esos datos se ajusta el auto-ralentí y se decide si se puede probar TSC1 (regulación continua de rpm).

## Material

- Portátil con Windows y Python 3.
- Adaptador **DSD TECH SH-C30A** ([B0BQ5G3KLR](https://www.amazon.es/dp/B0BQ5G3KLR)): basado en CANable, firmware **candleLight** de fábrica, bornero CAN_H / CAN_L / GND, interruptor **R120** (terminación) e interruptor **Boot**.
- Tres sondas back-probe (B9 de la lista de compra) y multímetro.

## 0. Seguridad

- Máquina **estacionada**, implementos apoyados, **palanca de seguridad bloqueada**.
- Selector Auto/Manual en **MANUAL**.
- **Solo escuchar.** El script abre el adaptador en modo *listen-only* y **se niega a capturar** si el adaptador no lo admite: en ese modo no transmite ni confirma tramas, así que es invisible para la E-ECU.

## 1. Mediciones con el multímetro (conector B de la E-ECU, sin desconectar nada)

| Paso | Condición | Medir | Esperado |
|---|---|---|---|
| 1 | **Llave quitada** | Resistencia **B1–B2** | **≈ 60 Ω**. Si da **≈ 120 Ω**, falta una terminación: puentear JB13↔JB14 y JB5↔JB6 en el conector de la V-ECU. **Anotarlo** |
| 2 | **Llave en contacto**, motor parado | Tensión **B1→B9** (CAN H) y **B2→B9** (CAN L) | ≈ 2,5 V ambas; con tráfico, CAN H 2,5–3,5 V y CAN L 1,5–2,5 V |

## 2. Preparar el portátil (una vez)

```bash
python -m pip install --user gs_usb pyusb libusb-package
```

Enchufar el SH-C30A con el interruptor **Boot en OFF**. Con candleLight, Windows suele cargar el driver WinUSB solo. Si el script dice que no encuentra el adaptador, abrir **Zadig** (zadig.akeo.ie), elegir el dispositivo «candleLight USB to CAN adapter» e instalar **WinUSB**.

Comprobación sin máquina (debe decir «Modo SOLO ESCUCHA confirmado»):

```bash
python tools/captura_can.py capturar --nombre prueba --duracion 5
```

## 3. Conexión a la máquina

| SH-C30A | Conector B de la E-ECU | Notas |
|---|---|---|
| CAN_H | **B1** (amarillo) | back-probe |
| CAN_L | **B2** (verde) | back-probe |
| GND | **B9** (o B10) | back-probe |
| Interruptor **R120** | **OFF** | el bus ya tiene sus dos terminaciones (E-ECU y panel) |

Alternativa: JB14 / JB6 en el mazo de la V-ECU. Conectar **antes** de dar contacto.

## 4. Capturas (un fichero por prueba)

Cada captura se guarda en `capturas/<fecha>_<hora>_<nombre>.log`. Mientras graba, escribir una nota y pulsar **Enter** marca el momento (p. ej. «interruptor en ALTA», «muevo el brazo»). Ctrl+C para terminar.

| # | Situación | Orden | Para qué |
|---|---|---|---|
| 1 | Llave en contacto, motor parado | `capturar --nombre 01_contacto --duracion 60` | Mensajes sin motor, averías activas |
| 2 | **Arranque** (empezar antes de girar la llave) | `capturar --nombre 02_arranque --duracion 60` | Mensajes del arranque, si echa en falta la V-ECU |
| 3 | Ralentí (interruptor 26 en ralentí) | `capturar --nombre 03_ralenti --duracion 120` | rpm, temperatura, par en reposo |
| 4 | Interruptor 26 en **ALTA** | `capturar --nombre 04_alta --duracion 120` | 1900 rpm, cambios en otros mensajes |
| 5 | En alta **moviendo brazo y cuchara** | `capturar --nombre 05_carga --duracion 120` | Par con carga → umbral del auto-ralentí |
| 6 | Vuelta a ralentí y parada | `capturar --nombre 06_parada --duracion 60` | Comportamiento al bajar |

(Todas con `python tools/captura_can.py` delante.)

## 5. Análisis

```bash
python tools/captura_can.py analizar "capturas/*.log" --informe capturas/resumen.md
```

Por cada fichero sale: tabla de identificadores (PGN, quién lo envía, periodo, bytes que cambian), rpm y par de **EEC1**, temperatura de **ET1**, averías de **DM1** (también las multitrama), si hay **TSC1** en el bus y las notas con su tiempo. Los `.log` usan el formato de `candump -l`: también se abren con SavvyCAN o python-can.

## 6. Qué decidir con los resultados

- **Umbral de par del auto-ralentí** (`par <pct>` en la consola del firmware): entre el par a ralentí sin carga (prueba 3) y el de trabajo (prueba 5).
- **Averías sin V-ECU** (SID 231 / PSID 201 u otras): si aparecen, saber cuáles son normales.
- **Nodos presentes** (direcciones de origen): E-ECU 0x00, panel 0x17, ¿otros?
- Con todo ello, preparar la **Fase 2** (prueba de TSC1) de [`CONTROL_RPM.md`](CONTROL_RPM.md) §4.
