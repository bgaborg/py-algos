from queue import PriorityQueue
import pygame
from astar_py import constants
import logging

from astar_py.constants import *
from astar_py.maze_generator import Maze
from astar_py.node import Node

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def solve(draw, grid, start, end):
	count = 0 # tie breaker - which was inserted first
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	# for getting if there's something is in the priority queue fast
	# we need hash to get something in O(1)
	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] # index is 2: get the node from the tuple
		# sync the open_set_hash with the open_set
		open_set_hash.remove(current)

		if current == end:
			# path found
			# we need to reconstruct the path
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		# consider the neighbors of the current node
		for neighbor in current.neighbors.values():
			if neighbor is None:
				continue
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				# we found a better way to the neighbor
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def draw(window, grid, rows, width):
	window.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(window)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	logger.debug(f"pos: {pos}, rows: {rows}, width: {width}, gap: {gap}")
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

class Display:
	def __init__(self, width):
		self.width = width
		self.window = None
		self.grid = None
		self.start = None
		self.end = None
		self.rows = constants.ROWS
		self.maze = Maze(constants.ROWS, width)
		self.grid = self.maze.grid
		window = pygame.display.set_mode((WIDTH, WIDTH))
		pygame.display.set_caption("A* Path Finding Algorithm Visualisation")

	def run(self):
		self.window = pygame.display.set_mode((self.width, self.width))
		self.main(self.window, self.width)

	def main(self, window, width) -> None:
		run = True
		while run:
			draw(window, self.grid, ROWS, width)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				if pygame.mouse.get_pressed()[0]:  # LEFT MOUSE BUTTON
					spot = self.calculate_spot(width, ROWS)
					self.handle_left_click(spot)

				elif pygame.mouse.get_pressed()[2]:  # RIGHT MOUSE BUTTON
					spot = self.calculate_spot(width, ROWS)
					self.handle_right_click(spot)

				if event.type == pygame.KEYDOWN:
					logger.debug(f"event.key: {event.key}")
					self.handle_keydown(window, width, ROWS, event)

		pygame.quit()

	def handle_keydown(self, window, width, ROWS, event):
		if event.key == 13 and self.start and self.end:
			for row in self.grid:
				for spot in row:
					spot.update_neighbors(self.grid)
					spot.remove_neighbours_with_walls()

			solve(lambda: draw(window, self.grid, ROWS, width),
					self.grid, self.start, self.end)

		if event.key == pygame.K_BACKSPACE:
			self.start, self.end = self.maze.generate(lambda: draw(window, self.grid, ROWS, width))


	def calculate_spot(self, width, ROWS) -> Node:
		pos = pygame.mouse.get_pos()
		row, col = get_clicked_pos(pos, ROWS, width)
		return self.grid[row][col]

	def handle_right_click(self, spot):
		spot.reset()
		if spot == self.start:
			self.start = None
		elif spot == self.end:
			self.end = None
		return self.start, self.end

	def handle_left_click(self, spot):
		logger.debug(f"clicked spot: {spot}")
		if not self.start and spot != self.end:
			self.start = spot
			self.start.make_start()

		elif not self.end and spot != self.start:
			self.end = spot
			self.end.make_end()

		return self.start, self.end

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)


def run():
	Display(WIDTH).run()