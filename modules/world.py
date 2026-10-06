from math import floor

from modules.player import Player
from modules.registry import Characters, Tiles

class World:
    def __init__(self, map_grid, tile_size=0, tile_types=(), character_type=Characters.BANDIT):
        self.map_grid = map_grid

        self.tile_size = tile_size
        self.tile_types = tile_types

        self.player = Player(GridCoordinate(2, 2), character_type)

    def get_tile(self, grid_coord):
        try:
            return self.tile_types.get(self.get_type(grid_coord))
        except IndexError:
            return TileType("", True)

    def get_type(self, grid_coord):
        return self.map_grid.get(grid_coord.x, grid_coord.y)

    def grid_to_world(self, grid_coord: object):
        return (grid_coord.x * self.tile_size, grid_coord.y * self.tile_size)

    def world_to_grid(self, world_coord: tuple):
        return (floor(world_coord[0] / self.tile_size),
                floor(world_coord[1] / self.tile_size))

    def move_player(self, x, y):
        grid_coord = GridCoordinate(x, y)
        neighbor_tile = self.player.get_coord() + grid_coord
        if (self.get_tile(neighbor_tile).walkable):
            self.player.move(grid_coord)

    def __iter__(self):
        return WorldIterator(self.map_grid, self.map_grid.width, self.map_grid.height)

class TileType:
    def __init__(self, surface, walkable=False):
        self.surface  = surface
        self.walkable = walkable

class GridCoordinate:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return GridCoordinate(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"{self.x}, {self.y}"

class WorldIterator:
    def __init__(self, map_grid, map_width, map_height):
        self.map_grid = map_grid
        self.map_width  = map_width
        self.map_height = map_height

        self.index_column = -1
        self.index_row = 0

    def __next__(self):
        self.index_column += 1
        if self.index_column >= self.map_width:
            self.index_column = 0
            self.index_row += 1

        if self.index_row >= self.map_height:
            raise StopIteration

        return GridCoordinate(self.index_column, self.index_row)
