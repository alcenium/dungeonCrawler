import json
import pygame

from modules.atlas import Atlas
from modules.renderer import Renderer

from modules.world import World
from modules.world import GridCoordinate

from modules.binary_space_partitioning import MapGenerator

from modules.registry import Characters, Tiles

class DungeonCrawler:
    def __init__(self):
        pygame.init()
        self.width,         self.height         = 1280, 720
        self.virtual_width, self.virtual_height = 640,  360
        self.screen         = pygame.display.set_mode((self.width, self.height))
        self.clock          = pygame.time.Clock()

        self.map_seed = None
        self.map_generator = MapGenerator(seed=self.map_seed)

        self.character_type = Characters.BANDIT
        self.world = World(self.map_generator.generate_map(),
                           character_type = self.character_type)

        self.renderer = Renderer(self.virtual_width, self.virtual_height, 32)

        self.dt = 0
        self.fps = 60
        self.running = True

    def run(self):
        self.load_data()

        while self.running:
            self.dt = self.clock.tick(60) / 1000
            self.process_event()
            self.process_key()
            self.update()
            self.draw()

        self.save_data()
        pygame.quit()

    def process_event(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    moved = self.world.player.move(self.world, event.key)
                    if moved:
                        self.world.update()

    def process_key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            self.running = False

    def update(self):
        self.renderer.camera.focus_on(self.world.player.coordinate)

    def save_data(self):
        with open('save_file.json', 'rt') as save_file:
            pass

    def load_data(self):
        with open('save_file.json', 'wt') as save_file:
            pass

    def draw(self):
        self.renderer.virtual_screen.fill((25,25,25))
        self.renderer.render_world(self.world)
        self.renderer.render_entity(self.world.player)
        self.renderer.render_entities(self.world.enemies)

        self.renderer.to_screen(self.screen)
        pygame.display.flip()


DungeonCrawler().run()
