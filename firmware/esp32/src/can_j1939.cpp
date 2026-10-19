#include "can_j1939.h"

#include <driver/twai.h>

#include "config.h"

namespace can {

static bool arrancado = false;
static bool escucha = true;

// PGN de interés
constexpr uint32_t PGN_EEC1 = 0xF004;   // 61444
constexpr uint32_t PGN_ET1 = 0xFEEE;    // 65262
constexpr uint32_t PGN_DM1 = 0xFECA;    // 65226
constexpr uint32_t PGN_TP_CM = 0xEC00;  // transporte, para DM1 multitrama (BAM)

static uint32_t pgnDe(uint32_t id) {
  uint32_t pgn = (id >> 8) & 0x3FFFF;
  if (((pgn >> 8) & 0xFF) < 240) pgn &= 0x3FF00;  // PDU1: el byte bajo es la dirección destino
  return pgn;
}

bool begin(bool soloEscuchaBus) {
  escucha = soloEscuchaBus;
  twai_general_config_t g = TWAI_GENERAL_CONFIG_DEFAULT(
      (gpio_num_t)cfg::PIN_CAN_TX, (gpio_num_t)cfg::PIN_CAN_RX,
      escucha ? TWAI_MODE_LISTEN_ONLY : TWAI_MODE_NORMAL);
  g.rx_queue_len = 32;
  g.tx_queue_len = 4;
  twai_timing_config_t t = TWAI_TIMING_CONFIG_250KBITS();
  twai_filter_config_t f = TWAI_FILTER_CONFIG_ACCEPT_ALL();

  if (twai_driver_install(&g, &t, &f) != ESP_OK) {
    Serial.println("[can] error al instalar el driver TWAI");
    return false;
  }
  if (twai_start() != ESP_OK) {
    Serial.println("[can] error al arrancar TWAI");
    twai_driver_uninstall();
    return false;
  }
  arrancado = true;
  Serial.printf("[can] 250 kbit/s, %s\n", escucha ? "SOLO ESCUCHA" : "NORMAL (TX habilitado)");
  return true;
}

static void procesar(const twai_message_t& m, EstadoMotor& motor, uint32_t ahora) {
  if (!m.extd || m.rtr) return;
  const uint32_t pgn = pgnDe(m.identifier);
  const uint8_t sa = m.identifier & 0xFF;
  if (sa != cfg::SA_EECU) return;
  const uint8_t* d = m.data;

  switch (pgn) {
    case PGN_EEC1:
      if (m.data_length_code < 5) return;
      {
        const uint16_t crudo = d[3] | (d[4] << 8);
        if (crudo < 0xFB00) {
          motor.rpm = crudo * 0.125f;
          motor.ultimoEEC1ms = ahora;
        }
        motor.parValido = d[2] < 0xFB;
        if (motor.parValido) motor.parPct = (int16_t)d[2] - 125;
      }
      break;

    case PGN_ET1:
      if (m.data_length_code < 1) return;
      motor.refrigeranteValido = d[0] < 0xFB;
      if (motor.refrigeranteValido) motor.refrigeranteC = (int16_t)d[0] - 40;
      motor.ultimoET1ms = ahora;
      break;

    case PGN_DM1:
      // DM1 de una trama: lámparas + un DTC (SPN 0 / FMI 0 = sin averías).
      if (m.data_length_code < 6) return;
      motor.lamparas = d[0];
      motor.dtcSpn = d[2] | (d[3] << 8) | ((uint32_t)(d[4] & 0xE0) << 11);
      motor.dtcFmi = d[4] & 0x1F;
      motor.numDtc = (motor.dtcSpn == 0 && motor.dtcFmi == 0) ? 0 : 1;
      motor.ultimoDM1ms = ahora;
      break;

    case PGN_TP_CM:
      // BAM que anuncia un DM1 largo: solo se cuenta el número de DTC.
      if (m.data_length_code == 8 && d[0] == 0x20) {
        const uint32_t pgnBam = d[5] | (d[6] << 8) | ((uint32_t)d[7] << 16);
        const uint16_t bytes = d[1] | (d[2] << 8);
        if (pgnBam == PGN_DM1 && bytes >= 2) {
          motor.numDtc = (bytes - 2) / 4;
          motor.dtcSpn = 0;
          motor.dtcFmi = 0;
          motor.ultimoDM1ms = ahora;
        }
      }
      break;
  }
}

void poll(EstadoMotor& motor) {
  if (!arrancado) return;
  const uint32_t ahora = millis();
  twai_message_t m;
  while (twai_receive(&m, 0) == ESP_OK) {
    motor.tramasRx++;
    procesar(m, motor, ahora);
  }

  // En modo normal, recuperar del bus-off.
  twai_status_info_t s;
  if (!escucha && twai_get_status_info(&s) == ESP_OK) {
    if (s.state == TWAI_STATE_BUS_OFF) {
      twai_initiate_recovery();
    } else if (s.state == TWAI_STATE_STOPPED) {
      twai_start();
    }
  }
}

bool enviarTSC1(uint16_t rpm) {
#if VECU_TSC1_TX
  if (!arrancado || escucha) return false;
  rpm = constrain(rpm, cfg::RPM_MIN, cfg::RPM_MAX);
  const uint16_t crudo = rpm * 8;  // 0,125 rpm/bit

  twai_message_t m = {};
  m.extd = 1;
  m.identifier = 0x0C000000 | ((uint32_t)cfg::SA_EECU << 8) | cfg::SA_VECU;  // prio 3, PGN 0
  m.data_length_code = 8;
  m.data[0] = 0xF1;  // modo control de velocidad
  m.data[1] = crudo & 0xFF;
  m.data[2] = crudo >> 8;
  for (int i = 3; i < 8; i++) m.data[i] = 0xFF;
  return twai_transmit(&m, 0) == ESP_OK;
#else
  (void)rpm;
  return false;
#endif
}

bool iniciado() { return arrancado; }
bool soloEscucha() { return escucha; }

const char* estadoBus() {
  if (!arrancado) return "sin driver";
  twai_status_info_t s;
  if (twai_get_status_info(&s) != ESP_OK) return "?";
  switch (s.state) {
    case TWAI_STATE_RUNNING: return "OK";
    case TWAI_STATE_BUS_OFF: return "BUS-OFF";
    case TWAI_STATE_RECOVERING: return "recuperando";
    default: return "parado";
  }
}

bool datosMotor(const EstadoMotor& motor, uint32_t ahora) {
  return motor.ultimoEEC1ms != 0 && ahora - motor.ultimoEEC1ms < cfg::CAN_TIMEOUT_MS;
}

}  // namespace can
