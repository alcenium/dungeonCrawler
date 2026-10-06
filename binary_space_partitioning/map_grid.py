import pygame

class MapGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [0] * (width*height)

    def set(self, x, y, value):
        self.grid[y * self.width + x] = value

    def get(self, x, y):
        if self.is_out_of_range(x,y):
            return None
        return self.grid[y * self.width + x]

    def is_out_of_range(self, x, y):
        return (x < -1 or
                y < -1 or
                x >= self.width or
                y >= self.height)

    def display(self, display, grid_size):
        for x in range(self.width):
            for y in range(self.height):
                if self.get(x, y) == 1:
                    pygame.draw.rect(display, 'black',
                                     (x*grid_size, y*grid_size, grid_size, grid_size))
                    pygame.draw.rect(display, 'white',
                                     (x*grid_size+1, y*grid_size+1, grid_size-2, grid_size-2))

                if self.get(x, y) == 2:
                    pygame.draw.rect(display, 'black',
                                     (x*grid_size, y*grid_size, grid_size, grid_size))
                    pygame.draw.rect(display, (112, 128, 144),
                                     (x*grid_size+1, y*grid_size+1, grid_size-2, grid_size-2))

