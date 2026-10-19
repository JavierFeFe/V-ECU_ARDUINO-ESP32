// Prueba de banco: parpadeo del LED de estado.
// Si el LED no parpadea, la placa no tiene LED en GPIO2.

#include <Arduino.h>

constexpr uint8_t PIN_LED = 2;
constexpr uint32_t PERIODO_MS = 500;

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED, OUTPUT);
  Serial.printf("\nParpadeo del LED en GPIO%u\n", PIN_LED);
}

void loop() {
  static bool encendido = false;
  encendido = !encendido;
  digitalWrite(PIN_LED, encendido ? HIGH : LOW);
  Serial.printf("LED %s\n", encendido ? "ON" : "OFF");
  delay(PERIODO_MS);
}
