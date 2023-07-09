#!/usr/bin/env python3
"""
Send random notes to the output port.
"""

import random
import sys
import time

import mido
from mido import Message

if len(sys.argv) > 1:
    portname = sys.argv[1]
else:
    portname = None  # Use default port


note = 0
velocity_colors = {
    "Red": 72,
    "Green": 87,
    "Blue": 41,
    "Yellow": 13,
    "white": 3,
    "Orange": 61,
    "Purple": 44,
    "Brown": 83,
}

try:
    with mido.open_output(portname, autoreset=True) as port:
        print(f"Using {port}")

        for channel in range(0, 7):
            for velocity in colors.values():
                on = Message("note_on", note=note, channel=channel, velocity=velocity)
                print(f"Sending {on}")
                port.send(on)
                note += 1
                time.sleep(0.001)

except KeyboardInterrupt:
    pass

print()
0
0
