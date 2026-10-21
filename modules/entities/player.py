import pygame
from typing import TYPE_CHECKING
from modules.grid_coordinate import GridCoordinate

if TYPE_CHECKING:
    from modules.registry import Characters

class Player:
    def __init__(self, tile_coord: GridCoordinate, _type: Characters) -> None:
        self.coordinate = tile_coord
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

        neighbor_tile  : GridCoordinate = self.coordinate + relative_coordinate

        if world.is_walkable(neighbor_tile):
            self.coordinate += relative_coordinate
            return True
        return False

    def reduce_hp(self, ammount):
        self.hp -= ammount
        print(f'{self.hp}')
