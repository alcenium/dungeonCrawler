from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.binary_space_partitioning.map_grid import MapGrid

class SpawnPoint:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def align(self, grid_size: int) -> None:
        self.x -= self.x % grid_size
        self.y -= self.y % grid_size

    def to_grid(self, grid_size: int):
        x = self.x // grid_size
        y = self.y // grid_size
        return SpawnPoint(x, y)
