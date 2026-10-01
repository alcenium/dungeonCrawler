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
