// OLED SSD1306 128×64 por I²C (0x3C). Si no se detecta, el firmware sigue sin pantalla.
#pragma once

#include "can_j1939.h"
#include "control.h"

namespace pantalla {

bool begin();
bool presente();
void actualizar(const EstadoControl& c, const EstadoMotor& m);

}  // namespace pantalla
