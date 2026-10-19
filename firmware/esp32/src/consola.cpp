#include "consola.h"

#include "config.h"
#include "control.h"
#include "pantalla.h"
#include "rele.h"

namespace consola {

static char linea[64];
static size_t len = 0;
static bool logPeriodico = false;
static uint32_t ultimoLogMs = 0;

static void ayuda() {
  Serial.println(
      "Comandos:\n"
      "  estado              resumen\n"
      "  modo reposo|alto|auto|tsc1\n"
      "  ralenti <s>         tiempo sin par antes de bajar a 800 rpm\n"
      "  par <pct>           par minimo que cuenta como trabajo\n"
      "  rpm <n>             consigna TSC1 (800-2000)\n"
      "  log                 activa/desactiva el estado cada segundo\n"
      "  ayuda");
}

static void estado(const EstadoMotor& m) {
  const EstadoControl& c = control::estado();
  const uint32_t ahora = millis();
  Serial.printf("modo=%s%s rele=%s | ralenti=%us par>=%d%% rpmTSC1=%u\n",
                control::nombre(c.modo),
                c.modo == Modo::AutoRalenti ? (c.enRalenti ? "(800)" : "(1900)") : "",
                rele::excitado() ? "ON" : "off", c.ralentiS, c.parActividadPct, c.rpmConsigna);
  if (can::datosMotor(m, ahora)) {
    Serial.printf("motor: %.0f rpm, par %d%%, refrig %d C, DTC %u (SPN %lu FMI %u)\n", m.rpm,
                  m.parValido ? m.parPct : 0, m.refrigeranteValido ? m.refrigeranteC : 0, m.numDtc,
                  (unsigned long)m.dtcSpn, m.dtcFmi);
  } else {
    Serial.println("motor: sin EEC1");
  }
  Serial.printf("can: %s, %s, %lu tramas rx, %lu TSC1 | oled: %s | libre %lu B\n", can::estadoBus(),
                can::soloEscucha() ? "solo escucha" : "TX", (unsigned long)m.tramasRx,
                (unsigned long)c.tsc1Enviados, pantalla::presente() ? "si" : "no", (unsigned long)ESP.getFreeHeap());
}

static void ejecutar(char* cmd, const EstadoMotor& m) {
  char* arg = strchr(cmd, ' ');
  if (arg) *arg++ = '\0';

  if (!strcmp(cmd, "estado") || !strcmp(cmd, "e")) {
    estado(m);
  } else if (!strcmp(cmd, "modo") && arg) {
    Modo nuevo;
    if (!strcmp(arg, "reposo")) nuevo = Modo::Reposo;
    else if (!strcmp(arg, "alto")) nuevo = Modo::Alto;
    else if (!strcmp(arg, "auto")) nuevo = Modo::AutoRalenti;
    else if (!strcmp(arg, "tsc1")) nuevo = Modo::Tsc1;
    else { Serial.println("modo desconocido"); return; }
    if (!control::fijarModo(nuevo)) Serial.println("modo no disponible (compilar con VECU_TSC1_TX=1)");
  } else if (!strcmp(cmd, "ralenti") && arg) {
    control::fijarRalentiS(atoi(arg));
    Serial.printf("ralenti = %u s\n", control::estado().ralentiS);
  } else if (!strcmp(cmd, "par") && arg) {
    control::fijarParActividad(atoi(arg));
    Serial.printf("par de actividad = %d %%\n", control::estado().parActividadPct);
  } else if (!strcmp(cmd, "rpm") && arg) {
    control::fijarRpm(atoi(arg));
    Serial.printf("consigna TSC1 = %u rpm\n", control::estado().rpmConsigna);
  } else if (!strcmp(cmd, "log")) {
    logPeriodico = !logPeriodico;
    Serial.printf("log %s\n", logPeriodico ? "on" : "off");
  } else {
    ayuda();
  }
}

void begin() {
  Serial.println("Escribe 'ayuda' para ver los comandos.");
}

void poll(const EstadoMotor& m) {
  while (Serial.available()) {
    const char ch = Serial.read();
    if (ch == '\r' || ch == '\n') {
      if (len) {
        linea[len] = '\0';
        ejecutar(linea, m);
        len = 0;
      }
    } else if (len < sizeof(linea) - 1) {
      linea[len++] = tolower(ch);
    }
  }

  if (logPeriodico && millis() - ultimoLogMs >= 1000) {
    ultimoLogMs = millis();
    estado(m);
  }
}

}  // namespace consola
