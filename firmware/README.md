# Firmware

Alcance actual: **control de rpm del motor** ([`../docs/CONTROL_RPM.md`](../docs/CONTROL_RPM.md)). La regulación de la válvula power shift queda aplazada.

```
firmware/
├── esp32/                    ← firmware del proyecto (PlatformIO, Arduino-ESP32 3.x)
│   ├── platformio.ini        ← entornos esp32dev (solo escucha) y esp32dev_tsc1
│   └── src/
│       ├── main.cpp          ← arranque, watchdog y bucle principal
│       ├── config.h          ← pines, límites (800–2000 rpm), tiempos y opciones
│       ├── rele.*            ← relé de la vía B (GPIO16 → línea B4)
│       ├── can_j1939.*       ← TWAI 250 kbit/s: EEC1 / ET1 / DM1; TSC1 (deshabilitado por defecto)
│       ├── control.*         ← modos Reposo / Alto / Auto-ralentí / TSC1 y manejo del encoder
│       ├── encoder.*         ← encoder rotativo (interrupción) y pulsador
│       ├── pantalla.*        ← OLED SSD1306 (opcional, se detecta sola)
│       └── consola.*         ← comandos por el puerto serie
└── pruebas/                  ← pruebas de banco (led GPIO2, relé GPIO16)
```

## Hardware

Placa **ESP32_Relay X1 V1.2**. Pines en [`../docs/HARDWARE_PLACA_ESP32_RELE.md`](../docs/HARDWARE_PLACA_ESP32_RELE.md):

| Función | GPIO |
|---|---|
| Relé (B4) | 16 (confirmado) |
| CAN TX / RX → CAN Pal (TJA1051T/3) | 17 / 18 |
| SLNT del CAN Pal (alto = silencio) | 4 |
| OLED SDA / SCL | 21 / 22 |
| Encoder CLK / DT / SW | 32 / 33 / 27 |
| Opto B4 / selector (opcional, `VECU_OPTO=1`) | 35 / 39 |

## Modos

| Modo | Relé | Comportamiento |
|---|---|---|
| **Reposo** | reposo | Manda el interruptor de emergencia original. Siempre se arranca aquí |
| **Alto** | excitado | 24 V en B4 → 1900 rpm |
| **Auto-ralentí** | según el par | 1900 rpm mientras el par real (EEC1) supere el umbral; tras `ralenti` segundos por debajo baja a 800 rpm y vuelve en cuanto sube el par o se toca el encoder. **Sin datos CAN no baja a ralentí** |
| **TSC1** | reposo | Envía TSC1 (`0x0C000011`, 10 ms) con la consigna 800–2000 rpm. Solo existe en el entorno `esp32dev_tsc1` |

Para que el relé pueda bajar a 800 rpm, el interruptor de emergencia 26 debe estar en **ralentí**: el relé está en paralelo con su contacto de alta.

## Encoder

- **Girar:** elegir modo (`> MODO ?` en la OLED); **pulsar** para aplicarlo. Si no se pulsa, se cancela a los 5 s.
- **Pulsar sin girar** (en Auto-ralentí o TSC1): editar el parámetro (segundos de ralentí o rpm de consigna); girar para cambiarlo y pulsar para guardar.
- **Pulsación larga (1,5 s):** vuelta inmediata a **Reposo**.

Los ajustes (segundos de ralentí, umbral de par, consigna) se guardan en la flash; el modo no.

## Consola serie (115200)

| Comando | Qué hace |
|---|---|
| `estado` (`e`) | Modo, relé, datos del motor, estado del bus |
| `modo reposo\|alto\|auto\|tsc1` | Cambiar de modo |
| `ralenti <s>` | Segundos sin par antes de bajar a 800 rpm (3–120) |
| `par <pct>` | Par real mínimo que cuenta como trabajo (por defecto 15 %) |
| `rpm <n>` | Consigna TSC1 |
| `log` | Estado cada segundo (activar/desactivar) |

## Panel en el navegador

Todas las funciones de la consola con botones: modo y relé, ajustes, datos del motor y del bus, log completo (filtrable y descargable) y línea de comandos libres. <kbd>Esc</kbd> vuelve a **Reposo** desde cualquier parte.

```bash
python tools/panel_esp32.py
```

Abre `http://127.0.0.1:8765` (solo accesible desde el propio portátil). El panel es el único programa que abre el puerto serie: **cerrar antes la consola de PlatformIO**. Busca solo el programador y, si se desenchufa y vuelve con otro nombre (`ttyACM0` → `ttyACM1`), lo reencuentra. Opciones: `--puerto /dev/ttyACM0`, `--http 8765`, `--no-abrir`.

El botón **📐 Diagramas** de la cabecera muestra el montaje de la placa, el esquema de rpm, el conector redondo (E7/E8), los interruptores del SH-C30A para la prueba de banco y las fotos de la placa. Con el visor abierto, <kbd>Esc</kbd> solo lo cierra (no manda Reposo).

**Registro automático:** cada sesión del panel se guarda en `registros/placa/<fecha>_<hora>.log` con todo lo que dice la placa, los comandos enviados y un resumen del estado cada 10 s (`--sin-registro` lo desactiva).

El relé no tiene orden propia en el firmware: en el panel, activarlo equivale a `modo alto` y desactivarlo a `modo reposo`.

## Compilar y grabar

```bash
python -m platformio run -d firmware/esp32 -e esp32dev -t upload
```

El programador va conectado solo con GND, TX y RX (EN e IO0 sin cablear): mantener pulsado el **botón IO0** de la placa al dar tensión antes de grabar y, al terminar, quitar y volver a dar tensión. Monitor: `python -m platformio device monitor -d firmware/esp32`.

El puerto se detecta solo (COMx en Windows, `/dev/ttyUSB0` o `/dev/ttyACM0` en Linux); si hay varios, añadir `--upload-port <puerto>`. En el portátil de pruebas con Linux, PlatformIO está en el entorno `.venv` del repositorio: activarlo antes (`source .venv/bin/activate.fish`) y, la primera vez, instalar los permisos del puerto serie con `sh tools/linux/instalar_permisos.sh` (ver [`../docs/CAPTURA_CAN.md`](../docs/CAPTURA_CAN.md) §2).

## Reglas de seguridad que cumple el firmware

1. Arranque con el relé en reposo; el modo no se recuerda entre arranques.
2. CAN en `LISTEN_ONLY` por defecto y, además, el transceptor en silencio por hardware (SLNT del CAN Pal en alto desde el arranque). TSC1 solo con el entorno `esp32dev_tsc1` (Fase 2 de `CONTROL_RPM.md`: tras la captura del bus y con la máquina parada).
3. Consigna TSC1 limitada a 800–2000 rpm.
4. Watchdog de 500 ms: si el programa se cuelga, el ESP32 se reinicia y el relé vuelve a reposo.
5. Auto-ralentí no baja a 800 rpm sin datos válidos del motor.
