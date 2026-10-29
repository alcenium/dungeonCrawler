import pygame
from modules.registry import Tiles

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygame import Surface
    from modules.binary_space_partitioning.map_grid import MapGrid

class Corridor:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def align(self, grid_size: int) -> None:
        self.x1 -= self.x1 % grid_size
        self.y1 -= self.y1 % grid_size
        self.x2 -= self.x2 % grid_size
        self.y2 -= self.y2 % grid_size

    def display(self, surface: Surface) -> None:
        pygame.draw.rect(surface, (112, 128, 144), (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))

    def to_grid(self, map_grid: MapGrid, grid_size: int):
        x_start = int(self.x1 // grid_size)
        x_end   = int(self.x2 // grid_size)
        y_start = int(self.y1 // grid_size)
        y_end   = int(self.y2 // grid_size)

        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                map_grid.set((x, y), Tiles.CORRIDOR)
