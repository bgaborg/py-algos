import pygame
from astar_py import constants
import logging

from astar_py.constants import *
from astar_py.node import Node

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    pass


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))


def draw(window, grid, rows, width):
    window.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(window)

    draw_grid(window, rows, width)
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
        window = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("A* Path Finding Algorithm Visualisation")

    def run(self):
        self.window = pygame.display.set_mode((self.width, self.width))
        self.main(self.window, self.width)

    def main(self, window, width) -> None:
        ROWS = constants.ROWS
        self.grid = make_grid(ROWS, width)

        run = True
        while run:
            draw(window, self.grid, ROWS, width)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                spot = self.calculate_spot(width, ROWS)
                self.handle_left_click(spot)

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                spot = self.calculate_spot(width, ROWS)
                self.handle_right_click(spot)

            if event.type == pygame.KEYDOWN:
                self.handle_keydown(window, width, ROWS, self.grid, event)

        pygame.quit()

    def calculate_spot(self, width, ROWS) -> Node:
        pos = pygame.mouse.get_pos()
        row, col = get_clicked_pos(pos, ROWS, width)
        return self.grid[row][col]

    def handle_keydown(self, window, width, ROWS, grid, event):
        logger.debug(f"keydown: {event.key}")
        if event.key == pygame.K_SPACE and self.start and self.end:
            for row in grid:
                for spot in row:
                    spot.update_neighbors(grid)

            algorithm(lambda: draw(window, grid, ROWS, width),self.grid, self.start, self.end)

        if event.key == pygame.K_BACKSPACE:
            self.start = None
            self.end = None
            self.grid = make_grid(ROWS, width)

    def handle_right_click(self, spot):
        spot.reset()
        if spot == self.start:
            self.start = None
        elif spot == self.end:
            self.end = None
        return self.start, self.end

    def handle_left_click(self, spot):
        if not self.start and spot != self.end:
            self.start = spot
            self.start.make_start()

        elif not self.end and spot != self.start:
            self.end = spot
            self.end.make_end()

        elif spot != self.end and spot != self.start:
            spot.make_barrier()
        return self.start, self.end

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

if __name__ == '__main__':
    Display(WIDTH).run()