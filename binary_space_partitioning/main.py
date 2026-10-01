import pygame
import random
from map import Map

screen_width = 1080
screen_height = 720

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

seed = 'Hi'
randomizer = random.Random(seed)

map = Map(screen_width, screen_height, randomizer, 16)
map.divide()
map.get_neighbors()
map.shrink()
map.add_corridors()
map.reduce_corridor()
map.align()
running = True

def draw_grid(grid_size):
    for x in range(grid_size, screen_width, grid_size):
        pygame.draw.rect(screen, (25, 25, 25), (x, 0, 1, screen_height))

    for y in range(grid_size, screen_height, grid_size):
        pygame.draw.rect(screen, (25, 25, 25), (0, y, screen_width, 1))

while running:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False

            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        running = False
                    case pygame.K_r:
                        map = Map(screen_width, screen_height, randomizer, 16)
                        map.divide()
                        map.get_neighbors()
                        map.shrink()
                        map.add_corridors()
                        map.reduce_corridor()
                        map.align()

    screen.fill((25, 25, 25))
    map.display(screen)
    draw_grid(16)
    pygame.display.flip()

    clock.tick(60)
