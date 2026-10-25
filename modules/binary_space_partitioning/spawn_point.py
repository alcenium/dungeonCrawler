from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.binary_space_partitioning.map_grid import MapGrid

class SpawnPoint:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, point) -> bool:
        if type(point) == tuple:
            return (self.x == point[0] and self.y == point[1])
        else:
            raise ValueError(f'Cannot compare spawn point to {type(point)}')

    def __ne__(self, point):
        if type(point) == tuple:
            return (self.x != point[0] or self.y != point[1])
        else:
            raise ValueError(f'Cannot compare spawn point to {type(point)}')
