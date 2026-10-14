import random
from typing import TYPE_CHECKING

from modules.grid_coordinate import GridCoordinate

if TYPE_CHECKING:
    from modules.registry import Enemies

class SmallSlime:
    def __init__(self, coordinate: GridCoordinate, _type: Enemies):
        self.coordinate = coordinate
        self._type      = _type

        random.seed()
        match random.randint(1, 4):
            case 1:
                self.direction = GridCoordinate( 1, 0)
            case 2:
                self.direction = GridCoordinate(-1, 0)
            case 3:
                self.direction = GridCoordinate( 0, 1)
            case 4:
                self.direction = GridCoordinate( 0,-1)

    def update(self, world):
        if world.is_walkable(self.coordinate + self.direction):
            self.coordinate += self.direction
        else:
            self.direction *= GridCoordinate(-1, -1)
