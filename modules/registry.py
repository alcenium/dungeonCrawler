from enum import Enum, auto
class Tiles(Enum):
    EMPTY = auto()
    WALL = auto()
    FLOOR = auto()
    CORRIDOR = auto()

class Characters(Enum):
    BANDIT = auto()
