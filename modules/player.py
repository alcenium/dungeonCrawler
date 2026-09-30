class Player:
    def __init__(self, tile_coord, character_type:str, character_surface):
        self.coordinate        = tile_coord
        self.character_type    = character_type
        self.character_surface = character_surface

    def move(self, grid_coord):
        self.coordinate.x += grid_coord.x
        self.coordinate.y += grid_coord.y

    def get_coord(self):
        return self.coordinate
