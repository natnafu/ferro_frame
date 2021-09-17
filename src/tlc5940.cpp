#include <Arduino.h>
#include <SPI.h>

#include "tlc5940.h"
#include "pins.h"

// SPI things
#define SPI_CLK               40000000
SPIClass * tlc_spi = NULL;

// GSCLK settings (uses ledc for PWM control)
#define GSCLK_PWM_CHANNEL     0
#define GSCLK_PWM_RESOLUTION  1
#define GSCLK_PWM_DUTY        1
#define GSCLK_FREQ            1000000

// BLANK settings (uses timer and interrupts)
#define ESP32_FREQ            80000000
#define BLANK_TIMER_ID        0
#define BLANK_TIMER_DIV       (ESP32_FREQ / GSCLK_FREQ) // sync to GSCLK freq
hw_timer_t * blank_timer = NULL;

// signals that data is ready to be latched
volatile uint8_t needs_xlat = 0;

// grayscale data
#define NUM_TLCS              16
uint8_t tlc_GSData[NUM_TLCS * 24];

// Pulses BLANK and (if needed) XLAT
void IRAM_ATTR onBlankTimer(){
  set_pin(TLC_BLANK_PIN);
  if (needs_xlat) {
    needs_xlat = 0;
    set_pin(TLC_XLAT_PIN);
    clear_pin(TLC_XLAT_PIN);
  }
  clear_pin(TLC_BLANK_PIN);
}

void tlc_init() {
  // init pins modes
  output_pin(TLC_SIN_PIN);
  output_pin(TLC_SCK_PIN);
  output_pin(TLC_XLAT_PIN);
  output_pin(TLC_BLANK_PIN);
  output_pin(TLC_GSCLK_PIN);

  // init pin states
  set_pin(TLC_BLANK_PIN);
  clear_pin(TLC_XLAT_PIN);
  clear_pin(TLC_SCK_PIN);

  // setup GSCLK
  ledcSetup(GSCLK_PWM_CHANNEL, GSCLK_FREQ, GSCLK_PWM_RESOLUTION);
  ledcAttachPin(TLC_GSCLK_PIN, GSCLK_PWM_CHANNEL);
  ledcWrite(GSCLK_PWM_CHANNEL, GSCLK_PWM_DUTY);

  // setup BLANK
  blank_timer = timerBegin(BLANK_TIMER_ID, BLANK_TIMER_DIV, true);
  timerAttachInterrupt(blank_timer, &onBlankTimer, true);
  timerAlarmWrite(blank_timer, 255, true);
  timerAlarmEnable(blank_timer);

  // setup SPI
  tlc_spi = new SPIClass(VSPI);
  tlc_spi->begin(TLC_SCK_PIN, TLC_CIPO_PIN, TLC_SIN_PIN, TLC_SS_PIN);

  tlc_update();
}

void tlc_update() {
  // wait for last data to be latched
  while (needs_xlat);

  uint8_t *p = tlc_GSData;
  while (p < tlc_GSData + NUM_TLCS * 24) {
      tlc_spi->transfer(*p++);
      tlc_spi->transfer(*p++);
      tlc_spi->transfer(*p++);
  }

  // signal XLAT pulse on next BLANK cycle
  needs_xlat = 1;
}

// borrowed code from arduino lib
void tlc_set(uint8_t channel, uint16_t value) {
    uint8_t index8 = (NUM_TLCS * 16 - 1) - channel;
    uint8_t *index12p = tlc_GSData + ((((uint16_t)index8) * 3) >> 1);
    if (index8 & 1) { // starts in the middle
                      // first 4 bits intact | 4 top bits of value
        *index12p = (*index12p & 0xF0) | (value >> 8);
                      // 8 lower bits of value
        *(++index12p) = value & 0xFF;
    } else { // starts clean
                      // 8 upper bits of value
        *(index12p++) = value >> 4;
                      // 4 lower bits of value | last 4 bits intact
        *index12p = ((uint8_t)(value << 4)) | (*index12p & 0xF);
    }
}

// also borrowed from arduino lib
void tlc_set_all(uint16_t value) {
    uint8_t firstByte = value >> 4;
    uint8_t secondByte = (value << 4) | (value >> 8);
    uint8_t *p = tlc_GSData;
    while (p < tlc_GSData + NUM_TLCS * 24) {
        *p++ = firstByte;
        *p++ = secondByte;
        *p++ = (uint8_t)value;
    }
}
