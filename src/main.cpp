#include <Arduino.h>

#include "command.h"
#include "pins.h"
#include "tlc5940.h"

void setup()
{
  command_init();
  tlc_init();
}

void loop()
{
  command_handler();
}
