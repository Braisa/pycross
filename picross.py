#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 18:06:35 2022

@author: RAI\brais.otero.lema
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

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

inputs = {
    "paint" : "p",
    "paint_stroke" : "s",
    "cross" : "c",
    "remove_cross" : "r"
}

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

def draw_board(board = game_board, target = target_board):
    plt.figure(dpi = grid_side * 10)
    
    # Obtemos as pistas de cada fila e columna
    rowsh, colsh = [], []
    for i in range(grid_side):
        rowsh.append(get_hint(get_paint(target[i, :])))
        colsh.append(get_hint(get_paint(target[:, i])))
    plt.xticks(np.arange(grid_side), np.array(colsh))
    plt.yticks(np.arange(grid_side), np.array(rowsh))
    
    image = np.zeros((grid_side, grid_side, 3))
    image[np.where(board == UNOUN)] = colors[UNOUN]
    image[np.where(board == BLANK)] = colors[BLANK]
    image[np.where(board == PAINT)] = colors[PAINT]
    image[np.where(board == CROSS)] = colors[CROSS]
    image[np.where(board == ERROR)] = colors[ERROR]
    plt.imshow(image)
    plt.show()

def check_victory(board = game_board, target = target_board):
    # Need to change UNOUN, CROSS and ERROR to BLANK
    compare = board.copy()
    compare[np.where(board == UNOUN)] = BLANK
    compare[np.where(board == CROSS)] = BLANK
    compare[np.where(board == ERROR)] = BLANK
    
    if np.all(compare == target):
        return True
    else:
        return False

def print_instructions(input_map = inputs):
    print("In order to win, you need to paint all blocks.")
    print("The numbers on each row and column indicate the amount of blocks there are.")
    print("If there are multiple numbers, then there are multiple strokes.")
    print("Strokes are separated from each other by at least one blank space.")
    print("\n")
    print("In order to make an input, you must type a key and a position.")
    print("To paint a block, the key is", inputs["paint"])
    #print("To paint an entire stroke, the key is,", inputs["paint_stroke"])
    print("To mark a cross, the key is", inputs["cross"])
    print("To remove a cross, the key is", inputs["remove_cross"])
    print("For example, if you want to paint the block at position (1,2), then you would input:")
    print("Input? p1,2")
    print("\n")

def get_input(board = game_board, target = target_board, input_map = inputs):
    i = input("Input? ")
    i = i.lower()
    itype = i[0]
    ipos = np.int_(i[1:].split(","))
    pos = (ipos[0]-1, ipos[1]-1)
    if board[pos] == PAINT:
        print("Pix already painted.")
        return "invalid"
    if itype == input_map["paint"]:
        if not board[pos] == CROSS:
            if target[pos] == PAINT:
                # Correct
                board[pos] = PAINT
            else:
                # Incorrect
                board[pos] = ERROR
        else:
            print("Remove cross first.")
            return "invalid"
    elif itype == input_map["cross"]:
        if not board[pos] == CROSS:
            board[pos] = CROSS
        else:
            print("Already crossed.")
            return "invalid"
    elif itype == input_map["remove_cross"]:
        if not board[pos] == UNOUN:
            board[pos] = UNOUN
        else:
            print("Nothing to remove.")
            return "invalid"
    # elif ...


print_instructions()
draw_board()
while True:
    while get_input() == "invalid":
        pass
    draw_board()
    if check_victory():
        print("Completed!")
        sys.exit()

