#!/usr/bin/env python3

import mido
import threading

# sticky = turns off at next note_on
# momentary = turns off at note_off
modes = ["sticky", "momentary"]
mode = "momentary"

# Global variable to store the MIDI port
midi_port = None

# midi velocity is color
velocity_colors = {
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
channel_brightness = 6

# Make an array of all the coils (1D for now)
coils = [False for x in range(8 * 8)]


def apc_update(coil, type="note_on", brightness=channel_brightness, color="Red"):
    global midi_port  # Access the global variable

    with mido.open_output(midi_port, autoreset=True) as port:
        on = mido.Message(
            type,
            note=coil,
            channel=brightness,
            velocity=velocity_colors[color],
        )
        print(f"sent: {on}")
        port.send(on)


def apc_reset():
    for coil in range(0, len(coils)):
        apc_update(coil=coil, color="Black")


def xy_to_midi(x, y):
    return x + 8 * y


def midi_to_xy(midi):
    return (midi % 8, int(midi / 8))


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

    midi_thread = threading.Thread(
        target=midi_listener,
    )
    midi_thread.start()
