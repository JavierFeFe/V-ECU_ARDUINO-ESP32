// V-ECU — control de rpm del motor D6D de la Volvo EC210B.
// Alcance: docs/CONTROL_RPM.md · montaje: docs/MONTAJE.md.
//
// Reglas de seguridad:
//  1. El relé arranca en reposo (manda el interruptor original) y el modo nunca
//     se recuerda entre arranques.
//  2. CAN en solo escucha salvo compilación explícita con VECU_TSC1_TX=1.
//  3. Watchdog de 500 ms: si el programa se cuelga, el ESP32 se reinicia y el
//     relé vuelve a reposo.

#include <Arduino.h>
#include <esp_task_wdt.h>

#include "can_j1939.h"
#include "config.h"
#include "consola.h"
#include "control.h"
#include "encoder.h"
#include "pantalla.h"
#include "rele.h"

static EstadoMotor motor;

static void iniciarWatchdog() {
  esp_task_wdt_config_t c = {};
  c.timeout_ms = cfg::WDT_MS;
  c.idle_core_mask = 0;
  c.trigger_panic = true;
  if (esp_task_wdt_reconfigure(&c) != ESP_OK) esp_task_wdt_init(&c);
  esp_task_wdt_add(nullptr);
}

void setup() {
  rele::begin();  // lo primero: relé en reposo

  Serial.begin(115200);
  Serial.printf("\nV-ECU rpm — reinicio: %d, TSC1 %s\n", (int)esp_reset_reason(),
                VECU_TSC1_TX ? "HABILITADO" : "deshabilitado");

  control::begin();
  encoder::begin();
  pantalla::begin();
  can::begin(!VECU_TSC1_TX);
  consola::begin();
  iniciarWatchdog();
}

void loop() {
  esp_task_wdt_reset();
  can::poll(motor);
  control::actualizar(motor);
  consola::poll(motor);
  pantalla::actualizar(control::estado(), motor);
  delay(1);
}
