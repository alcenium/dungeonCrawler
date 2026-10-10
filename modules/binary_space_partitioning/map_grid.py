import pygame
from modules.registry import Tiles

class MapGrid:
    def __init__(self, width, height, grid_size):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.grid = [Tiles.EMPTY] * (width*height)

        self.spawn_point = None

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

    def fill_wall(self):
        neighbors = ((-1, -1), (0, -1), (1, -1),
                     (-1,  0),          (1,  0),
                     (-1,  1), (0,  1), (1,  1))

        for x in range(0, self.width):
            for y in range(0, self.height):
                cell_self = self.get(x, y)
                for neighbor_relative_pos in neighbors:
                    neighbor = self.get(x + neighbor_relative_pos[0],
                                        y + neighbor_relative_pos[1])
                    if cell_self != Tiles.EMPTY:
                        continue
                    if neighbor != None and neighbor != Tiles.EMPTY and neighbor != Tiles.WALL_TOP:
                        self.set(x, y, Tiles.WALL_TOP)

    def add_wall_depth(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                cell_south = self.get(x, y + 1)
                cell_self  = self.get(x, y)

                if cell_self != Tiles.WALL_TOP:
                    continue
                if cell_south != Tiles.WALL_TOP:
                    self.set(x, y, Tiles.WALL_SIDE)

    def add_spawn_point(self, spawn_point):
        self.spawn_point = spawn_point

    def display(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                if self.get(x, y) == Tiles.FLOOR:
                    pygame.draw.rect(surface, 'white',
                                     (x*self.grid_size, y*self.grid_size, self.grid_size, self.grid_size))

                if self.get(x, y) == Tiles.CORRIDOR:
                    pygame.draw.rect(surface, (112, 128, 144),
                                     (x*self.grid_size, y*self.grid_size, self.grid_size, self.grid_size))

        if self.spawn_point:
            pygame.draw.rect(surface, 'green', (self.spawn_point.x * self.grid_size,
                                                self.spawn_point.y * self.grid_size,
                                                self.grid_size,
                                                self.grid_size))
