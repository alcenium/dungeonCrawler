import pygame
from modules.registry import Tiles

class MapGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [Tiles.EMPTY] * (width*height)

    def set(self, x, y, value):
        self.grid[y * self.width + x] = value

    def get(self, x, y):
        if self.is_out_of_range(x,y):
            return None
        return self.grid[y * self.width + x]

    def is_out_of_range(self, x, y):
        return (x < 0 or
                y < 0 or
                x >= self.width or
                y >= self.height)

    def display(self, display, grid_size):
        for x in range(self.width):
            for y in range(self.height):
                if self.get(x, y) == Tiles.FLOOR:
                    pygame.draw.rect(display, 'white',
                                     (x*grid_size, y*grid_size, grid_size, grid_size))

                if self.get(x, y) == Tiles.CORRIDOR:
                    pygame.draw.rect(display, (112, 128, 144),
                                     (x*grid_size, y*grid_size, grid_size, grid_size))
