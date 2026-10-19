// Máquina de estados del control de rpm (docs/CONTROL_RPM.md §4, Fases 2–4).
//
// Modos:
//   Reposo      relé en reposo: manda el interruptor de emergencia original.
//   Alto        relé excitado: B4 a 24 V = 1900 rpm.
//   AutoRalenti 1900 rpm mientras hay par (EEC1); tras N s sin par baja a 800 rpm
//               y vuelve a 1900 en cuanto sube el par. Sin datos CAN se queda en alto.
//   Tsc1        consigna continua por CAN (solo con VECU_TSC1_TX=1). Relé en reposo,
//               así al dejar de enviar la E-ECU vuelve a lo que diga B4.
//
// Encoder: girar elige modo (pulsar para aplicar); pulsar sin girar edita el parámetro
// del modo (s de auto-ralentí o rpm de TSC1); pulsación larga = Reposo inmediato.
#pragma once

#include <Arduino.h>

#include "can_j1939.h"

enum class Modo : uint8_t { Reposo, Alto, AutoRalenti, Tsc1 };
enum class Ui : uint8_t { Normal, EligiendoModo, EditandoParam };

struct EstadoControl {
  Modo modo = Modo::Reposo;
  Modo candidato = Modo::Reposo;
  Ui ui = Ui::Normal;
  bool enRalenti = false;  // AutoRalenti: true = bajado a 800 rpm
  uint16_t rpmConsigna = 1500;
  uint16_t ralentiS = 10;
  int8_t parActividadPct = 15;
  uint32_t ultimaActividadMs = 0;
  bool b4Alto = false;        // optoacoplador (VECU_OPTO)
  bool selectorManual = true; // ídem
  uint32_t tsc1Enviados = 0;
};

namespace control {

void begin();
void actualizar(const EstadoMotor& motor);
const EstadoControl& estado();

bool fijarModo(Modo m);
void fijarRalentiS(uint16_t s);
void fijarRpm(uint16_t rpm);
void fijarParActividad(int8_t pct);

const char* nombre(Modo m);
bool disponible(Modo m);

}  // namespace control
