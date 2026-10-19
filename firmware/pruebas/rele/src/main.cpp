// Prueba de banco del relé (docs/MONTAJE.md §5.1).
// Conmuta GPIO16 cada segundo: debe oírse el clic y medirse continuidad COM–NO
// con el pin en alto. Si no conmuta, el relé está en otro GPIO.

#include <Arduino.h>

constexpr uint8_t PIN_RELE = 16;  // probable, a confirmar
constexpr uint32_t PERIODO_MS = 1000;

void setup() {
  Serial.begin(115200);
  pinMode(PIN_RELE, OUTPUT);
  digitalWrite(PIN_RELE, LOW);
  Serial.printf("\nPrueba de rele en GPIO%u\n", PIN_RELE);
}

void loop() {
  static bool alto = false;
  alto = !alto;
  digitalWrite(PIN_RELE, alto ? HIGH : LOW);
  Serial.printf("GPIO%u = %s\n", PIN_RELE, alto ? "ALTO (rele excitado?)" : "BAJO");
  delay(PERIODO_MS);
}
