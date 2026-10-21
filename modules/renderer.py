import pygame

from modules.camera   import Camera
from modules.atlas    import Atlas
from modules.registry import Characters, Tiles, Enemies

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from enum   import Enum
    from pygame import Surface
    from modules.world           import World
    from modules.grid_coordinate import GridCoordinate

class Renderer:
    def __init__(self, virtual_width: int, virtual_height: int, grid_size: int) -> None:
        self.virtual_width  = virtual_width
        self.virtual_height = virtual_height
        self.virtual_screen: Surface = pygame.Surface((virtual_width, virtual_height))
        self.camera = Camera(virtual_width, virtual_height, grid_size)

        self.tile_size = 32
        self.atlases: dict[str, Atlas] = {
                "tiles":    Atlas("assets/32rogues/tiles.png",    "assets/32rogues/tiles.txt",    32),
                "rogues":   Atlas("assets/32rogues/rogues.png",   "assets/32rogues/rogues.txt",   32),
                "monsters": Atlas("assets/32rogues/monsters.png", "assets/32rogues/monsters.txt", 32),
                }

        self.tile_types: dict[Enum, Surface] = {
           Tiles.EMPTY:        self.atlases["tiles"].get("blank floor (dark purple)"),
           Tiles.WALL_TOP:     self.atlases["tiles"].get("dirt wall (top)"),
           Tiles.WALL_SIDE:    self.atlases["tiles"].get("dirt wall (side)"),
           Tiles.FLOOR:        self.atlases["tiles"].get("blank floor (dark grey)"),
           Tiles.CORRIDOR:     self.atlases["tiles"].get("stone floor 2"),
           Characters.BANDIT:  self.atlases["rogues"].get("bandit"),
           Enemies.SMALL_SLIME:self.atlases["monsters"].get("small slime"),
        }

    def render(self, tile: Enum, tile_coordinate: GridCoordinate) -> None:
        """
        Biến tọa độ thế giới sang tọa độ trên màn hình
        Hiển thị mặt phẳng lên màn hình
        """
        if not self.camera.object_visible(tile_coordinate):
            return

        surface = self.tile_types[tile]
        screen_position = self.camera.grid_to_screen(tile_coordinate)
        self.virtual_screen.blit(surface, screen_position)

    def render_world(self, world: World):
        """ Hiển thị mọi thứ trong một danh sách tọa độ """
        for tile_data in world:
            tile: Enum = tile_data[0]
            tile_coordinate = tile_data[1]
            self.render(tile, tile_coordinate)

    def render_enemies(self, enemies):
        for enemy in enemies:
            self.render(enemy._type, enemy.coordinate)
            if not enemy.moving:
                self.draw_move_intent(enemy.coordinate + enemy.direction)

    def render_player(self, player):
        self.render(player._type, player.coordinate)

    def to_screen(self, screen: Surface):
        """ Scale và đặt virtual_screen lên màn hình """
        scale = (screen.get_width() // self.virtual_width,
                 screen.get_height() // self.virtual_height)

        pygame.transform.scale_by(self.virtual_screen, scale, screen)

    def draw_move_intent(self, tile_coordinate):
        hight_light = (72, 0, 0)
        screen_position = self.camera.grid_to_screen(tile_coordinate)
        pygame.draw.rect(self.virtual_screen, hight_light, (screen_position[0], screen_position[1], 1, self.tile_size))
        pygame.draw.rect(self.virtual_screen, hight_light, (screen_position[0], screen_position[1], self.tile_size, 1))
        pygame.draw.rect(self.virtual_screen, hight_light, (screen_position[0] + self.tile_size - 1, screen_position[1], 1, self.tile_size))
        pygame.draw.rect(self.virtual_screen, hight_light, (screen_position[0], screen_position[1] + self.tile_size - 1, self.tile_size, 1))
