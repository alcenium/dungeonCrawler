import pygame
from pygame import Surface

class Atlas:
    def __init__(self, atlas_file: str, atlas_index_file: str, tile_size: int):
        self.tile_size = tile_size
        self.atlas_index_file = atlas_index_file

        self.indexes = {}
        self.extract_indexes()

        self.image = pygame.image.load(atlas_file).convert()

    def get_area(self, item_name:str) -> tuple:
        """
        Returns a tuple containing (x, y, width, height) of the tile
        inside the tileset
        """
        tile_pos = self.indexes[item_name]
        return (tile_pos[1] * self.tile_size, tile_pos[0] * self.tile_size, self.tile_size, self.tile_size)

    def debug(self):
        """
        Print out all tiles's name inside the atlas
        """
        for key, value in self.indexes.items():
            print(f"{key}: {value}")

    def extract_indexes(self):
        """
        Open the index file
        Stores all the names and individual coordinate in a dictionary
        """
        with open(self.atlas_index_file) as file:
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

    def blit(self, surface: Surface, name: str, coordinate: tuple) -> None:
        surface.blit(self.image, coordinate, self.get_area(name))
