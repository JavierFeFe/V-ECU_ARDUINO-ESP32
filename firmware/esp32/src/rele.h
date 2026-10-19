// Relé de la vía B: en paralelo con el contacto 2–3 del interruptor de emergencia 26.
// En reposo manda el interruptor original; excitado pone 24 V en B4 (1900 rpm).
#pragma once

namespace rele {

void begin();  // deja el relé en reposo; llamar lo primero en setup()
void fijar(bool excitado);
bool excitado();

}  // namespace rele
