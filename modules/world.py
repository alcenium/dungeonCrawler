from math import floor

from modules.entities.player      import Player
from modules.coordinate      import Coordinate
from modules.registry import Characters, Tiles, Enemies

from modules.entities.small_slime import SmallSlime
from modules.entities.skeleton import Skeleton

from modules.pathfinding.a_star import AStar

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.binary_space_partitioning.map_grid import MapGrid

class World:
    def __init__(self, map_grid: MapGrid, character_type: Characters = Characters.BANDIT) -> None:
        self.map_grid = map_grid
        self.width = map_grid.width
        self.height = map_grid.height

        self.pathfinder = AStar(self.map_grid)

        self.player = Player(Coordinate(map_grid.spawn_point.x,
                                            map_grid.spawn_point.y),
                             character_type)

        self.enemies: list[Entity] = []
        self.add_enemies()

    def add_enemies(self):
        for enemy in self.map_grid.enemies:
            coordinate = Coordinate(enemy.x, enemy.y)
            match enemy.type:
                case Enemies.SMALL_SLIME:
                    enemy = SmallSlime(coordinate, Enemies.SMALL_SLIME)
                case Enemies.SKELETON:
                    enemy = Skeleton(coordinate, Enemies.SKELETON)
            self.enemies.append(enemy)

    def get_tile(self, coordinate: Coordinate) -> Tiles:
        return self.map_grid.get(coordinate)

    def get_entity(self, coordinate: Coordinate) -> Entity | None:
        if self.player.coordinate == coordinate:
            return self.player

        for enemy in self.enemies:
            if enemy.coordinate == coordinate:
                return enemy
        return None

    def is_walkable(self, coordinate: Coordinate | tuple[int, int]) -> bool:
        for enemy in self.enemies:
            if enemy.coordinate == coordinate:
                return False

        return self.get_tile(coordinate).walkable

    def update(self) -> None:
        self.pathfinder.update_map(self)
        for enemy in self.enemies:
            enemy.update(self)

    def __iter__(self):
        return WorldIterator(self.map_grid)


class WorldIterator:
    def __init__(self, map_grid: MapGrid) -> None:
        self.map_grid = map_grid
        self.index_column = -1
        self.index_row = 0

    def __next__(self) -> Coordinate:
        self.index_column += 1
        if self.index_column >= self.map_grid.width:
            self.index_column = 0
            self.index_row += 1

        if self.index_row >= self.map_grid.height:
            raise StopIteration

        return (self.map_grid.map_grid[self.index_row * self.map_grid.width + self.index_column],
                Coordinate(self.index_column, self.index_row))
