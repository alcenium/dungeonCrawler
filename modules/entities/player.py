import pygame
from typing import TYPE_CHECKING
from modules.grid_coordinate import GridCoordinate

if TYPE_CHECKING:
    from modules.registry import Characters

class Player:
    def __init__(self, tile_coord: GridCoordinate, _type: Characters) -> None:
        self.coordinate = tile_coord
        self._type      = _type

    def move(self, world, key) -> bool:
        """ Di chuyển tọa độ của người chơi """
        match key:
            case pygame.K_q:
                x, y = -1, -1
            case pygame.K_w:
                x, y =  0, -1
            case pygame.K_e:
                x, y =  1, -1
            case pygame.K_a:
                x, y = -1,  0
            case pygame.K_s:
                return True
            case pygame.K_d:
                x, y =  1,  0
            case pygame.K_z:
                x, y = -1,  1
            case pygame.K_x:
                x, y =  0,  1
            case pygame.K_c:
                x, y =  1,  1
            case _:
                return False

        grid_coordinate: GridCoordinate = GridCoordinate(x, y)
        neighbor_tile  : GridCoordinate = self.get_coord() + grid_coordinate

        if world.is_walkable(neighbor_tile):
            self.coordinate += grid_coordinate
            return True
        return False

    def get_coord(self) -> GridCoordinate:
        """ Trả về tọa độ của người chơi """
        return self.coordinate
