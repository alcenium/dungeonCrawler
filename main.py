import pygame
from modules.atlas import Atlas
from modules.camera import Camera
from modules.player import Player
from modules.world import World
from modules.world import TileType
from modules.world import GridCoordinate

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
                "animals":  Atlas("32rogues/animals.png",  "32rogues/animals.txt",  32),
                "items":    Atlas("32rogues/items.png",    "32rogues/items.txt",    32),
                "tiles":    Atlas("32rogues/tiles.png",    "32rogues/tiles.txt",    32),
                "rogues":   Atlas("32rogues/rogues.png",   "32rogues/rogues.txt",   32),
                "monsters": Atlas("32rogues/monsters.png", "32rogues/monsters.txt", 32)
                }
        self.world = World((0, 1, 1, 1, 1, 1, 1, 1, 0,
                            0, 2, 2, 2, 2, 2, 2, 2, 0,
                            0, 2, 2, 2, 2, 2, 2, 2, 0,
                            0, 2, 2, 2, 2, 2, 2, 2, 0,
                            0, 2, 2, 2, 2, 2, 2, 2, 0,
                            1, 1, 1, 1, 3, 1, 1, 1, 1),
                            map_width = 9,
                            map_height= 6,

                            tile_size = 32,
                            tile_types = (TileType("dirt wall (top)", False),
                                          TileType("dirt wall (side)", False),
                                          TileType("blank floor (dark grey)", True),
                                          TileType("door 1", True)
                                         )
                          )

        self.player = Player(GridCoordinate(4, 4), "bandit")
        self.camera = Camera(self.virtual_width, self.virtual_height)

        self.dt = 0
        self.fps = 60
        self.running = True

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000
            self.processEvent()
            self.processKey()
            self.update()
            self.draw()
        pygame.quit()

    def processEvent(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_w:
                            self.try_moving(0, -1)
                        case pygame.K_s:
                            self.try_moving(0, 1)
                        case pygame.K_a:
                            self.try_moving(-1, 0)
                        case pygame.K_d:
                            self.try_moving(1, 0)

    def processKey(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.running = False

    def update(self):
        self.camera.focus_on(
                self.world.grid_to_world(self.player.coordinate))

    def draw(self):
        self.virtual_screen.fill((25,25,25))

        self.render_world()
        self.render(self.atlases["rogues"],
                    self.player.character_type,
                    self.world.grid_to_world(self.player.coordinate))

        pygame.transform.scale_by(self.virtual_screen, self.scale, self.screen)
        pygame.display.flip()

    def render(self, atlas, tile_name, world_position):
        """
        Convert from world coordinate to camera relative coordinate
        Blit the tile to the virtual screen
        """
        dest = self.camera.world_to_screen(world_position)
        atlas.blit(self.virtual_screen, tile_name, dest)

    def render_world(self):
        """
        Blit every tiles in the map
        """
        for grid_coord in self.world:
            tile_type = self.world.get_tile(grid_coord)

            atlas = self.atlases["tiles"]
            tile_name = tile_type.name

            self.render(atlas, tile_name, self.world.grid_to_world(grid_coord))

    def try_moving(self, x, y):
        grid_coord = GridCoordinate(x, y)
        neighbor_tile = self.player.get_coord() + grid_coord
        if (self.world.get_tile(neighbor_tile).walkable):
            self.player.move(grid_coord)

DungeonCrawler().run()
