from enum import Enum, IntEnum
import json

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

WIDTH = 900
ROWS = 30

class NodeState(Enum):
    OPEN = GREEN
    CLOSED = RED
    BARRIER = BLACK
    START = ORANGE
    END = TURQUOISE
    PATH = PURPLE
    DEFAULT = WHITE

class WallPlacement(str, Enum):
    NORTH, EAST, SOUTH, WEST = ["north", "east", "south", "west"]

    def opposite(self):
        if self == WallPlacement.NORTH:
            return WallPlacement.SOUTH
        if self == WallPlacement.SOUTH:
            return WallPlacement.NORTH
        if self == WallPlacement.EAST:
            return WallPlacement.WEST
        if self == WallPlacement.WEST:
            return WallPlacement.EAST
