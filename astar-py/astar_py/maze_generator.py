
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from curses import qiflush
import json
import pickle
from queue import Queue
import random
import time
from typing import Tuple
from astar_py.constants import WallPlacement
from astar_py.node import Node


class Maze:
    def __init__(self, rows, width):
        self.rows = rows
        self.width = width
        self.grid = self.__make_grid(self.rows, self.width)
        self.start = None
        self.end = None

    def __make_grid(self, rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                node = Node(i, j, gap, rows)
                grid[i].append(node)
        return grid

    def generate(self, draw) -> tuple[Node, Node]:
        maze_generator: MazeGenerator = KruskalsGenerator(self)
        return maze_generator.generate_maze(draw)

    def remove_neighbours(self):
        for row in self.grid:
            for node in row:
                node.remove_all_neighbors()

class MazeGenerator(ABC):
    def __init__(self, maze: Maze):
        self.maze = maze

    @abstractmethod
    def generate_maze(self) -> None:
        """Generate paths through a maze."""
        raise NotImplemented

class Wall:
    def __init__(self, from_node: Node, position: WallPlacement):
        self.from_node = from_node
        self.position = position

class KruskalsGenerator(MazeGenerator):
    """MazeGenerator subclass that generates mazes using a modified version of Kruskal's algorithm."""

    def generate_maze(self, draw) -> None:
        """Generate paths through a maze using a modified version of Kruskal's algorithm."""
        grid = self.maze.grid

        sets = DisjointSet()
        all_nodes = [item for sublist in grid for item in sublist]
        sets.make_set(all_nodes)

        walls = deque()
        for node in all_nodes:
            node.reset()
            node.add_walls()
            node.update_neighbors(grid)
            walls.extend([Wall(node, w) for w in node.walls])
        random.shuffle(walls)

        start_node = all_nodes[0]
        end_node = all_nodes[-1]
        start_node.make_start()
        end_node.make_end()

        print("Generating maze...")
        while len(walls) > 0:
            wall: Wall = walls.pop()
            other_node = wall.from_node.neighbors[wall.position]
            if other_node and sets.find(wall.from_node) != sets.find(other_node):
                wall.from_node.open_walls(wall.position)
                other_node.open_walls(wall.position.opposite())
                sets.union(wall.from_node, other_node)

        return (start_node, end_node)

class DisjointSet:
    parent = {}

    def make_set(self, universe):
        for i in universe:
            self.parent[i] = i

    def find(self, k):
        return k if self.parent[k] == k else self.find(self.parent[k])

    def union(self, a, b):
        x = self.find(a)
        y = self.find(b)
        self.parent[x] = y

if __name__ == '__main__':
    maze = Maze(rows = 20, width = 20)
    maze.generate(None)