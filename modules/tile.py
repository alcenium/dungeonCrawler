class Tile:
    def __init__(self, tileset_name, name, walkable=False):
        self.tileset_name = tileset_name
        self.name         = name
        self.walkable     = walkable

class TileCoord:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
