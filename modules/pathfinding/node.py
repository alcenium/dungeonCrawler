import pygame
from modules.registry import Tiles

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.binary_space_partitioning.map_grid import Map_Grid

class Node:
    def __init__(self, x: int, y: int, walkable: bool) -> None:
        self.x = x
        self.y = y
        self.distance_to_start = 0
        self.distance_to_end = 0
        self.walkable = walkable

        self.neighbors_relative_pos = ((-1, -1), (0, -1), (1, -1),
                                       (-1,  0),          (1,  0),
                                       (-1,  1), (0,  1), (1,  1))
        self.neighbors = []
        self.connection = None

    def distance_to(self, other):
        """ Sử dụng cách tính khoảng cách octile """
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        return 10 * max(dx, dy) + 4 * min(dx, dy)

    @property
    def total_distance(self):
        return self.distance_to_start + self.distance_to_end

    def get_neighbors(self, cells):
        self.neighbors.clear()
        for pos in self.neighbors_relative_pos:
            neighbor_x = self.x + pos[0]
            neighbor_y = self.y + pos[1]
            neighbor = cells.get(neighbor_x, neighbor_y)
            if neighbor is not None:
                self.neighbors.append(neighbor)

    def __str__(self):
        return f'(x:{self.x}, y:{self.y})'

    def __eq__(self, other):
        if other is None:
            return False
        return (self.x == other.x and self.y == other.y)

    def __ne__(self, other):
        if other is None:
            return True
        return (self.x != other.x or self.y != other.y)

class NodeMap:
    def __init__(self, map):
        self.width = map.width
        self.height = map.height
        self.node_map = []
        self.process_map(map)
        self.cache_neighbor()

    def process_map(self, map: MapGrid):
        x, y = 0, 0
        for tile in map.grid:
            self.node_map.append(Node(x, y, tile.walkable))
            x += 1
            if x >= self.width:
                x %= self.width
                y += 1

    def cache_neighbor(self):
        for node in self.node_map:
            node.get_neighbors(self)

    def reset(self):
        for node in self.node_map:
            node.distance_to_start = 0
            node.distance_to_end = 0
    def get(self, x: int, y: int) -> Node | None:
        if self.is_out_of_range(x, y):
            return None
        return self.node_map[y * self.width + x]

    def set(self, x: int, y: int, value: Node):
        if self.is_out_of_range(x, y):
            return False
        self.node_map[y * self.width + x]
        return True

    def is_out_of_range(self, x, y):
        return (x >= self.width or y >= self.height or x < 0 or y < 0)

    def display(self, surface):
        x, y = 0, 0
        for node in self.node_map:
            if node.walkable:
                pygame.draw.rect(surface, 'white', (x * 16, y * 16, 16, 16))
            else:
                pygame.draw.rect(surface, 'gray', (x * 16, y * 16, 16, 16))

            x += 1
            if x >= self.width:
                x %= self.width
                y += 1
