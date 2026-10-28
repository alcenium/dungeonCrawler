import pygame
from modules.registry import Tiles, Enemies
from modules.binary_space_partitioning.spawn_point import SpawnPoint
from modules.binary_space_partitioning.enemy import Enemy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from random import Random
    from typing import Any

class MapGrid:
    def __init__(self, width: int, height: int, grid_size: int, randomizer: Random):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.randomizer = randomizer

        self.grid: list[Tiles] = [Tiles.EMPTY] * (width*height)
        self.rooms: list[tuple] = []

        self.spawn_point: Any = None
        self.enemies: list[Enemy] = []

    def set(self, x, y, value) -> bool:
        if self.is_out_of_range(x,y):
            return False
        self.grid[y * self.width + x] = value
        return True

    def get(self, x, y):
        if self.is_out_of_range(x,y):
            return None
        return self.grid[y * self.width + x]

    def is_out_of_range(self, x, y):
        return (x < 0 or
                y < 0 or
                x >= self.width or
                y >= self.height)

    def fill_wall(self):
        neighbors = ((-1, -1), (0, -1), (1, -1),
                     (-1,  0),          (1,  0),
                     (-1,  1), (0,  1), (1,  1))

        for x in range(0, self.width):
            for y in range(0, self.height):
                cell_self = self.get(x, y)
                for neighbor_relative_pos in neighbors:
                    neighbor = self.get(x + neighbor_relative_pos[0],
                                        y + neighbor_relative_pos[1])
                    if cell_self != Tiles.EMPTY:
                        continue
                    if neighbor != None and neighbor != Tiles.EMPTY and neighbor != Tiles.WALL_TOP:
                        self.set(x, y, Tiles.WALL_TOP)

    def add_wall_depth(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                cell_south = self.get(x, y + 1)
                cell_self  = self.get(x, y)

                if cell_self != Tiles.WALL_TOP:
                    continue
                if cell_south != Tiles.WALL_TOP:
                    self.set(x, y, Tiles.WALL_SIDE)

    def add_spawn_point(self) -> None:
        """ Chọn một phòng ngẫu nhiên và dặt điểm sinh ra người chơi ở đó """
        room = self.randomizer.choice(self.rooms)
        point = self.get_random_walkable_coordinate(room[0], room[1], room[2], room[3])
        self.spawn_point = SpawnPoint(point[0], point[1])

    def add_enemies(self) -> None:
        for room in self.rooms:
            point = self.get_random_walkable_coordinate(room[0], room[1], room[2], room[3])
            enemy_type = self.randomizer.choice((Enemies.SMALL_SLIME, Enemies.SKELETON))
            self.enemies.append(Enemy(point[0], point[1], enemy_type))

    def get_random_walkable_coordinate(self, x1: int, y1: int, x2: int, y2: int) -> tuple:
        x, y = 0, 0
        while True:
            x = self.randomizer.randint(x1, x2)
            y = self.randomizer.randint(y1, y2)
            if self.tile_walkable(x, y):
                break
        return (x, y)

    def tile_walkable(self, x, y):
        if self.spawn_point and self.spawn_point == (x, y):
            return False

        for enemy in self.enemies:
            if enemy == (x, y):
                return False

        return self.get(x, y).walkable
            
    def display(self, surface, draw_other: bool=True):
        for x in range(self.width):
            for y in range(self.height):
                match self.get(x, y):
                    case Tiles.EMPTY:
                        pygame.draw.rect(surface, (25, 25, 25),
                                         (x*self.grid_size, y*self.grid_size, self.grid_size, self.grid_size))
                    case Tiles.FLOOR:
                        pygame.draw.rect(surface, 'white',
                                         (x*self.grid_size, y*self.grid_size, self.grid_size, self.grid_size))
                    case Tiles.CORRIDOR:
                        pygame.draw.rect(surface, (112, 128, 144),
                                         (x*self.grid_size, y*self.grid_size, self.grid_size, self.grid_size))
                    case Tiles.WALL_TOP:
                        pygame.draw.rect(surface, (165, 42, 42),
                                         (x*self.grid_size, y*self.grid_size, self.grid_size, self.grid_size))
                    case Tiles.WALL_SIDE:
                        pygame.draw.rect(surface, (90, 0, 0),
                                         (x*self.grid_size, y*self.grid_size, self.grid_size, self.grid_size))

        if not draw_other:
            return

        for enemy in self.enemies:
            pygame.draw.rect(surface, (255, 0, 0),
                             (enemy.x*self.grid_size, enemy.y*self.grid_size, self.grid_size, self.grid_size))

        if self.spawn_point:
            pygame.draw.rect(surface, 'green', (self.spawn_point.x * self.grid_size,
                                                self.spawn_point.y * self.grid_size,
                                                self.grid_size,
                                                self.grid_size))
