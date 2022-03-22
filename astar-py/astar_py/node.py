import json
import random
from typing import Tuple
import pygame
from astar_py.constants import *

class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.state = NodeState.DEFAULT
		self.width = width
		self.total_rows = total_rows
		self.walls = {
		}
		self.neighbors = {
		}


	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.state == NodeState.CLOSED

	def is_open(self):
		return self.state == NodeState.OPEN

	def is_barrier(self):
		return self.state == NodeState.BARRIER

	def is_start(self):
		return self.state == NodeState.START

	def is_end(self):
		return self.state == NodeState.END

	def reset(self):
		self.state = NodeState.DEFAULT

	def make_start(self):
		self.state = NodeState.START

	def make_closed(self):
		self.state = NodeState.CLOSED

	def make_open(self):
		self.state = NodeState.OPEN

	def make_barrier(self):
		self.state = NodeState.BARRIER

	def make_end(self):
		self.state = NodeState.END

	def make_path(self):
		self.state = NodeState.PATH

	def draw(self, win):
		pygame.draw.rect(win, self.state.value, (self.x, self.y, self.width, self.width))
		if WallPlacement.NORTH in self.walls:
			pygame.draw.line(win, BLACK, (self.x, self.y), (self.x + self.width, self.y))
		if WallPlacement.SOUTH in self.walls:
			pygame.draw.line(win, BLACK, (self.x, self.y + self.width), (self.x + self.width, self.y + self.width))
		if WallPlacement.EAST in self.walls:
			pygame.draw.line(win, BLACK, (self.x + self.width, self.y), (self.x + self.width, self.y + self.width))
		if WallPlacement.WEST in self.walls:
			pygame.draw.line(win, BLACK, (self.x, self.y), (self.x, self.y + self.width))

	def update_neighbors(self, grid):
		self.neighbors = {
			WallPlacement.NORTH: None,
			WallPlacement.SOUTH: None,
			WallPlacement.EAST: None,
			WallPlacement.WEST: None
		}
		if self.row < self.total_rows - 1:
			self.neighbors[WallPlacement.EAST] = grid[self.row + 1][self.col]
		if self.row > 0:
			self.neighbors[WallPlacement.WEST] = grid[self.row - 1][self.col]
		if self.col < self.total_rows - 1:
			self.neighbors[WallPlacement.SOUTH] = grid[self.row][self.col + 1]
		if self.col > 0:
			self.neighbors[WallPlacement.NORTH] = grid[self.row][self.col - 1]

	def remove_neighbours_with_walls(self):
		for direction in self.neighbors:
			if (self.neighbors[direction] is not None
			    and direction in self.walls):
				self.neighbors[direction] = None

	def open_walls(self, direction: WallPlacement = None):
		if direction is None:
			self.walls = set()
		else:
			self.walls.remove(direction)

	def add_walls(self, direction: WallPlacement = None):
		if direction is None:
			self.walls = {
				WallPlacement.NORTH,
				WallPlacement.SOUTH,
				WallPlacement.EAST,
				WallPlacement.WEST
			}
		else:
			self.walls.add(direction)

	def __str__(self) -> str:
		return json.dumps(self.__dict__, indent=4, cls=EnumEncoder)

	def __lt__(self, other):
		return False

class EnumEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Enum):
			return obj.name
		if isinstance(obj, set):
			return list(obj)
		if isinstance(obj, Node):
			return json.dumps(self.__dict__, indent=4, cls=EnumEncoder)
		return json.JSONEncoder.default(self, obj)