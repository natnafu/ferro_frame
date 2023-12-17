#!/usr/local/bin/python3.8

import fcomm

import math
import tkinter
import time

GRID_SIZE_PX = 500
BOX_SIZE_PX = GRID_SIZE_PX / 16

last_x = -1
last_y = -1
last_time_ms = 0


def motion(event):
    global last_x
    global last_y
    global last_time_ms

    # convert coordinates to bounded boxes
    x, y = math.floor(event.x / BOX_SIZE_PX), math.floor(event.y / BOX_SIZE_PX)

    # don't create events if x or y values are out of bounds
    if x > 15 or y > 15:
        return

    # translate x and y to make trackpad match grid orientation when cables are
    # pointing away.
    x = 15 - x
    # y = 15 - y

    time_ms = time.time() * 1000
    if time_ms - last_time_ms > fcomm.UPDATE_PERIOD_MS:
        last_time_ms = time_ms
    else:
        return

    # Only do things if coordinates have changed
    if x != last_x or y != last_y:
        print(f"{x}, {y}")
        last_x = x
        last_y = y

        # print out full grid
        grid = []
        for row in range(16):
            for col in range(16):
                state = fcomm.OFF_DUTY
                if x == row and y == col:
                    state = fcomm.MAX_DUTY
                grid.append(state)
        print(grid)
        grid.pop()  # can't send 256, so need to pop off 1 value
        ferroframe.set_n(grid)


ferroframe = fcomm.Fcomm()

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("16x16 Grid Window")

    canvas = tkinter.Canvas(root, width=GRID_SIZE_PX, height=GRID_SIZE_PX)
    canvas.pack()

    # Drawing a 16x16 grid
    for i in range(16):
        canvas.create_line(0, i * BOX_SIZE_PX, GRID_SIZE_PX, i * BOX_SIZE_PX)
        canvas.create_line(i * BOX_SIZE_PX, 0, i * BOX_SIZE_PX, GRID_SIZE_PX)

    # Adding text to each cell
    for row in range(16):
        for col in range(16):
            text = f"{row + 16 * col}"
            canvas.create_text(
                col * BOX_SIZE_PX + BOX_SIZE_PX / 2,
                row * BOX_SIZE_PX + BOX_SIZE_PX / 2,
                text=text,
            )

    canvas.bind("<Motion>", motion)

    root.mainloop()
