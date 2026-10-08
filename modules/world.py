from math import floor

from modules.player import Player
from modules.registry import Characters, Tiles

class World:
    def __init__(self, map_grid, character_type=Characters.BANDIT):
        self.map_grid = map_grid

        self.player = Player(GridCoordinate(2, 2), character_type)

    def get_tile(self, grid_coordinate):
        return self.map_grid.get(grid_coordinate.x, grid_coordinate.y)

    def move_player(self, x, y):
        grid_coordinate= GridCoordinate(x, y)
        neighbor_tile = self.player.get_coord() + grid_coordinate
        if (self.get_tile(neighbor_tile).walkable):
            self.player.move(grid_coordinate)

    def __iter__(self):
        return WorldIterator(self.map_grid)

class GridCoordinate:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return GridCoordinate(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"{self.x}, {self.y}"

class WorldIterator:
    def __init__(self, map_grid):
        self.map_grid = map_grid
        self.index_column = -1
        self.index_row = 0

    def __next__(self):
        self.index_column += 1
        if self.index_column >= self.map_grid.width:
            self.index_column = 0
            self.index_row += 1

        if self.index_row >= self.map_grid.height:
            raise StopIteration

        return GridCoordinate(self.index_column, self.index_row)
