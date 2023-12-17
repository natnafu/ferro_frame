#!/usr/bin/env python3

import serial

CMD_SET_ALL = "A"  # sets all coils to specified value
CMD_SET_N = "N"  # set the first N coils to the N passed in values
CMD_SET_ONE = "O"  # sets one coil to the specified value
CMD_GET = "G"  # TODO - gets current state

CMD_LIST = [CMD_SET_N, CMD_SET_ONE, CMD_SET_ALL, CMD_GET]

MAX_DUTY = 255
OFF_DUTY = 0

UPDATE_PERIOD_MS = 100


class Fcomm:
    def __init__(self, port="/dev/tty.usbserial-0001", baudrate=115200, timeout=1):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None

        # make sure all coils are off
        self.set_all(0)

    def set_all(self, duty):
        self.ser.write(bytes([ord(CMD_SET_ALL)]) + bytes(duty))

    def set_one(self, x, y, duty):
        raise RuntimeError("do not use this, ESP returns unknown cmd error")
        assert x < 16, f"invalid x: {x}"
        assert y < 16, f"invalid y: {y}"
        coil = 16 * x + y
        self.ser.write(bytes([ord(CMD_SET_ONE)]) + bytes([coil]) + bytes(duty))

    def set_n(self, duties):
        num_coils = len(duties)
        assert num_coils < 256, f"Only 255 coils allowed, {num_coils} tried"
        self.ser.write(bytes([ord(CMD_SET_N)]) + bytes([num_coils]) + bytes(duties))

    def read(self):
        if self.ser.in_waiting > 0:
            data = self.ser.read(self.ser.in_waiting)
            print(f"RX: {data}\n")
