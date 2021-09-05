#ifndef PINS_H
#define PINS_H

// TLC4950 pins
#define TLC_SIN_PIN    23
#define TLC_SCK_PIN    18
#define TLC_XLAT_PIN   12
#define TLC_BLANK_PIN  15
#define TLC_GSCLK_PIN  2
#define TLC_CIPO_PIN   19 // dummy
#define TLC_SS_PIN     5  // dummy

#define output_pin(pin)  pinMode(pin, OUTPUT)
#define set_pin(pin)     digitalWrite(pin, HIGH)
#define clear_pin(pin)   digitalWrite(pin, LOW)

#endif
