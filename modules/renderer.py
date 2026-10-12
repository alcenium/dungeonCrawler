import pygame

from modules.atlas    import Atlas
from modules.registry import Characters, Tiles

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from enum import Enum
    from pygame import Surface
    from modules.world    import World
    from modules.camera   import Camera
    from modules.world    import GridCoordinate

class Renderer:
    def __init__(self, virtual_width: int, virtual_height: int) -> None:
        self.virtual_width  = virtual_width
        self.virtual_height = virtual_height
        self.virtual_screen: Surface = pygame.Surface((virtual_width, virtual_height))

        self.tile_size = 32
        self.atlases: dict[str, Atlas] = {
                "tiles":    Atlas("assets/32rogues/tiles.png",    "assets/32rogues/tiles.txt",    32),
                "rogues":   Atlas("assets/32rogues/rogues.png",   "assets/32rogues/rogues.txt",   32),
                }

        self.tile_types: dict[Enum, Surface] = {
           Tiles.EMPTY:       self.atlases["tiles"].get("blank floor (dark purple)"),
           Tiles.WALL_TOP:    self.atlases["tiles"].get("dirt wall (top)"),
           Tiles.WALL_SIDE:   self.atlases["tiles"].get("dirt wall (side)"),
           Tiles.FLOOR:       self.atlases["tiles"].get("blank floor (dark grey)"),
           Tiles.CORRIDOR:    self.atlases["tiles"].get("stone floor 2"),
           Characters.BANDIT: self.atlases["rogues"].get("bandit"),
        }

    def render(self, camera: Camera, tile: Enum, grid_coordinate: GridCoordinate) -> None:
        """
        Biến tọa độ thế giới sang tọa độ trên màn hình
        Hiển thị mặt phẳng lên màn hình
        """
        if not camera.object_visible(grid_coordinate):
            return

        surface = self.tile_types[tile]
        screen_position = camera.grid_to_screen(grid_coordinate)
        self.virtual_screen.blit(surface, screen_position)

    def render_world(self, camera: Camera, world: World):
        """ Hiển thị mọi thứ trong một danh sách tọa độ """
        for grid_coordinate in world:
            tile: Enum = world.get_tile(grid_coordinate)
            self.render(camera, tile, grid_coordinate)

    def to_screen(self, screen: Surface):
        """ Scale và đặt virtual_screen lên màn hình """
        scale = (screen.get_width() // self.virtual_width,
                 screen.get_height() // self.virtual_height)

        pygame.transform.scale_by(self.virtual_screen, scale, screen)
