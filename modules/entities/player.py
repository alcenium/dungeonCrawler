import pygame
from typing import TYPE_CHECKING

from modules.coordinate import Coordinate
from modules.entities.enemy  import Enemy

if TYPE_CHECKING:
    from modules.registry import Characters

class Player:
    def __init__(self, coordinate: Coordinate, _type: Characters) -> None:
        self.coordinate = coordinate
        self._type      = _type
        self.hp         = 4

    def move(self, world, key) -> bool:
        """ Di chuyển người chơi """
        match key:
            case pygame.K_q:
                relative_coordinate = (-1, -1)
            case pygame.K_w:
                relative_coordinate = ( 0, -1)
            case pygame.K_e:
                relative_coordinate = ( 1, -1)
            case pygame.K_a:
                relative_coordinate = (-1,  0)
            case pygame.K_s:
                return True
            case pygame.K_d:
                relative_coordinate = ( 1,  0)
            case pygame.K_z:
                relative_coordinate = (-1,  1)
            case pygame.K_x:
                relative_coordinate = ( 0,  1)
            case pygame.K_c:
                relative_coordinate = ( 1,  1)
            case _:
                return False

        neighbor_tile  : Coordinate = self.coordinate + relative_coordinate

        if world.is_walkable(neighbor_tile):
            self.coordinate += relative_coordinate
            return True
        else:
            entity = world.get_entity(neighbor_tile)
            match entity:
                case Enemy():
                    entity.reduce_hp()
                    if entity.hp <= 0:
                        world.enemies.remove(entity)
                    return True
        return False

    def reduce_hp(self, ammount: int = 1):
        self.hp -= ammount
        print(f'{self.hp}')
