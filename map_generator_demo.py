import pygame
import random
from modules.binary_space_partitioning.map import Map

screen_width = 1080
screen_height = 720

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

seed = 'b'
randomizer = random.Random(seed)

step = 0
grid_size = 16
running = True

def execute_step(map, step):
    match step:
        case 0:
            map = Map(screen_width, screen_height, randomizer, grid_size=grid_size, room_count=10)
        case 1:
            map.divide()
        case 2:
            map.get_neighbors()
        case 3:
            map.shrink()
        case 4:
            map.add_corridors()
        case 5:
            map.add_spawn_point()
        case 6:
            map.align()
        case 7:
            return map.to_grid()
    return map

def draw_grid(grid_size):
    for x in range(grid_size, screen_width, grid_size):
        pygame.draw.rect(screen, (25, 25, 25), (x, 0, 1, screen_height))

    for y in range(grid_size, screen_height, grid_size):
        pygame.draw.rect(screen, (25, 25, 25), (0, y, screen_width, 1))

map = None
map = execute_step(map, step)
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
                        step += 1
                        step %= 8
                        map = execute_step(map, step)

    screen.fill((25, 25, 25))
    map.display(screen)
    draw_grid(grid_size)

    pygame.display.flip()

    clock.tick(60)
