#!/usr/bin/env python3

import serial, sys

data = sys.argv[1:]
assert len(data) > 0, "No data to send."

for i in range(0, len(data)):
    data[i] = int(data[i])

ser = serial.Serial("/dev/tty.usbserial-0001", baudrate=115200)
ser.write(data)
