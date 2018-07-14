#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  minesweeper_pygame.py
'''
Minesweeper
'''
from __future__ import print_function
import random
import sys
import time
import pygame
# from pygame.locals import *

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

width = 20
height = 20
margin = 5
SIZE = 20
board = []


'''
To-do:
    - PORT TO PYGAME (instead of tk)
    - Add timer (and mine count?)
    - Prevent getting mine on first square click (will probably need big rewrite
      because of the way the board is generated, or just move the mine and
      update values)
    - Stop console from appearing (kept for debugging purposes)
    - Maybe fix "You win" dialog from appearing multiple times when repeatedly
      called by BFS revealing (I think)
'''


# Init pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((SIZE*(width+margin)+margin, SIZE*(width+margin)+margin))
pygame.display.set_caption('Minesweeper')
clock = pygame.time.Clock()

# Keep track of squares left to win
total_mines = 0
squares_left = 1


class Zone():
    """Represent a single square on the minesweeper board."""
    def __init__(self, mine, val, x, y, rect):
        self.mine = mine
        self.revealed = False
        self.marked = False
        self.value = val
        self.x = x
        self.y = y
        # self.button = None
        self.rect = rect


'''
   y
   _________________________
  |                         |
x  i0[ j0, j1, j2, j3, ... ]

   i1[                     ]

   i2[                     ]

   i3[                     ]

   ...
  |_________________________|

i=y=row, j=x=col

So that when indexing we can do i,j and row,col but this gives us array[y][x]
'''


def check_mines(mines, x, y):
    """Check for the number of mines in the 8 surrounding squares."""
    neighborhood = {(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1),
            (x, y+1), (x+1, y+1)}
    num_mines = 0
    for neighbor in neighborhood:
        if neighbor in mines:
            num_mines += 1
    return num_mines


def generate_board(mines):
    """Generate a random minesweeper board."""
    mine_coords = []
    for _ in range(mines):
        x = random.randint(0, SIZE-1)
        y = random.randint(0, SIZE-1)
        if (x,y) not in ((0,0), (0,SIZE-1), (SIZE-1,0), (SIZE-1,SIZE-1)):
            mine_coords.append((x, y))

    global total_mines
    total_mines = len(set(mine_coords))

    global squares_left
    squares_left = SIZE * SIZE

    global board
    board = [[None for j in range(SIZE)] for i in range(SIZE)]
    offset = width+margin
    for i in range(SIZE):
        board.append([])
        for j in range(SIZE):
            if (j, i) in mine_coords:
                board[i][j] = Zone(True, "M", j, i, pygame.Rect(margin+i*offset, margin+j*offset, width, height))
                # board.append(Zone(True, "M", j, i))
            else:
                board[i][j] = Zone(False, check_mines(mine_coords, j, i), j, i, pygame.Rect(margin+i*offset, margin+j*offset, width, height))
                # board.append(Zone(False, check_mines(mine_coords, j, i), j, i))

    return mine_coords


def print_board():
    """Pretty print board to stdout."""
    for i in range(len(board)):
        for j in range(len(board[i])):
            print("%3s" % (board[i][j].value), end=' ')
        print("\n")


def clear_adjacent(board, root_zone, mine_coords):
    """Clear area around clicked zone."""
    queue = [root_zone]
    visited = set()

    while queue:
        current_zone = queue.pop(0)
        x = current_zone.x
        y = current_zone.y
        neighborhood = {(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y),
                        (x-1, y+1), (x, y+1), (x+1, y+1)}
        for n in neighborhood:
            if (n[0] < 0) or (n[1] < 0):
                continue
            try:
                adjacent_zone = board[n[1]][n[0]]
                if adjacent_zone not in visited:
                    if adjacent_zone.value == 0:
                        queue += [adjacent_zone]
                    if adjacent_zone.value != 'M':
                        reveal(adjacent_zone.button.master, board,
                               adjacent_zone, False, mine_coords)
                    visited.add(adjacent_zone)
            except IndexError:
                continue


def reveal(frame, board, zone, bfs, mine_coords):
    """
    Reveal square on click.

    Lose and exit if the square is a mine.
    Win and disable buttons when all squares except mines are cleared.
    """
    #~ global BUTTON_WIDTH
    #~ zone.button = tk.Button(frame, bg="grey", fg="black", height=1, width=BUTTON_WIDTH, relief="sunken", text=zone.value)
    #~ # zone_button.grid(row=zone.y, column=zone.x)
    # zone_button = frame.grid_slaves(row=zone.y, column=zone.x)[0]
    zone.button.config(bg="grey")
    zone.button.config(relief="sunken")
    zone.button.config(text=zone.value)
    zone.button.config(command=None)
    zone.button.unbind("<Button-3>")

    if zone.value is "M":
        tkMessageBox.showinfo("KABOOM", "Stepped on a mine.")
        for coord in mine_coords:
            current_mine_zone = board[coord[1]][coord[0]]
            current_mine_zone.button.config(bg="dark red")
            current_mine_zone.button.config(text=current_mine_zone.value)
        for b in frame.winfo_children():
            b.configure(state="disabled")
            b.unbind("<Button-3>")

    if not zone.revealed:
        global squares_left
        # global total_mines
        squares_left -= 1
        zone.revealed = True
    if squares_left == total_mines:
        tkMessageBox.showinfo("CLEAR", "You win!")
        for b in frame.winfo_children():
            b.configure(state="disabled")
            b.unbind("<Button-3>")
    if (bfs) and (zone.value == 0):
        clear_adjacent(board, zone, mine_coords)


def mark_zone(event):
    """Mark a square as a mine with right-click."""
    zone_button = event.widget

    #~ prev_command = zone_button.cget('command')
    #~ prev_parent = zone_button.master
    #~ grid_info = zone_button.grid_info()

    #~ global BUTTON_WIDTH
    #~ zone_button = tk.Button(prev_parent, bg="dark red", command=prev_command, fg="black", height=1, width=BUTTON_WIDTH)
    #~ zone_button.grid(row=grid_info["row"], column=grid_info["column"])
    zone_button.configure(bg="dark red")

    zone_button.config(state="disabled")
    zone_button.bind('<Button-3>', unmark_zone)

    zone_button.marked = True


def unmark_zone(event):
    """Unmark a square as a mine with right-click."""
    zone_button = event.widget

    #~ prev_command = zone_button.cget('command')
    #~ prev_parent = zone_button.master
    #~ grid_info = zone_button.grid_info()

    #~ global BUTTON_WIDTH
    #~ zone_button = tk.Button(prev_parent, bg="dark blue", command=prev_command, fg="black", height=1, width=BUTTON_WIDTH)
    #~ zone_button.grid(row=grid_info["row"], column=grid_info["column"])
    zone_button.configure(bg="dark blue")

    zone_button.config(state="normal")
    zone_button.bind('<Button-3>', mark_zone)

    zone_button.marked = False


def main_loop():
    """
    Main game loop.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                i = pos[0] // (width + margin)
                j = pos[1] // (height + margin)
                board[i][j].revealed = True
        
        # Game logic


        # Screen clearing
        DISPLAYSURF.fill(BLACK)

        # Drawing code
        for i in range(SIZE):
            for j in range(SIZE):
                color = ()
                if board[i][j].revealed:
                    color = WHITE
                elif board[i][j].marked:
                    color = RED
                else:
                    color = BLUE
                pygame.draw.rect(DISPLAYSURF, color, board[i][j].rect)

        pygame.display.update()

        # 60 frames per second
        clock.tick(60)

    return 0


def main(args):
    '''
    Main method.
    '''
    try:
        N = abs(int(raw_input("Board size? ")))
        M = min(abs(int(raw_input("Difficulty (0-3)? "))), 3)
    except NameError:
        N = abs(int(input("Board size? ")))
        M = min(abs(int(input("Difficulty (0-3)? "))), 3)
    N = min(N, 20)  # Hard capped at 20 for performance
    global SIZE
    SIZE = N

    mine_coords = generate_board(int(N*N*M/9+1))
    print_board()

    # for i in range(len(board_array)):
    #     for j in range(len(board_array[i])):
    #         zone_button = tk.Button(board_frame, bg="dark blue", command=lambda
    #                                 i=i, j=j: reveal(board_frame, board_array,
    #                                 board_array[i][j], True, mine_coords),
    #                                 fg="black", height=1, width=BUTTON_WIDTH)
    #         zone_button.grid(row=i, column=j)
    #         zone_button.bind('<Button-3>', mark_zone)
    #         board_array[i][j].button = zone_button
    main_loop()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
