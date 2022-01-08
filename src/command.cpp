#include <Arduino.h>

#include "tlc5940.h"

#define RX_BUF_SIZE   256
#define RX_TIMEOUT_MS 100

#define CMD_NONE     0
#define CMD_SET_ONE  1
#define CMD_SET_ALL  2

static uint8_t rx_buf[RX_BUF_SIZE];
static uint32_t rx_count;

void command_init() {
  Serial.begin(115200);
}

void command_handler() {
  if (Serial.available()) {
    // Get command
    uint8_t cmd = Serial.read();
    // Get data
    uint32_t cmd_time = millis();
    rx_count = 0;
    while (millis() - cmd_time < RX_TIMEOUT_MS) {
      if (rx_count == RX_BUF_SIZE) break;
      if (Serial.available()) rx_buf[rx_count++] = Serial.read();
    }

    switch(cmd) {
      case CMD_SET_ONE :
        tlc_set(rx_buf[0], rx_buf[1]);
        tlc_update();
    }
  }
}
