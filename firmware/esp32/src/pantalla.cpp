#include "pantalla.h"

#include <Adafruit_SSD1306.h>
#include <Wire.h>

#include "config.h"
#include "rele.h"

namespace pantalla {

static Adafruit_SSD1306 oled(128, 64, &Wire, -1);
static bool hay = false;
static uint32_t ultimaMs = 0;

bool begin() {
  Wire.begin(cfg::PIN_SDA, cfg::PIN_SCL, 400000);
  Wire.beginTransmission(cfg::OLED_ADDR);
  if (Wire.endTransmission() != 0 || !oled.begin(SSD1306_SWITCHCAPVCC, cfg::OLED_ADDR)) {
    Serial.println("[oled] no detectada: se sigue sin pantalla");
    hay = false;
    return false;
  }
  hay = true;
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  oled.println("V-ECU rpm");
  oled.display();
  Serial.println("[oled] detectada");
  return true;
}

bool presente() { return hay; }

void actualizar(const EstadoControl& c, const EstadoMotor& m) {
  if (!hay) return;
  const uint32_t ahora = millis();
  if (ahora - ultimaMs < cfg::PANTALLA_PERIODO_MS) return;
  ultimaMs = ahora;

  const bool datos = can::datosMotor(m, ahora);
  oled.clearDisplay();

  // Línea 1: modo (o el que se está eligiendo)
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  if (c.ui == Ui::EligiendoModo) {
    oled.printf("> %s ?", control::nombre(c.candidato));
  } else {
    oled.print(control::nombre(c.modo));
    if (c.modo == Modo::AutoRalenti) oled.print(c.enRalenti ? " (800)" : " (1900)");
  }

  // Centro: rpm reales
  oled.setTextSize(3);
  oled.setCursor(0, 14);
  if (datos) oled.printf("%4.0f", m.rpm);
  else oled.print("----");
  oled.setTextSize(1);
  oled.setCursor(76, 28);
  oled.print("rpm");

  // Parámetro del modo
  oled.setCursor(0, 42);
  const bool editando = c.ui == Ui::EditandoParam;
  if (c.modo == Modo::AutoRalenti) {
    oled.printf("%sralenti %us", editando ? ">" : "", c.ralentiS);
  } else if (c.modo == Modo::Tsc1) {
    oled.printf("%sconsigna %u", editando ? ">" : "", c.rpmConsigna);
  }
  if (datos && m.parValido) {
    oled.setCursor(92, 42);
    oled.printf("%3d%%", m.parPct);
  }

  // Línea inferior: refrigerante, relé, DTC, CAN
  oled.setCursor(0, 56);
  if (m.refrigeranteValido) oled.printf("%dC ", m.refrigeranteC);
  else oled.print("--C ");
  oled.print(rele::excitado() ? "B4:ON " : "B4:-- ");
  if (m.numDtc) oled.printf("DTC%u ", m.numDtc);
  oled.print(datos ? "CAN" : "noCAN");

  oled.display();
}

}  // namespace pantalla
