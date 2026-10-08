from enum import Enum, auto

class Tiles(Enum):
    EMPTY     = (auto(), True)
    WALL_TOP  = (auto(), False)
    WALL_SIDE = (auto(), False)
    FLOOR     = (auto(), True)
    CORRIDOR  = (auto(), True)

    def __init__(self, value, walkable):
        self.walkable = walkable

class Characters(Enum):
    BANDIT = auto()
