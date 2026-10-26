import random
from typing import TYPE_CHECKING

from modules.grid_coordinate import GridCoordinate
from modules.entities.player import Player
from modules.entities.enemy import Enemy
from modules.registry import Tiles

if TYPE_CHECKING:
    from modules.registry import Enemies

class Skeleton(Enemy):
    def __init__(self, coordinate: GridCoordinate, _type: Enemies):
        super().__init__(coordinate, _type)
        self.moving = True
        self.neighbor = None

    def update(self, world):
        pass
