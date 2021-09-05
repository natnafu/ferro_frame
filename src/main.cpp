#include <Arduino.h>

#include "pins.h"
#include "tlc5940.h"

void setup()
{
  tlc_init();
}

void loop()
{
  for (int i = 0; i < 4096; i++) {
    tlc_set(1, i);
    tlc_update();
  }
}
