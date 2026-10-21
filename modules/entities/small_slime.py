import random
from typing import TYPE_CHECKING

from modules.grid_coordinate import GridCoordinate
from modules.entities.player import Player
from modules.registry import Tiles

if TYPE_CHECKING:
    from modules.registry import Enemies

class SmallSlime:
    def __init__(self, coordinate: GridCoordinate, _type: Enemies):
        self.coordinate = coordinate
        self._type      = _type
        self.turn = 1

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
        self.turn += 1    
        self.turn %= 2
        if self.turn == 0:
            self.move(world)


    def move(self, world):
        neighbor_pos = self.coordinate + self.direction
        neighbor = world.get_tile(neighbor_pos)

        match neighbor:
            case Tiles():
                if neighbor.walkable:
                    self.coordinate += self.direction
                else:
                    self.direction = (self.direction[0] * -1,
                                      self.direction[1] * -1)
                    self.coordinate += self.direction
            case Player():
                neighbor.reduce_hp(1)
