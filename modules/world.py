class World:
    def __init__(self, map_grid, map_width=0, map_height=0, tile_size=0, tile_types=()):
        self.map_grid = map_grid
        self.map_width  = map_width
        self.map_height = map_height

        self.tile_size = tile_size
        self.tile_types = tile_types

    def get_tile(self, x, y):
        return self.tile_types[self.get_type(x, y)]

    def get_type(self, x, y):
        return self.map_grid[self.get_pos(x, y)]
    
    def get_pos(self, x, y):
        return y * self.map_width + x

    def grid_to_world(self, tile_coord):
        return (tile_coord.x * self.tile_size, tile_coord.y * self.tile_size)

    def world_to_grid(self, world_coord):
        return (x / self.tile_size, y / self.tile_size)

class TileType:
    def __init__(self, name, walkable=False):
        self.name         = name
        self.walkable     = walkable

class GridCoordinate:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
