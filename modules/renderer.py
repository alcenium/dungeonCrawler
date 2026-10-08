import pygame

from modules.atlas    import Atlas
from modules.registry import Characters, Tiles

class Renderer:
    def __init__(self, virtual_width, virtual_height):
        self.virtual_width  = virtual_width
        self.virtual_height = virtual_height
        self.virtual_screen = pygame.Surface((virtual_width, virtual_height))

        self.tile_size = 32
        self.atlases = {
                "tiles":    Atlas("32rogues/tiles.png",    "32rogues/tiles.txt",    32),
                "rogues":   Atlas("32rogues/rogues.png",   "32rogues/rogues.txt",   32),
                }

        self.tile_types = {
           Tiles.EMPTY:       self.atlases["tiles"].get("blank floor (dark grey)"),
           Tiles.WALL:        self.atlases["tiles"].get("dirt wall (top)"),
           Tiles.FLOOR:       self.atlases["tiles"].get("blank red floor"),
           Tiles.CORRIDOR:    self.atlases["tiles"].get("grass 1"),
           Characters.BANDIT: self.atlases["rogues"].get("bandit"),
        }

    def render(self, camera, tile, grid_coordinate):
        """
        Biến tọa độ thế giới sang tọa độ trên màn hình
        Hiển thị mặt phẳng lên màn hình
        """
        if not camera.object_visible(grid_coordinate):
            return

        surface = self.tile_types[tile]
        screen_position = camera.grid_to_screen(grid_coordinate)
        self.virtual_screen.blit(surface, screen_position)

    def render_world(self, camera, world):
        """ Hiển thị mọi thứ trong một danh sách tọa độ """

        for grid_coordinate in world:
            tile = world.get_tile(grid_coordinate)
            self.render(camera, tile, grid_coordinate)

    def to_screen(self, screen):
        scale = (screen.get_width() // self.virtual_width,
                 screen.get_height() // self.virtual_height)

        pygame.transform.scale_by(self.virtual_screen, scale, screen)
