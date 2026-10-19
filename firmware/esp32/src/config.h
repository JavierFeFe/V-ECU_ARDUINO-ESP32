// Pines, límites y opciones de compilación.
// Pines: docs/HARDWARE_PLACA_ESP32_RELE.md · mensajes CAN: docs/CONTROL_RPM.md §5.
#pragma once

#include <Arduino.h>

// 1 = permite transmitir TSC1 (vía A). Por defecto el CAN va en solo escucha.
#ifndef VECU_TSC1_TX
#define VECU_TSC1_TX 0
#endif

// 1 = lee el optoacoplador (estado de B4 y selector Auto/Manual).
#ifndef VECU_OPTO
#define VECU_OPTO 0
#endif

namespace cfg {

// --- Pines de la placa ESP32_Relay X1 V1.2 ---
constexpr uint8_t PIN_RELE = 16;  // confirmado; relé excitado = 24 V en B4 = 1900 rpm
constexpr uint8_t PIN_CAN_TX = 17;
constexpr uint8_t PIN_CAN_RX = 18;
constexpr uint8_t PIN_SDA = 21;
constexpr uint8_t PIN_SCL = 22;
constexpr uint8_t PIN_ENC_CLK = 32;
constexpr uint8_t PIN_ENC_DT = 33;
constexpr uint8_t PIN_ENC_SW = 27;
constexpr uint8_t PIN_OPTO_B4 = 35;        // solo entrada, sin pull-up interno
constexpr uint8_t PIN_OPTO_SELECTOR = 39;  // ídem
constexpr bool OPTO_ACTIVO_BAJO = true;    // salida típica de colector abierto

constexpr uint8_t OLED_ADDR = 0x3C;

// --- Régimen ---
constexpr uint16_t RPM_RALENTI = 800;  // B4 < 4 V
constexpr uint16_t RPM_ALTO = 1900;    // B4 > 8 V
constexpr uint16_t RPM_MIN = 800;      // límites de la consigna TSC1
constexpr uint16_t RPM_MAX = 2000;
constexpr uint16_t RPM_PASO = 50;

// --- Auto-ralentí ---
constexpr uint16_t RALENTI_S_DEFECTO = 10;
constexpr uint16_t RALENTI_S_MIN = 3;
constexpr uint16_t RALENTI_S_MAX = 120;
constexpr int8_t PAR_ACTIVIDAD_DEFECTO = 15;  // % de par real (EEC1) que cuenta como trabajo

// --- CAN J1939 ---
constexpr uint8_t SA_EECU = 0x00;
constexpr uint8_t SA_VECU = 0x11;
constexpr uint32_t CAN_TIMEOUT_MS = 500;  // sin EEC1 en este tiempo = sin datos del motor
constexpr uint32_t TSC1_PERIODO_MS = 10;

// --- Sistema ---
constexpr uint32_t WDT_MS = 500;
constexpr uint32_t PANTALLA_PERIODO_MS = 200;
constexpr uint32_t UI_TIMEOUT_MS = 5000;  // sin tocar el encoder, se cancela la selección
constexpr uint32_t PULSACION_LARGA_MS = 1500;
constexpr uint8_t PASOS_POR_DETENTE = 4;  // transiciones del encoder por clic

}  // namespace cfg
