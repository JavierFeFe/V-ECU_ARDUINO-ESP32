#include "rele.h"

#include "config.h"

namespace rele {

static bool estado = false;

void begin() {
  digitalWrite(cfg::PIN_RELE, LOW);
  pinMode(cfg::PIN_RELE, OUTPUT);
  digitalWrite(cfg::PIN_RELE, LOW);
  estado = false;
}

void fijar(bool excitado) {
  if (excitado == estado) return;
  digitalWrite(cfg::PIN_RELE, excitado ? HIGH : LOW);
  estado = excitado;
  Serial.printf("[rele] %s\n", excitado ? "EXCITADO (B4 alto)" : "REPOSO");
}

bool excitado() { return estado; }

}  // namespace rele
