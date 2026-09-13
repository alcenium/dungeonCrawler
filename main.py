import pygame
from camera import Camera
from player import Player
from tileSet import TileSet
from tilemap import Tilemap
from tile import Tile
from tile import TileCoord
from map import Map

class DungeonCrawler:
    def __init__(self):
        pygame.init()
        self.width,         self.height         = 1280, 720
        self.virtual_width, self.virtual_height = 320,  180

        self.scale = (self.width  // self.virtual_width,
                      self.height // self.virtual_height)
        self.center = (self.virtual_width //2 - 16,
                       self.virtual_height//2 - 16)

        self.clock          = pygame.time.Clock()
        self.screen         = pygame.display.set_mode((self.width, self.height))
        self.virtual_screen = pygame.Surface((self.virtual_width, self.virtual_height))

        self.tile_size = 32
        self.tilemap = Tilemap(self.tile_size)
        self.tilesets = {
                "animals": TileSet("32rogues/animals.png", "32rogues/animals.txt", self.tile_size),
                "items": TileSet("32rogues/items.png", "32rogues/items.txt", self.tile_size),
                "tiles": TileSet("32rogues/tiles.png", "32rogues/tiles.txt", self.tile_size),
                "rogues": TileSet("32rogues/rogues.png", "32rogues/rogues.txt", self.tile_size),
                "monsters": TileSet("32rogues/monsters.png", "32rogues/monsters.txt", self.tile_size)
                }
        self.map = Map((0, 1, 1, 1, 1, 1, 1, 1, 0,
                        0, 2, 2, 2, 2, 2, 2, 2, 0,
                        0, 2, 2, 2, 2, 2, 2, 2, 0,
                        0, 2, 2, 2, 2, 2, 2, 2, 0,
                        0, 2, 2, 2, 2, 2, 2, 2, 0,
                        1, 1, 1, 1, 3, 1, 1, 1, 1),
                        width = 9,
                        height= 6,
                        types = (Tile("tiles", "dirt wall (top)", False),
                                 Tile("tiles", "dirt wall (side)", False),
                                 Tile("tiles", "blank floor (dark grey)", True),
                                 Tile("tiles", "door 1", True))
                       )

        self.player = Player(TileCoord(4, 4), "bandit")
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
                            self.player.move(0, -1)
                        case pygame.K_s:
                            self.player.move(0, 1)
                        case pygame.K_a:
                            self.player.move(-1, 0)
                        case pygame.K_d:
                            self.player.move(1, 0)

    def processKey(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.running = False

    def update(self):
        self.camera.focus_on(
                self.tilemap.to_world_coord(self.player.coordinate))

    def draw(self):
        self.virtual_screen.fill((25,25,25))

        self.render_map()
        self.render(self.tilesets["rogues"],
                    self.player.character_type,
                    self.tilemap.to_world_coord(self.player.coordinate))

        pygame.transform.scale_by(self.virtual_screen, self.scale, self.screen)
        pygame.display.flip()

    def render(self, tileset, tile_name, world_coord):
        dest = self.camera.world_to_screen(world_coord)
        area = tileset.get_area(tile_name)

        self.virtual_screen.blit(tileset.image, dest, area)

    def render_map(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                tile_type = self.map.get_tile(x, y)

                tileset = self.tilesets[tile_type.tileset_name]
                tile_name = tile_type.name

                self.render(tileset, tile_name, self.tilemap.to_world_coord(TileCoord(x, y)))

DungeonCrawler().run()
