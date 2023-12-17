#!/usr/local/bin/python3.8

import fcomm

import math
import time

ferroframe = fcomm.Fcomm()

SINE_PERIOD_S = 4
MIN_DUTY = 127
MAX_DUTY = 255

# Indicates 9 magnets in a 3x3 40mm grid
coils = [
    (0, 0),
    (0, 2),
    (0, 4),
    (2, 0),
    (2, 2),
    (2, 4),
    (4, 0),
    (4, 2),
    (4, 4),
]

last_time_ms = 0


def set_3x3(duty):
    global last_time_ms
    time_ms = time.time() * 1000
    if time_ms - last_time_ms > fcomm.UPDATE_PERIOD_MS:
        last_time_ms = time_ms
    else:
        return

    # print out full grid
    grid = []
    for row in range(16):
        for col in range(16):
            state = fcomm.OFF_DUTY
            if (row, col) in coils:
                state = duty
            grid.append(state)
    print(duty)
    grid.pop()  # can't send 256, so need to pop off 1 value
    ferroframe.set_n(grid)


if __name__ == "__main__":
    while True:
        current_time = time.time()
        angle = (2 * math.pi * current_time) / SINE_PERIOD_S
        duty = MIN_DUTY + (MAX_DUTY - MIN_DUTY) * 0.5 * (1 + math.sin(angle))
        duty = int(duty)
        set_3x3(duty)
        # ferroframe.read()
