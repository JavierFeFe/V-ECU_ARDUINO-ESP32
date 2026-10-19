// Bus J1939 a 250 kbit/s con el periférico TWAI del ESP32.
// Lee EEC1 (rpm, par), ET1 (refrigerante) y DM1 (averías) de la E-ECU.
#pragma once

#include <Arduino.h>

struct EstadoMotor {
  float rpm = 0;
  int16_t parPct = 0;  // par real, % (EEC1 byte 3 − 125)
  bool parValido = false;
  int16_t refrigeranteC = 0;
  bool refrigeranteValido = false;
  uint32_t ultimoEEC1ms = 0;
  uint32_t ultimoET1ms = 0;

  // DM1: lámparas (byte 1) y DTC activos.
  uint8_t lamparas = 0;
  uint8_t numDtc = 0;
  uint32_t dtcSpn = 0;  // primer DTC (DM1 de una sola trama)
  uint8_t dtcFmi = 0;
  uint32_t ultimoDM1ms = 0;

  uint32_t tramasRx = 0;
};

namespace can {

bool begin(bool soloEscucha);
void poll(EstadoMotor& motor);
bool enviarTSC1(uint16_t rpm);  // devuelve false en solo escucha o si la cola está llena
bool iniciado();
bool soloEscucha();
const char* estadoBus();

// true si hay EEC1 reciente.
bool datosMotor(const EstadoMotor& motor, uint32_t ahora);

}  // namespace can
