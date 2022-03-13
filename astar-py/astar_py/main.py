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
        window = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("A* Path Finding Algorithm Visualisation")

    def run(self):
        self.window = pygame.display.set_mode((self.width, self.width))
        self.main(self.window, self.width)

    def main(self, window, width) -> None:
        ROWS = constants.ROWS
        grid = make_grid(ROWS, width)

        start = None
        end = None

        run = True
        while run:
            draw(window, grid, ROWS, width)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                start, end = self.handle_left_click(start, end, spot)

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                start, end = self.handle_right_click(start, end, spot)

            if event.type == pygame.KEYDOWN:
                logger.debug(f"keydown: {event.key}")
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

        pygame.quit()

    def handle_right_click(self, start, end, spot):
        spot.reset()
        if spot == start:
            start = None
        elif spot == end:
            end = None
        return start,end

    def handle_left_click(self, start, end, spot):
        if not start and spot != end:
            start = spot
            start.make_start()

        elif not end and spot != start:
            end = spot
            end.make_end()

        elif spot != end and spot != start:
            spot.make_barrier()
        return start,end

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

if __name__ == '__main__':
    Display(WIDTH).run()