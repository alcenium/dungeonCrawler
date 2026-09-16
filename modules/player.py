class Player:
    def __init__(self, tile_coord, character_type:str):
        self.coordinate = tile_coord
        self.character_type = character_type

    def move(self, x, y):
        self.coordinate.x += x
        self.coordinate.y += y

    def get_coord(self):
        return self.coordinate
