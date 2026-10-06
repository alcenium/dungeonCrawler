import pygame
import random
from modules.binary_space_partitioning.map import Map

screen_width = 1080
screen_height = 720

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

seed = 'Hi'
randomizer = random.Random(seed)

grid_size = 16
running = True

def create_map():
    map = Map(screen_width, screen_height, randomizer, grid_size=grid_size, room_count=10)
    map.divide()
    map.get_neighbors()
    map.shrink()
    map.add_corridors()
    map.reduce_corridor()
    map.align()
    return map

def draw_grid(grid_size):
    for x in range(grid_size, screen_width, grid_size):
        pygame.draw.rect(screen, (25, 25, 25), (x, 0, 1, screen_height))

    for y in range(grid_size, screen_height, grid_size):
        pygame.draw.rect(screen, (25, 25, 25), (0, y, screen_width, 1))

map = create_map()
map_grid = map.to_grid()

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
                        map = create_map()
                        map_grid = map.to_grid()

    screen.fill((25, 25, 25))
    # map.display(screen)
    # draw_grid(grid_size)
    map_grid.display(screen, grid_size)
    pygame.display.flip()

    clock.tick(60)
