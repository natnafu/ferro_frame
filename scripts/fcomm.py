#!/usr/bin/env python3

import serial

CMD_SET_ALL = "A"  # sets all coils to specified value
CMD_SET_N = "N"  # set the first N coils to the N passed in values
CMD_SET_ONE = "O"  # sets one coil to the specified value
CMD_GET = "G"  # TODO - gets current state

CMD_LIST = [CMD_SET_N, CMD_SET_ONE, CMD_SET_ALL, CMD_GET]

MAX_DUTY = 255
OFF_DUTY = 0


class Fcomm:
    def __init__(self, port="/dev/tty.usbserial-0001", baudrate=115200, timeout=1):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None

    def send(self, command, data):
        if not self.ser:
            print("no serial comms")
            return

        num_coils = len(data)
        assert num_coils <= 256, f"too many coils in data: {num_coils}"

        if command == CMD_SET_ALL or command == CMD_SET_ONE:
            assert num_coils == 1, f"command {command} only allows 1 coil, >1 specified"

        # debug
        # print(f"command {command}")
        # print(f"num_coils {num_coils}")
        # print(f"data {data}")

        self.ser.write(bytes([ord(command)]) + bytes([num_coils]) + bytes(data))
