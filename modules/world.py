from math import floor

class World:
    def __init__(self, map_grid, map_width=0, map_height=0, tile_size=0, tile_types=()):
        self.map_grid = map_grid
        self.map_width  = map_width
        self.map_height = map_height

        self.tile_size = tile_size
        self.tile_types = tile_types

    def get_tile(self, tile_coord):
        try:
            return self.tile_types[self.get_type(tile_coord)]
        except IndexError:
            return TileType("", True)

    def get_type(self, tile_coord):
        return self.map_grid[self.get_pos(tile_coord)]
    
    def get_pos(self, tile_coord):
        if (  tile_coord.x < 0 or tile_coord.x >= self.map_width
           or tile_coord.y < 0 or tile_coord.y >= self.map_height):
            raise IndexError("Coordinate provided is outside of the world's range")

        return tile_coord.y * self.map_width + tile_coord.x

    def grid_to_world(self, tile_coord: object):
        return (tile_coord.x * self.tile_size, tile_coord.y * self.tile_size)

    def world_to_grid(self, world_coord: tuple):
        return (floor(world_coord[0] / self.tile_size),
                floor(world_coord[1] / self.tile_size))

    def __iter__(self):
        return WorldIterator(self.map_grid, self.map_width, self.map_height)

class TileType:
    def __init__(self, name, walkable=False):
        self.name         = name
        self.walkable     = walkable

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
