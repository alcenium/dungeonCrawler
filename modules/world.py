from math import floor

from modules.player   import Player
from modules.registry import Characters, Tiles

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.binary_space_partitioning.map_grid import MapGrid

class World:
    def __init__(self, map_grid: MapGrid, character_type: Characters = Characters.BANDIT) -> None:
        self.enemies = []
        self.map_grid = map_grid
        self.player = Player(GridCoordinate(map_grid.spawn_point.x,
                                            map_grid.spawn_point.y),
                             character_type)

    def get_tile(self, grid_coordinate: GridCoordinate) -> Tiles:
        return self.map_grid.get(grid_coordinate.x, grid_coordinate.y)

    def move_player(self, x: int, y: int) -> None:
        grid_coordinate: GridCoordinate = GridCoordinate(x, y)
        neighbor_tile: GridCoordinate   = self.player.get_coord() + grid_coordinate

        if self.get_tile(neighbor_tile).walkable:
            self.player.move(grid_coordinate)

    def __iter__(self):
        return WorldIterator(self.map_grid)

class GridCoordinate:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def __add__(self, other) -> GridCoordinate:
        return GridCoordinate(self.x + other.x, self.y + other.y)

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"

class WorldIterator:
    def __init__(self, map_grid: MapGrid) -> None:
        self.map_grid = map_grid
        self.index_column = -1
        self.index_row = 0

    def __next__(self) -> GridCoordinate:
        self.index_column += 1
        if self.index_column >= self.map_grid.width:
            self.index_column = 0
            self.index_row += 1

        if self.index_row >= self.map_grid.height:
            raise StopIteration

        return GridCoordinate(self.index_column, self.index_row)
