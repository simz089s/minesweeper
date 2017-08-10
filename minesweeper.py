#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  minesweeper.py

'''
To-do:
	- Add timer (and mine count?)
	- Prevent getting mine on first square click (will probably need big rewrite because of the way the board is generated, or just move the mine and update values)
	- Stop console from appearing (kept for debugging purposes)
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
	
	def button(self):
		return self.button

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

# Keep track of squares left to win
total_mines = 0
squares_left = 1

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
	
	global total_mines
	total_mines = len(set(mine_coords))
	
	board = [[None for j in range(size)] for i in range(size)]
	
	global squares_left
	squares_left = size * size
	
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

def clear_adjacent(board, root_zone):
	queue = [root_zone]
	visited = set()
	
	while (queue):
		current_zone = queue.pop(0)
		x = current_zone.x
		y = current_zone.y
		neighborhood = ((x-1,y-1), (x,y-1), (x+1,y-1), (x-1,y), (x+1,y), (x-1,y+1), (x,y+1), (x+1,y+1))
		for n in neighborhood:
			if (n[0] < 0) or (n[1] < 0): continue
			try:
				adjacent_zone = board[n[1]][n[0]]
				if (adjacent_zone not in visited):
					if (adjacent_zone.value == 0): queue += [adjacent_zone]
					if (adjacent_zone.value != 'M'): reveal(adjacent_zone.button.master, board, adjacent_zone, False)
					visited.add(adjacent_zone)
			except IndexError: continue

def reveal(frame, board, zone, bfs):
	"""Reveal square on click.
Lose and exit if the square is a mine.
Win and disable buttons when all squares except mines are cleared."""
	#~ zone.button = tk.Button(frame, bg="grey", fg="black", height=1, width=2, relief="sunken", text=zone.value)
	#~ # zone_button.grid(row=zone.y, column=zone.x)
	# zone_button = frame.grid_slaves(row=zone.y, column=zone.x)[0]
	zone.button.config(bg="grey")
	zone.button.config(relief="sunken")
	zone.button.config(text=zone.value)
	zone.button.config(command=None)
	zone.button.unbind("<Button-3>")
	
	if (zone.value is "M"):
		tk.messagebox.showinfo("KABOOM", "Stepped on a mine.")
		exit(0)
	
	if (not zone.revealed):
		global squares_left
		global total_mines
		squares_left -= 1
		zone.revealed = True
	if (squares_left == total_mines):
		tk.messagebox.showinfo("CLEAR", "You win!")
		for b in frame.winfo_children():
			b.configure(state="disabled")
			b.unbind("<Button-3>")
	if (bfs) and (zone.value == 0):
		clear_adjacent(board, zone)

def mark_zone(event):
	"""Mark a square as a mine with right-click."""
	zone_button = event.widget
	
	#~ prev_command = zone_button.cget('command')
	#~ prev_parent = zone_button.master
	#~ grid_info = zone_button.grid_info()
	
	#~ zone_button = tk.Button(prev_parent, bg="dark red", command=prev_command, fg="black", height=1, width=2)
	#~ zone_button.grid(row=grid_info["row"], column=grid_info["column"])
	zone_button.configure(bg="dark red")
	
	zone_button.config(state="disabled")
	zone_button.bind('<Button-3>',  unmark_zone)
	
	zone_button.marked = True

def unmark_zone(event):
	"""Unmark a square as a mine with right-click."""
	zone_button = event.widget
	
	#~ prev_command = zone_button.cget('command')
	#~ prev_parent = zone_button.master
	#~ grid_info = zone_button.grid_info()
	
	#~ zone_button = tk.Button(prev_parent, bg="dark blue", command=prev_command, fg="black", height=1, width=2)
	#~ zone_button.grid(row=grid_info["row"], column=grid_info["column"])
	zone_button.configure(bg="dark blue")
	
	zone_button.config(state="normal")
	zone_button.bind('<Button-3>',  mark_zone)
	
	zone_button.marked = False

def main_loop():
	"""Main game loop.
Generate board and print it to STDOUT."""
	
	try:
		N = abs(int(raw_input("Board size? ")))
		M = min(abs(int(raw_input("Difficulty (0-3)? "))), 3)
	except NameError:
		N = abs(int(input("Board size? ")))
		M = min(abs(int(input("Difficulty (0-3)? "))), 3)
	N = min(N, 20) # Hard capped at 20 for performance
	board_array = create_board(N, int(N*N*M/9+1))
	
	print_board(board_array)
	
	top = tk.Tk()
	
	board_frame = tk.Frame(top, bg="white", height=N, width=2*N)
	board_frame.pack()
	
	for i in range(len(board_array)):
		for j in range(len(board_array[i])):
			zone_button = tk.Button(board_frame, bg="dark blue", command=lambda i=i, j=j:reveal(board_frame, board_array, board_array[i][j], True), fg="black", height=1, width=2)
			zone_button.grid(row=i, column=j)
			zone_button.bind('<Button-3>',  mark_zone)
			board_array[i][j].button = zone_button
	
	top.mainloop()
	
	return 0

def main(args):
	
	main_loop()
	
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
