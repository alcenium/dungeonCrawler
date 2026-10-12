from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enum import Enum
    from modules.world import GridCoordinate

class Player:
    def __init__(self, tile_coord: GridCoordinate, character_type: Enum) -> None:
        self.coordinate        = tile_coord
        self.character_type    = character_type

    def move(self, grid_coord: GridCoordinate) -> None:
        """ Di chuyển tọa độ của người chơi """
        self.coordinate.x += grid_coord.x
        self.coordinate.y += grid_coord.y

    def get_coord(self) -> GridCoordinate:
        """ Trả về tọa độ của người chơi """
        return self.coordinate
