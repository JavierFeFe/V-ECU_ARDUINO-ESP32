// Encoder rotativo KY-040: giro por interrupción, pulsador por sondeo.
#pragma once

#include <Arduino.h>

namespace encoder {

enum class Pulsacion : uint8_t { Ninguna, Corta, Larga };

void begin();
int32_t leerDelta();      // clics girados desde la última llamada (+ horario)
Pulsacion leerPulsacion();  // llamar en cada loop()

}  // namespace encoder
