import pygame
from modules.atlas import Atlas
from modules.camera import Camera
from modules.renderer import Renderer

from modules.world import World
from modules.world import GridCoordinate

from modules.binary_space_partitioning import generate_map

from modules.registry import Characters, Tiles

class DungeonCrawler:
    def __init__(self):
        pygame.init()
        self.width,         self.height         = 1280, 720
        self.virtual_width, self.virtual_height = 640,  360
        self.screen         = pygame.display.set_mode((self.width, self.height))
        self.clock          = pygame.time.Clock()

        self.character_type = Characters.BANDIT
        self.world = World(generate_map(), character_type = self.character_type)

        self.camera = Camera(self.virtual_width, self.virtual_height, 32)
        self.renderer = Renderer(self.virtual_width, self.virtual_height)

        self.dt = 0
        self.fps = 60
        self.running = True

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000
            self.process_event()
            self.process_key()
            self.update()
            self.draw()
        pygame.quit()

    def process_event(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_w:
                            self.world.move_player(0, -1)
                        case pygame.K_s:
                            self.world.move_player(0, 1)
                        case pygame.K_a:
                            self.world.move_player(-1, 0)
                        case pygame.K_d:
                            self.world.move_player(1, 0)

    def process_key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.running = False

    def update(self):
        self.camera.focus_on(self.world.player.coordinate)

    def draw(self):
        self.renderer.virtual_screen.fill((25,25,25))
        self.renderer.render_world(self.camera, self.world)
        self.renderer.render(self.camera,
                             self.world.player.character_type,
                             self.world.player.coordinate)

        self.renderer.to_screen(self.screen)
        pygame.display.flip()


DungeonCrawler().run()
