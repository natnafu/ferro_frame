#include <Arduino.h>

#include "command.h"
#include "pins.h"
#include "tlc5940.h"

#define DELAY_MS 10

void setup()
{
  command_init();
  tlc_init();
}

void loop()
{
  //command_handler();
  static int row = 1;
  static int col = 1;
  static int dir = 1;
  tlc_clear_all();
  tlc_set(col + row*16, 255);
  tlc_update();
  delay(DELAY_MS);

  row += dir;
  if (row == 15) {
    // row--;
    dir = -1;
    col++;
  }
  else if (row == 0) {
    // row++;
    dir = 1;
    col++;
  }

  if (col == 15) {
    while (col != 1) {
      col--;
      tlc_clear_all();
      tlc_set(col + row*16, 255);
      tlc_update();
      delay(DELAY_MS);
    }
  }
}
