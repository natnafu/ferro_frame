#!/usr/bin/env python3

import serial, sys

data = sys.argv[1:]
# Make sure command and data size present
assert len(data) > 0, "missing command"
assert len(data) > 1, "missing data"


command = data[0]
int_data = list(map(int, data[1:]))

ser = serial.Serial("/dev/tty.usbserial-0001", baudrate=115200)
ser.write(bytes([ord(command)]) + bytes([len(int_data)]) + bytes(int_data))
