#include "encoder.h"

#include <soc/gpio_reg.h>

#include "config.h"

namespace encoder {

static volatile int32_t transiciones = 0;
static volatile uint8_t historial = 0;
static portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;

// Decodificación en cuadratura: índice = (estado anterior << 2) | estado actual.
static const int8_t TABLA[16] = {0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0};

static inline uint8_t IRAM_ATTR leerPin(uint8_t pin) {
  return pin >= 32 ? (REG_READ(GPIO_IN1_REG) >> (pin - 32)) & 1 : (REG_READ(GPIO_IN_REG) >> pin) & 1;
}

static void IRAM_ATTR isr() {
  const uint8_t s = (leerPin(cfg::PIN_ENC_CLK) << 1) | leerPin(cfg::PIN_ENC_DT);
  historial = ((historial << 2) | s) & 0x0F;
  portENTER_CRITICAL_ISR(&mux);
  transiciones += TABLA[historial];
  portEXIT_CRITICAL_ISR(&mux);
}

// Pulsador
static bool pulsado = false;
static bool largaEmitida = false;
static uint32_t desdeMs = 0;
static bool lecturaPrev = false;
static uint32_t cambioMs = 0;

void begin() {
  pinMode(cfg::PIN_ENC_CLK, INPUT_PULLUP);
  pinMode(cfg::PIN_ENC_DT, INPUT_PULLUP);
  pinMode(cfg::PIN_ENC_SW, INPUT_PULLUP);
  historial = (leerPin(cfg::PIN_ENC_CLK) << 1) | leerPin(cfg::PIN_ENC_DT);
  attachInterrupt(digitalPinToInterrupt(cfg::PIN_ENC_CLK), isr, CHANGE);
  attachInterrupt(digitalPinToInterrupt(cfg::PIN_ENC_DT), isr, CHANGE);
}

int32_t leerDelta() {
  portENTER_CRITICAL(&mux);
  const int32_t clics = transiciones / cfg::PASOS_POR_DETENTE;
  transiciones -= clics * cfg::PASOS_POR_DETENTE;
  portEXIT_CRITICAL(&mux);
  return clics;
}

Pulsacion leerPulsacion() {
  const uint32_t ahora = millis();
  const bool lectura = digitalRead(cfg::PIN_ENC_SW) == LOW;
  if (lectura != lecturaPrev) {
    lecturaPrev = lectura;
    cambioMs = ahora;
  }
  if (ahora - cambioMs < 30) return Pulsacion::Ninguna;  // antirrebote

  if (lectura && !pulsado) {
    pulsado = true;
    largaEmitida = false;
    desdeMs = ahora;
  } else if (lectura && pulsado && !largaEmitida && ahora - desdeMs >= cfg::PULSACION_LARGA_MS) {
    largaEmitida = true;
    return Pulsacion::Larga;
  } else if (!lectura && pulsado) {
    pulsado = false;
    if (!largaEmitida) return Pulsacion::Corta;
  }
  return Pulsacion::Ninguna;
}

}  // namespace encoder
