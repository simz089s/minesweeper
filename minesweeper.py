#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  minesweeper.py

'''
To do:
	- Auto-clear empty (0) squares when clicked
	- Prevent getting mine on first square click (will probably need big rewrite because of the way the board is generated, or just move the mine and update values)
	- Add right-click marking
	- Add winning
'''

try:
	import Tkinter as tk
	from Tkinter import messagebox
except ImportError:
	import tkinter as tk
	from tkinter import messagebox
import random

class Zone:
	"""Represent a single square on the minesweeper board."""
	
	def __init__(self, mine, val, x, y):
		self.mine = mine
		self.revealed = False
		self.marked = False
		self.value = val
		self.x = x
		self.y = y
	
	def mine(self):
		return self._mine
	
	def revealed(self):
		return self.revealed
	
	def marked(self):
		return self.marked
	
	def value(self):
		return self._value
	
	def x(self):
		return self._x
	
	def y(self):
		return self._y

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
	area = ((x-1,y-1), (x,y-1), (x+1,y-1), (x-1,y), (x+1,y), (x-1,y+1), (x,y+1), (x+1,y+1))
	num_mines = 0
	for neighbor in area:
		if (neighbor in mines): num_mines += 1
	return num_mines

def create_board(size, mines):
	"""Generate a random minesweeper board."""
	mine_coords = []
	for k in range(mines):
		x = random.randint(0, size-1)
		y = random.randint(0, size-1)
		mine_coords.append((x, y))
	
	#~ print(mine_coords)
	
	board = [[None for j in range(size)] for i in range(size)]
	
	for i in range(size):
		for j in range(size):
			if ((j, i) in mine_coords): board[i][j] = Zone(True, "M", j, i)
			else: board[i][j] = Zone(False, check_mines(mine_coords, j, i), j, i)
	
	return board

def print_board(board):
	"""Print board to STDOUT."""
	for i in range(len(board)):
		for j in range(len(board[i])):
			print("%3s" % (board[i][j].value), end=' ')
		print("\n")

def reveal(frame, board, zone):
	"""Reveal square on click.
Lose and exit if the square is a mine."""
	zone_button = tk.Button(frame, bg="grey", fg="black", height=1, width=2, relief="sunken", text=zone.value)
	zone_button.grid(row=zone.y, column=zone.x)
	
	if (zone.value is "M"):
		tk.messagebox.showinfo("KABOOM", "Stepped on a mine.")
		exit(0)

def main_loop():
	"""Main game loop.
Generate board and print it to STDOUT."""
	
	try: N = int(raw_input("Board size? "))
	except NameError: N = int(input("Board size? "))
	board_array = create_board(N, (N*2+1)//3)
	print_board(board_array)
	
	top = tk.Tk()
	
	board_frame = tk.Frame(top, bg="white", height=N, width=2*N)
	board_frame.pack()
	
	for i in range(len(board_array)):
		for j in range(len(board_array[i])):
			zone_button = tk.Button(board_frame, bg="dark blue", command=lambda i=i, j=j:reveal(board_frame, board_array, board_array[i][j]), fg="black", height=1, width=2)
			zone_button.grid(row=i, column=j)
	
	top.mainloop()
	
	return 0

def main(args):
	
	main_loop()
	
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
