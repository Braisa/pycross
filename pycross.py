# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 22:21:33 2023

@author: Brais
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys, os
import tkinter as tk
from tkinter import ttk

UNOUN = 0
BLANK = 1
PAINT = 2
CROSS = 3
ERROR = 4

colors = {
    UNOUN : [1, 1, 1],
    BLANK : [1, 1, 1],
    PAINT : [0, 0, 0],
    CROSS : [1, 1, 0],
    ERROR : [1, 0, 0]
}

# As inputs mapéanse ós botóns de matplotlib event
inputs = {
    "paint" : 1,
    "cross" : 3
}

path = os.path.dirname(__file__) + "\\"

def select_board(): # dataset
    side = int(input("Select the side of the board: "))
    return side

grid_side = select_board()
max_strokes = int(np.ceil(grid_side/2))
grid_shape = (grid_side, grid_side)

target_board = np.random.randint(BLANK, PAINT+1, size = grid_shape)
game_board = np.zeros_like(target_board)

def get_paint(line):
    # 2 x max_strokes array
    # A primeira fila indica o número de stroke
    # A segunda fila almacena o número de bloques do stroke
    paint = np.int_(np.vstack((np.arange(max_strokes), np.zeros(max_strokes))))
    stroke = 0
    for pix in line:
        if pix == PAINT:
            paint[1, stroke] += 1
        elif pix == BLANK and paint[1, stroke] > 0:
            stroke += 1
    
    return paint[1, :] # Devolve só os bloques de cada stroke

def get_hint(paint, separator):
    # Crea a pista que aparecerá na fila ou columna a partir do paint
    hint = ""
    for stroke in paint:
        if not stroke == 0:
            hint += str(stroke)
            hint += separator
    if hint == "":
        hint = "0" + separator
    return hint[:len(hint) - len(separator)]

def draw_board(fig, ax, board = game_board, target = target_board):
    # Obtemos as pistas de cada fila e columna
    rowsh, colsh = [], []
    for i in range(grid_side):
        rowsh.append(get_hint(get_paint(target[i, :]), " "))
        colsh.append(get_hint(get_paint(target[:, i]), "\n"))
    ax.set_xticks(np.arange(grid_side))
    ax.set_xticklabels(np.array(colsh), rotation = 0)
    ax.set_yticks(np.arange(grid_side))
    ax.set_yticklabels(np.array(rowsh))
    
    ax.xaxis.set_ticks_position("top")
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
    
    image = np.zeros((grid_side, grid_side, 3))
    image[np.where(board == UNOUN)] = colors[UNOUN]
    image[np.where(board == BLANK)] = colors[BLANK]
    image[np.where(board == PAINT)] = colors[PAINT]
    image[np.where(board == CROSS)] = colors[CROSS]
    image[np.where(board == ERROR)] = colors[ERROR]
    
    ax.imshow(image)
    fig.canvas.draw()

def cross_line(roc : str, idx : int, board = game_board):
    if roc == "r" or roc == "row":
        pos = np.where(board[idx, :] == UNOUN)
        board[idx, pos] = CROSS
    elif roc == "c" or roc == "col" or roc == "column":
        pos = np.where(board[:, idx] == UNOUN)
        board[pos, idx] = CROSS

def check_completed(pos : tuple, board = game_board, target = target_board):
    # Need to change UNOUN, CROSS and ERROR to BLANK
    compare = board.copy()
    compare[np.where(board == UNOUN)] = BLANK
    compare[np.where(board == CROSS)] = BLANK
    compare[np.where(board == ERROR)] = BLANK
    
    # Checks row
    if np.all(compare[pos[0], :] == target[pos[0], :]):
        cross_line("r", pos[0])
    
    # Checks column
    if np.all(compare[:, pos[1]] == target[:, pos[1]]):
        cross_line("c", pos[1])

def check_victory(board = game_board, target = target_board):
    # Need to change UNOUN, CROSS and ERROR to BLANK
    compare = board.copy()
    compare[np.where(board == UNOUN)] = BLANK
    compare[np.where(board == CROSS)] = BLANK
    compare[np.where(board == ERROR)] = BLANK
    
    return np.all(compare == target)

mpl.rcParams["toolbar"] = "None"
fig, ax = plt.subplots(dpi = max(grid_side, 100), layout = "constrained")
draw_board(fig, ax)

def mouse_to_board(x, y):
    board_x, board_y = np.int_((x + .5, y + .5))
    return (board_x, board_y)

def on_click(event, board = game_board, target = target_board):
    # Cambiado pola lóxica indicial das matrices
    pos = mouse_to_board(event.ydata, event.xdata)
    # Non hai match/case en python 3.8
    if not board[pos] == PAINT:
        if event.button == inputs["paint"]:
            if target[pos] == PAINT:
                # Correcto
                board[pos] = PAINT
            else:
                # Incorrecto
                board[pos] = ERROR
        elif event.button == inputs["cross"]:
            if not board[pos] == ERROR:
                if not board[pos] == CROSS:
                    board[pos] = CROSS
                else:
                    board[pos] = UNOUN
    # Comproba se a liña ou columna foi completada para recheala
    check_completed(pos, board = board)
    ax.clear()
    draw_board(fig, ax, board = board)
    if check_victory(board = board):
        print("Finished!")

# cid : connection id
cid = fig.canvas.mpl_connect("button_press_event", on_click)
