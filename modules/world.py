from math import floor

from modules.entities.player      import Player
from modules.entities.small_slime import SmallSlime
from modules.grid_coordinate      import GridCoordinate
from modules.registry import Characters, Tiles, Enemies

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.binary_space_partitioning.map_grid import MapGrid

class World:
    def __init__(self, map_grid: MapGrid, character_type: Characters = Characters.BANDIT) -> None:
        self.enemies: list[Entity] = []
        self.map_grid = map_grid
        self.player = Player(GridCoordinate(map_grid.spawn_point.x,
                                            map_grid.spawn_point.y),
                             character_type)
        self.add_enemies()

    def add_enemies(self):
        for enemy in self.map_grid.enemies:
            if enemy.type == Enemies.SMALL_SLIME:
                tile_coordinate = GridCoordinate(enemy.x, enemy.y)
                self.enemies.append(SmallSlime(tile_coordinate, Enemies.SMALL_SLIME))

    def get_tile(self, tile_coordinate: GridCoordinate) -> Tiles:
        return self.map_grid.get(tile_coordinate.x, tile_coordinate.y)

    def is_walkable(self, tile_coordinate):
        return self.get_tile(tile_coordinate).walkable

    def update(self) -> None:
        for enemy in self.enemies:
            enemy.update(self)

    def __iter__(self):
        return WorldIterator(self.map_grid)

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
