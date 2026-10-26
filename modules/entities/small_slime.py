import random
from typing import TYPE_CHECKING

from modules.grid_coordinate import GridCoordinate
from modules.entities.player import Player
from modules.entities.enemy import Enemy
from modules.registry import Tiles

if TYPE_CHECKING:
    from modules.registry import Enemies

class SmallSlime(Enemy):
    def __init__(self, coordinate: GridCoordinate, _type: Enemies):
        super().__init__(coordinate, _type)
        self.hp     = 2
        self.moving = True
        self.neighbor = None

        random.seed()
        match random.randint(1, 4):
            case 1:
                self.direction = ( 1, 0)
            case 2:
                self.direction = (-1, 0)
            case 3:
                self.direction = ( 0, 1)
            case 4:
                self.direction = ( 0,-1)

    def update(self, world):
        neighbor_pos = self.coordinate + self.direction
        self.neighbor = world.get_tile(neighbor_pos)

        if type(self.neighbor) == Tiles and not self.neighbor.walkable:
            self.direction = (self.direction[0] * -1,
                              self.direction[1] * -1)

        self.moving = not self.moving
        if self.moving:
            self.move(world)

    def move(self, world):
        match self.neighbor:
            case Tiles():
                self.coordinate += self.direction
            case Player():
                self.neighbor.reduce_hp(1)
