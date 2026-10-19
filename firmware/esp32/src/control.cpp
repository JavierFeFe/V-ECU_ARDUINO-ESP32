#include "control.h"

#include <Preferences.h>

#include "config.h"
#include "encoder.h"
#include "rele.h"

namespace control {

static EstadoControl e;
static Preferences prefs;
static uint32_t uiDesdeMs = 0;
static uint32_t ultimoTsc1Ms = 0;

const char* nombre(Modo m) {
  switch (m) {
    case Modo::Reposo: return "REPOSO";
    case Modo::Alto: return "ALTO";
    case Modo::AutoRalenti: return "AUTO-RALENTI";
    case Modo::Tsc1: return "TSC1";
  }
  return "?";
}

bool disponible(Modo m) {
  return m != Modo::Tsc1 || VECU_TSC1_TX;
}

static Modo siguiente(Modo m, int32_t paso) {
  constexpr int N = 4;
  int i = (int)m;
  do {
    i = ((i + paso) % N + N) % N;
  } while (!disponible((Modo)i));
  return (Modo)i;
}

static void guardar() {
  prefs.putUShort("ralentiS", e.ralentiS);
  prefs.putUShort("rpm", e.rpmConsigna);
  prefs.putChar("par", e.parActividadPct);
}

void begin() {
  prefs.begin("vecu", false);
  e.ralentiS = constrain(prefs.getUShort("ralentiS", cfg::RALENTI_S_DEFECTO), cfg::RALENTI_S_MIN, cfg::RALENTI_S_MAX);
  e.rpmConsigna = constrain(prefs.getUShort("rpm", 1500), cfg::RPM_MIN, cfg::RPM_MAX);
  e.parActividadPct = prefs.getChar("par", cfg::PAR_ACTIVIDAD_DEFECTO);
  e.modo = Modo::Reposo;  // el modo nunca se recuerda: siempre se arranca en reposo
  e.ultimaActividadMs = millis();
#if VECU_OPTO
  pinMode(cfg::PIN_OPTO_B4, INPUT);
  pinMode(cfg::PIN_OPTO_SELECTOR, INPUT);
#endif
}

const EstadoControl& estado() { return e; }

bool fijarModo(Modo m) {
  if (!disponible(m)) return false;
  if (m != e.modo) Serial.printf("[control] modo %s -> %s\n", nombre(e.modo), nombre(m));
  e.modo = m;
  e.enRalenti = false;
  e.ultimaActividadMs = millis();
  return true;
}

void fijarRalentiS(uint16_t s) {
  e.ralentiS = constrain(s, cfg::RALENTI_S_MIN, cfg::RALENTI_S_MAX);
  guardar();
}

void fijarRpm(uint16_t rpm) {
  e.rpmConsigna = constrain(rpm, cfg::RPM_MIN, cfg::RPM_MAX);
  guardar();
}

void fijarParActividad(int8_t pct) {
  e.parActividadPct = constrain(pct, (int8_t)0, (int8_t)100);
  guardar();
}

static void atenderEncoder(uint32_t ahora) {
  const int32_t delta = encoder::leerDelta();
  const encoder::Pulsacion p = encoder::leerPulsacion();

  if (delta != 0 || p != encoder::Pulsacion::Ninguna) {
    uiDesdeMs = ahora;
    e.ultimaActividadMs = ahora;  // tocar el mando también cuenta como actividad
  }

  if (p == encoder::Pulsacion::Larga) {
    e.ui = Ui::Normal;
    fijarModo(Modo::Reposo);
    return;
  }

  switch (e.ui) {
    case Ui::Normal:
      if (delta != 0) {
        e.candidato = siguiente(e.modo, delta > 0 ? 1 : -1);
        e.ui = Ui::EligiendoModo;
      } else if (p == encoder::Pulsacion::Corta &&
                 (e.modo == Modo::AutoRalenti || e.modo == Modo::Tsc1)) {
        e.ui = Ui::EditandoParam;
      }
      break;

    case Ui::EligiendoModo:
      if (delta != 0) e.candidato = siguiente(e.candidato, delta > 0 ? 1 : -1);
      if (p == encoder::Pulsacion::Corta) {
        fijarModo(e.candidato);
        e.ui = Ui::Normal;
      }
      break;

    case Ui::EditandoParam:
      if (delta != 0) {
        if (e.modo == Modo::AutoRalenti) {
          e.ralentiS = constrain((int32_t)e.ralentiS + delta, (int32_t)cfg::RALENTI_S_MIN, (int32_t)cfg::RALENTI_S_MAX);
        } else if (e.modo == Modo::Tsc1) {
          e.rpmConsigna = constrain((int32_t)e.rpmConsigna + delta * cfg::RPM_PASO, (int32_t)cfg::RPM_MIN, (int32_t)cfg::RPM_MAX);
        }
      }
      if (p == encoder::Pulsacion::Corta) {
        guardar();
        e.ui = Ui::Normal;
      }
      break;
  }

  if (e.ui != Ui::Normal && ahora - uiDesdeMs > cfg::UI_TIMEOUT_MS) {
    if (e.ui == Ui::EditandoParam) guardar();
    e.ui = Ui::Normal;
  }
}

void actualizar(const EstadoMotor& motor) {
  const uint32_t ahora = millis();
  atenderEncoder(ahora);

#if VECU_OPTO
  e.b4Alto = (digitalRead(cfg::PIN_OPTO_B4) == LOW) == cfg::OPTO_ACTIVO_BAJO;
  e.selectorManual = (digitalRead(cfg::PIN_OPTO_SELECTOR) == LOW) == cfg::OPTO_ACTIVO_BAJO;
#endif

  const bool hayDatos = can::datosMotor(motor, ahora);
  bool releOn = false;

  switch (e.modo) {
    case Modo::Reposo:
      releOn = false;
      break;

    case Modo::Alto:
      releOn = true;
      break;

    case Modo::AutoRalenti:
      if (!hayDatos || !motor.parValido) {
        // Sin datos no se sabe si la máquina trabaja: no bajar a ralentí.
        e.ultimaActividadMs = ahora;
        if (e.enRalenti) Serial.println("[control] sin datos CAN: vuelta a alto");
        e.enRalenti = false;
      } else if (motor.parPct >= e.parActividadPct) {
        e.ultimaActividadMs = ahora;
        if (e.enRalenti) Serial.printf("[control] par %d %%: vuelta a alto\n", motor.parPct);
        e.enRalenti = false;
      } else if (!e.enRalenti && ahora - e.ultimaActividadMs >= e.ralentiS * 1000UL) {
        Serial.printf("[control] %u s sin par: ralenti\n", e.ralentiS);
        e.enRalenti = true;
      }
      if (e.enRalenti && ahora - e.ultimaActividadMs < 100) e.enRalenti = false;  // actividad del mando
      releOn = !e.enRalenti;
      break;

    case Modo::Tsc1:
      releOn = false;
      if (ahora - ultimoTsc1Ms >= cfg::TSC1_PERIODO_MS) {
        ultimoTsc1Ms = ahora;
        if (can::enviarTSC1(e.rpmConsigna)) e.tsc1Enviados++;
      }
      break;
  }

  rele::fijar(releOn);
}

}  // namespace control
