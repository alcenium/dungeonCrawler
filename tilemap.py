class Tilemap:
    def __init__(self, tile_size):
        self.tile_size = tile_size

    def to_world_coord(self, tile_coord):
        return (tile_coord.x * self.tile_size, tile_coord.y * self.tile_size)

    def to_game_coord(self, world_coord):
        return (x / self.tile_size, y / self.tile_size)
