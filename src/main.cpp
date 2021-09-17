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
  // test program: pulses
  static uint8_t val = 0;
  static int8_t dir = 1;
  tlc_set_all(val);
  val = val + dir;
  tlc_update();
  if (val == 255 || val == 0) dir = dir * -1;
}
