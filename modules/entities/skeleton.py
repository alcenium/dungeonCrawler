import random
from typing import TYPE_CHECKING

from modules.coordinate import Coordinate
from modules.entities.player import Player
from modules.entities.enemy import Enemy
from modules.registry import Tiles

if TYPE_CHECKING:
    from modules.registry import Enemies

class Skeleton(Enemy):
    def __init__(self, coordinate: Coordinate, _type: Enemies):
        super().__init__(coordinate, _type)
        self.moving = True
        self.neighbor = None

        self.IDLE = 0
        self.CHASING = 1
        self.state = self.IDLE

        self.path = None

    def update(self, world):
        if self.is_nearby(world.player.coordinate, 5):
            self.path = world.pathfinder.pathfind(self.coordinate, world.player.coordinate)

        if self.path:
            self.move(world, self.path.pop(0))
            return
    
    def move(self, world, position):
        coordinate = Coordinate.to_coordinate(position)
        entity = world.get_entity(coordinate)
        match entity:
            case None:
                self.coordinate = coordinate
            case Player():
                entity.reduce_hp(1)
