#include <Arduino.h>

#include "tlc5940.h"

#define RX_TIMEOUT_MS 100

#define CMD_SET_N 'N'   // sets the first N coils to the N passed in values
#define CMD_SET_ONE 'O' // sets one coil to the specified value
#define CMD_SET_ALL 'A' // sets all coils to 0
#define CMD_GET 'G'     // TODO

void command_init()
{
  Serial.begin(115200);
}

void commmand_process(char command, const char *data, int dataSize)
{
  // Process the received command and data
  switch (command)
  {

  case CMD_SET_N:
    Serial.printf("CMD_SET_N: setting first %i coils\n", dataSize);
    for (int i = 0; i < dataSize; i++)
    {
      tlc_set(i, data[i]);
    }
    tlc_update();
    break;

  case CMD_SET_ONE:
    if (dataSize != 2)
    {
      Serial.printf("ERROR: CMD_SET_ONE needs 2 values but %i given\n", dataSize);
    }
    else
    {
      Serial.printf("CMD_SET_ONE: SET coil %i to %i\n", data[0], data[1]);
      tlc_set(data[0], data[1]);
      tlc_update();
    }
    break;

  case CMD_SET_ALL:
    if (dataSize != 1)
    {
      Serial.printf("ERROR: CMD_SET_ALL needs 1 value but %i given\n", dataSize);
    }
    else
    {
      Serial.printf("CMD_SET_ALL: set all coilds to %i\n", data[0]);
      tlc_set_all(data[0]);
      tlc_update();
    }
    break;

  case CMD_GET:
    // TODO - send back the current state of the coils
    break;

  default:
    // Unknown command
    Serial.println("ERROR: Unknown cmd");
    break;
  }
}

void command_handler()
{
  if (Serial.available() >= 2)
  {
    unsigned long startTime = millis(); // Record the start time

    char command = Serial.read();
    int dataSize = Serial.read();

    while (Serial.available() < dataSize)
    {
      if (millis() - startTime >= RX_TIMEOUT_MS)
      {
        // Timeout occurred, exit the loop
        Serial.println("ERROR: RX timeout");
        break;
      }
      delay(1); // Wait for more data to be available
    }

    if (Serial.available() >= dataSize)
    {
      char data[dataSize];
      for (int i = 0; i < dataSize; i++)
      {
        data[i] = Serial.read();
      }
      commmand_process(command, data, dataSize);
    }
  }
}
