from enum import Enum, auto

class Tiles(Enum):
    EMPTY    = (auto(), False)
    WALL     = (auto(), False)
    FLOOR    = (auto(), True)
    CORRIDOR = (auto(), True)

    def __init__(self, value, walkable):
        self.walkable = walkable

class Characters(Enum):
    BANDIT = auto()
