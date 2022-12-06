#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 18:06:35 2022

@author: RAI\brais.otero.lema
"""

import numpy as np
import matplotlib.pyplot as plt

UNOUN = 0
BLANK = 1
PAINT = 2
CROSS = 3

grid_side = 5
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

def get_hint(paint):
    # Crea a pista que aparecerá na fila ou columna a partir do paint
    hint = ""
    separator = " | "
    for stroke in paint:
        if not stroke == 0:
            hint += str(stroke)
            hint += separator
    if hint == "":
        hint = "0" + separator
    return hint[:len(hint) - len(separator)]

def print_board(board):
    for i in range(grid_side):
        print(f"Columna {i+1}: {get_paint(board[:, i])}")
        print(f"Fila {i+1}: {get_paint(board[i, :])}")

def draw_board(board):
    plt.figure(dpi = grid_side * 10)
    
    # Obtemos as pistas de cada fila e columna
    rowsh, colsh = [], []
    for i in range(grid_side):
        rowsh.append(get_hint(get_paint(board[i, :])))
        colsh.append(get_hint(get_paint(board[:, i])))
    plt.xticks(np.arange(grid_side), np.array(colsh))
    plt.yticks(np.arange(grid_side), np.array(rowsh))
    
    image = np.zeros((grid_side, grid_side, 3))
    image[np.where(board == BLANK)] = [1, 1, 1]
    image[np.where(board == PAINT)] = [0, 0, 0]
    plt.imshow(image)
    plt.show()

def get_input():
    i = input("? ")
    i = i.lower()
    itype = i[0]
    ipos = np.int_(i[1:].split(","))
    pos = (ipos[0], ipos[1])
    if game_board[pos] == PAINT:
        print("Pix already painted.")
        return "invalid"
    if itype == "p":
        if not game_board[pos] == CROSS:
            game_board[pos] = PAINT # debería comprobar si es correcto o no
        else:
            print("Remove cross first.")
            return "invalid"
    elif itype == "c":
        if not game_board[pos] == CROSS:
            game_board[pos] = CROSS
        else:
            print("Already crossed.")
            return "invalid"
    elif itype == "r":
        if not game_board[pos] == BLANK:
            game_board[pos] = BLANK
        else:
            print("Nothing to remove.")
            return "invalid"
    # elif ...


draw_board(target_board)
"""
while get_input() == "invalid": ??
"""

