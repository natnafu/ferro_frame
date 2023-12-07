#!/usr/bin/env python3

import math, serial, sys, time

data = sys.argv[1:]
# Make sure command and data size present
assert len(data) > 0, "missing command"
assert len(data) > 1, "missing data"

command = data[0]
int_data = list(map(int, data[1:]))
ser = serial.Serial("/dev/tty.usbserial-0001", baudrate=115200)

if command == "pulse":
    # run demo
    coil = int_data[0]

    amplitude = 255
    frequency = 1  # Hz
    interval = 0.01  # seconds (100 milliseconds)

    start_time = time.time()
    elapsed_time = 0

    while True:
        duty = int(
            amplitude / 2
            + amplitude / 2 * math.sin(2 * math.pi * frequency * elapsed_time)
        )
        print(int(duty))
        ser.write(bytes([ord("O")] + [2] + [coil] + [duty]))
        elapsed_time = time.time() - start_time
        time.sleep(interval)
else:
    # send raw command to ESP
    ser.write(bytes([ord(command)]) + bytes([len(int_data)]) + bytes(int_data))
