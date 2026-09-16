import pygame
from pygame import Surface

class TileSet:
    def __init__(self, tileset_file: str, tile_index_file: str, tile_size: int):
        self.tile_size = tile_size
        self.tile_index_file = tile_index_file

        self.indexes = {}
        self.extract_indexes()

        self.image = pygame.image.load(tileset_file).convert()

    def get_area(self, item_name:str) -> tuple:
        """
        Returns a tuple containing (x, y, width, height) of the tile
        inside the tileset
        """
        tile_pos = self.indexes[item_name]
        return (tile_pos[1] * self.tile_size, tile_pos[0] * self.tile_size, self.tile_size, self.tile_size)

    def debug(self):
        for key, value in self.indexes.items():
            print(f"{key}: {value}")

    def extract_indexes(self):
        with open(self.tile_index_file) as file:
            column = 0
            row = 0

            lines = file.read().splitlines()
            for line in lines:
                if len(line) != 0:
                    name = line.split(sep='.')[2]
                    self.indexes[name.lstrip()] = (row, column)
                    column += 1
                else:
                    column = 0
                    row += 1
