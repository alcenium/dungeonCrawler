import pygame
from modules.atlas import Atlas
from modules.camera import Camera
from modules.player import Player

from modules.world import World
from modules.world import TileType
from modules.world import GridCoordinate

from modules.binary_space_partitioning import generate_map

from modules.registry import Characters, Tiles

class DungeonCrawler:
    def __init__(self):
        pygame.init()
        self.width,         self.height         = 1280, 720
        self.virtual_width, self.virtual_height = 640,  360

        self.scale = (self.width  // self.virtual_width,
                      self.height // self.virtual_height)
        self.center = (self.virtual_width //2 - 16,
                       self.virtual_height//2 - 16)

        self.clock          = pygame.time.Clock()
        self.screen         = pygame.display.set_mode((self.width, self.height))
        self.virtual_screen = pygame.Surface((self.virtual_width, self.virtual_height))

        self.atlases = {
                "tiles":    Atlas("32rogues/tiles.png",    "32rogues/tiles.txt",    32),
                "rogues":   Atlas("32rogues/rogues.png",   "32rogues/rogues.txt",   32),
                }

        self.character_type = Characters.BANDIT
        self.world = World(generate_map(),
                           tile_size = 32,
                           tile_types = {
                               Tiles.EMPTY:       TileType(self.atlases["tiles"].get("blank floor (dark grey)"), True),
                               Tiles.WALL:        TileType(self.atlases["tiles"].get("dirt wall (top)"), False),
                               Tiles.FLOOR:       TileType(self.atlases["tiles"].get("blank red floor"), True),
                               Tiles.CORRIDOR:    TileType(self.atlases["tiles"].get("grass 1"),         True),
                               Characters.BANDIT: TileType(self.atlases["rogues"].get("bandit"), False),
                                        },
                           character_type = self.character_type
                          )

        self.camera = Camera(self.virtual_width, self.virtual_height)

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
        self.camera.focus_on(
                self.world.grid_to_world(self.world.player.coordinate))

    def draw(self):
        self.virtual_screen.fill((25,25,25))

        self.render_world()
        self.render(self.world.tile_types[self.character_type].surface,
                    self.world.grid_to_world(self.world.player.coordinate))

        pygame.transform.scale_by(self.virtual_screen, self.scale, self.screen)
        pygame.display.flip()

    def render(self, surface, world_position):
        """
        Biến tọa độ thế giới sang tọa độ trên màn hình
        Hiển thị mặt phẳng lên màn hình
        """
        screen_position = self.camera.world_to_screen(world_position)
        self.virtual_screen.blit(surface, screen_position)

    def render_world(self):
        """
        Hiển thị mọi tile trên thế giới
        """
        for grid_coord in self.world:
            tile = self.world.get_tile(grid_coord)
            self.render(tile.surface, self.world.grid_to_world(grid_coord))

DungeonCrawler().run()
