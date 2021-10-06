#include <Arduino.h>

#include "pins.h"
#include "tlc5940.h"

void setup()
{
  tlc_init();
  tlc_update();
}

void loop()
{
  static uint8_t coil;
  tlc_clear_all();
  tlc_set(coil++, 25);
  tlc_update();
  delay(100);
}
