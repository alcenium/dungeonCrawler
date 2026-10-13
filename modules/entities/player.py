from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.registry import Characters
    from modules.world import GridCoordinate

class Player:
    def __init__(self, tile_coord: GridCoordinate, _type: Characters) -> None:
        self.coordinate = tile_coord
        self._type      = _type

    def move(self, grid_coord: GridCoordinate) -> None:
        """ Di chuyển tọa độ của người chơi """
        self.coordinate.x += grid_coord.x
        self.coordinate.y += grid_coord.y

    def get_coord(self) -> GridCoordinate:
        """ Trả về tọa độ của người chơi """
        return self.coordinate
