import pygame

class Corridor:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def align(self, grid_size):
        self.x1 -= self.x1 % grid_size
        self.y1 -= self.y1 % grid_size
        self.x2 -= self.x2 % grid_size
        self.y2 -= self.y2 % grid_size

    def display(self, surface):
        pygame.draw.rect(surface, (112, 128, 144), (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))

    def to_grid(self, map_grid, grid_size):
        x_start = int(self.x1 // grid_size)
        x_end   = int(self.x2 // grid_size)
        y_start = int(self.y1 // grid_size)
        y_end   = int(self.y2 // grid_size)

        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                map_grid.set(x, y, 2)
