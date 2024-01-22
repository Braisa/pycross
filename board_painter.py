# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 19:17:49 2024

@author: brais
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys, os
from matplotlib.widgets import Button, TextBox

BLANK = 1
PAINT = 2

colors = {
    BLANK : [1, 1, 1],
    PAINT : [0, 0, 0]
}

# As inputs mapéanse ós botóns de matplotlib event
inputs = {
    "paint" : 1,
    "erase" : 3,
    "lock" : 2
}

path = os.path.dirname(__file__) + "\\"

def select_board(): # dataset
    side = int(input("Select the side of the board: "))
    return side

grid_side = select_board()
max_strokes = int(np.ceil(grid_side/2))
grid_shape = (grid_side, grid_side)

canvas = np.ones(grid_shape)

def draw_board(fig, ax, side = grid_side):
    # Moves grid
    ax.set_xticks(np.arange(grid_side) + .5, minor = True)
    ax.tick_params(axis = "x", which = "minor", length = 0)
    ax.grid(axis = "x", which = "minor")
    ax.set_yticks(np.arange(grid_side) + .5, minor = True)
    ax.tick_params(axis = "y", which = "minor", length = 0)
    ax.grid(axis = "y", which = "minor")
    # Adds wider gridlines
    for j in range(grid_side//5):
        ax.axhline(j*5 + 4.5, color = "gray", linewidth = 1.5)
        ax.axvline(j*5 + 4.5, color = "gray", linewidth = 1.5)
    
    image = np.ones((grid_side, grid_side, 3))
    image[np.where(canvas == PAINT)] = colors[PAINT]
    
    ax.imshow(image)
    fig.canvas.draw()
    
    return image

mpl.rcParams["toolbar"] = "None"
fig, ax = plt.subplots(dpi = max(grid_side, 100))#, layout = "constrained")
draw_board(fig, ax)

def save_canvas(text, board = canvas):
    name = text + ".png"
    if name == "" or os.path.isfile(name):
        print("File already exists or incorrect file name.")
    else:
        plt.imsave(name, draw_board(fig, ax))
        print(f"File saved as {name}.")

save_box = TextBox(plt.axes([.3, .9, .5, .075]), "Name ")
save_box.on_submit(save_canvas)

def mouse_to_board(x, y):
    board_x, board_y = np.int_((x + .5, y + .5))
    return (board_x, board_y)

def on_click(event):
    # Check if click is on board
    if event.inaxes == ax:
        # Cambiado pola lóxica indicial das matrices
        pos = mouse_to_board(event.ydata, event.xdata)
        if event.button == inputs["paint"]:
            canvas[pos] = PAINT
        elif event.button == inputs["erase"]:
            canvas[pos] = BLANK
        ax.clear()
        draw_board(fig, ax)

# cid : connection id
cid = fig.canvas.mpl_connect("button_press_event", on_click)
