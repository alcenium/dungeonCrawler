from math import floor

from modules.entities.player      import Player
from modules.grid_coordinate      import GridCoordinate
from modules.registry import Characters, Tiles, Enemies

from modules.entities.small_slime import SmallSlime
from modules.entities.skeleton import Skeleton

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
            tile_coordinate = GridCoordinate(enemy.x, enemy.y)
            match enemy.type:
                case Enemies.SMALL_SLIME:
                    enemy = SmallSlime(tile_coordinate, Enemies.SMALL_SLIME)
                case Enemies.SKELETON:
                    enemy = Skeleton(tile_coordinate, Enemies.SKELETON)
            self.enemies.append(enemy)

    def get_tile(self, tile_coordinate: GridCoordinate) -> Tiles:
        if tile_coordinate == self.player.coordinate:
            return self.player
        return self.map_grid.get(tile_coordinate.x, tile_coordinate.y)

    def get_entity(self, tile_coordinate: GridCoordinate) -> Entity | None:
        for enemy in self.enemies:
            if enemy.coordinate == tile_coordinate:
                return enemy
        return None

    def is_walkable(self, tile_coordinate: GridCoordinate | tuple[int, int]) -> bool:
        for enemy in self.enemies:
            if enemy.coordinate == tile_coordinate:
                return False

        if tile_coordinate == self.player.coordinate:
            return False

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

        return (self.map_grid.grid[self.index_row * self.map_grid.width + self.index_column],
                GridCoordinate(self.index_column, self.index_row))
