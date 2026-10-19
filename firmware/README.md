# Firmware

Estructura prevista (ver el plan en `../docs/INVESTIGACION_V-ECU_EC210B.md` §6 y los pines en `../docs/ESQUEMA_CONEXION.md`):

```
firmware/
├── esp32/            ← proyecto PlatformIO (Arduino-ESP32 core 3.x)
│   ├── platformio.ini
│   └── src/
│       ├── main.cpp          ← bucle principal, watchdog, máquina de estados
│       ├── valve_driver.*    ← lazo PI de corriente, PWM 1 kHz + dither, rampas, relé de seguridad
│       ├── can_j1939.*       ← TWAI 250 kbit/s: escucha EEC1/ET1/DM1; TSC1 (Fase 3, deshabilitado por defecto)
│       ├── ui.*              ← encoder KY-040 + OLED SSD1306
│       └── config.h          ← pines, límites (200–650 mA, 800–2000 rpm), tabla de modos
└── arduino_nano/     ← alternativa ATmega328P + MCP2515 (Fase 1 y escucha CAN)
```

Reglas de seguridad que el firmware debe cumplir:

1. Arranque con el relé K1 en reposo (Resistor Box de fábrica) y PWM a 0; el relé solo se activa cuando el lazo de corriente está en marcha y el watchdog armado.
2. Consigna de corriente limitada a 200–650 mA; sin lectura válida del sensor de corriente no se activa el relé.
3. Si la corriente medida se aleja más de 120 mA de la consigna durante más de 300 ms → PWM a 0 y relé en reposo.
4. CAN en `LISTEN_ONLY` por defecto. La transmisión de TSC1 requiere una opción de compilación explícita y el selector Auto/Manual en Auto con la V-ECU desconectada.
5. Watchdog hardware de 500 ms.
