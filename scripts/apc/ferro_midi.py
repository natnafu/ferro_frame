#!/usr/bin/env python3

import mido
import serial
import threading

"""
    PCBA stuff
"""
MAX_DUTY = 255
OFF_DUTY = 0
# PCBA only supports setting one coil at a time atm
CMD_SET_ONE = 1
# Global variable to store the serial port
ser = None


def update_ferro(coil, duty):
    """
    Updates a single coil
    """
    # translate coil from 8x8 to 16x16
    (x, y) = midi_to_xy(coil, 8)
    coil = xy_to_midi(y, x, 16)

    global ser
    ser.write([CMD_SET_ONE, int(coil), int(duty)])


"""
    MIDI/APC stuff
"""
# sticky = turns off at next note_on
# momentary = turns off at note_off
modes = ["sticky", "momentary"]
mode = "momentary"

# Global variable to store the MIDI port
midi_port = None

# midi velocity is color
colors = {
    "Black": 0,
    "Red": 72,
    "Green": 87,
    "Blue": 41,
    "Yellow": 13,
    "white": 3,
    "Orange": 61,
    "Purple": 44,
    "Brown": 83,
}

# midi channel is brightness
# 0-6 with 6 being full brightness. >6 are various blinking modes
max_brightness = 6

# Make an array of all the coils (1D for now)
coils = [False for x in range(8 * 8)]


def apc_update(coil, color, type="note_on", brightness=max_brightness):
    """
    Updates a single APC button
    """
    global midi_port  # Access the global variable

    with mido.open_output(midi_port, autoreset=True) as port:
        on = mido.Message(
            type,
            note=coil,
            channel=brightness,
            velocity=colors[color],
        )
        print(f"sent: {on}")
        port.send(on)

        update_ferro(coil, 0 if color == "Black" else 255)


def apc_reset():
    """
    Turns off all APC buttons
    """
    for coil in range(0, len(coils)):
        apc_update(coil=coil, color="Black")


def xy_to_midi(x, y, size):
    return x + size * y


def midi_to_xy(midi, size):
    return (midi % size, int(midi / size))


def list_midi_devices():
    """
    Lists all available MIDI devices.
    """
    print("Available MIDI devices:")
    devices = mido.get_input_names()
    assert len(devices) >= 1, "No MIDI device detected"
    for index, device in enumerate(devices):
        print(f"{index + 1}. {device}")
    print()


def select_midi_device():
    """
    Prompts the user to select a MIDI device from the available options.
    Returns the name of the selected device.
    """
    devices = mido.get_input_names()
    list_midi_devices()
    while True:
        try:
            selection = int(
                input("Enter the number of the MIDI device to connect to: ")
            )
            if 1 <= selection <= len(devices):
                return devices[selection - 1]
            else:
                print("Invalid selection. Please enter a valid device number.")
        except ValueError:
            print("Invalid input. Please enter a valid device number.")


def midi_message_handler(message):
    """
    Handles incoming MIDI messages and prints their information.
    """
    print(f"received: {message}")
    if mode == "sticky":
        if message.type == "note_on":
            coils[message.note] = not coils[message.note]
            apc_update(
                coil=message.note,
                color="Blue" if coils[message.note] else "Black",
            )
    elif mode == "momentary":
        if message.type == "note_on":
            coils[message.note] = True
        elif message.type == "note_off":
            coils[message.note] = False
        apc_update(
            coil=message.note,
            color="Blue" if coils[message.note] else "Black",
        )


def midi_listener():
    """
    Connects to the specified MIDI device and listens for MIDI messages.
    """
    global midi_port  # Access the global variable

    with mido.open_input(midi_port) as port:
        print("Connected to MIDI device:", midi_port)
        print("Listening for MIDI messages...")
        apc_reset()
        for message in port:
            midi_message_handler(message)


if __name__ == "__main__":
    midi_port = select_midi_device()
    ser = serial.Serial("/dev/tty.usbserial-0001", baudrate=115200)

    midi_thread = threading.Thread(
        target=midi_listener,
    )
    midi_thread.start()
