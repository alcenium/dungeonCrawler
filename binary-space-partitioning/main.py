import pygame
from map import Map

screen_width = 1080
screen_height = 720

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

map = Map(screen_width, screen_height)
map.divide()
map.shrink()
running = True

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
                        map = Map(screen_width, screen_height)
                        map.divide()
                        map.shrink()

    screen.fill((25, 25, 25))
    map.display(screen)
    pygame.display.flip()

    clock.tick(60)
