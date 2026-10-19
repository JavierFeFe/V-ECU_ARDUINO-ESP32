// Consola por el puerto serie (115200): pruebas en banco y ajustes sin OLED.
#pragma once

#include "can_j1939.h"

namespace consola {

void begin();
void poll(const EstadoMotor& motor);

}  // namespace consola
