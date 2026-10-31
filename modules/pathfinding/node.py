import pygame
from modules.registry import Tiles
from modules.coordinate import Coordinate

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.binary_space_partitioning.map_grid import MapGrid

class Node(Coordinate):
    def __init__(self, x: int, y: int, walkable: bool) -> None:
        self.x = x
        self.y = y
        self.distance_from_start = 0
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
        return self.distance_from_start + self.distance_to_end

    def get_neighbors(self, cells):
        self.neighbors.clear()
        for pos in self.neighbors_relative_pos:
            neighbor_x = self.x + pos[0]
            neighbor_y = self.y + pos[1]
            neighbor = cells.get(neighbor_x, neighbor_y)
            if neighbor is not None:
                self.neighbors.append(neighbor)

    def __repr__(self):
        return f'(x:{self.x}, y:{self.y}, {self.walkable})'

    def __eq__(self, other):
        if other is None:
            return False
        return (self.x == other.x and self.y == other.y)

    def __ne__(self, other):
        if other is None:
            return True
        return (self.x != other.x or self.y != other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)
    
    def __lt__(self, other):
        return (self.total_distance < other.total_distance or
                self.total_distance == other.total_distance and
                self.distance_to_end < other.distance_to_end)

class NodeMap:
    def __init__(self, map):
        self.width = map.width
        self.height = map.height
        self.node_map = []
        self.process_map(map)
        self.cache_neighbor()

    def process_map(self, map: MapGrid):
        for y in range(0, map.height):
            for x in range(0, map.width):
                self.node_map.append(Node(x, y, map.is_walkable((x, y)) ))

    def update(self, updated_map):
        for y in range(0, updated_map.height):
            for x in range(0, updated_map.width):
                self.node_map[y * self.width + x].walkable = updated_map.is_walkable((x, y))

    def cache_neighbor(self):
        for node in self.node_map:
            node.get_neighbors(self)

    def reset(self):
        for node in self.node_map:
            node.distance_from_start = 0
            node.distance_to_end = 0
            node.connection = None

    def get(self, *args) -> Node | None:
        x, y = Coordinate.to_tuple(*args)
        if self.is_out_of_range(x, y):
            return None
        return self.node_map[y * self.width + x]

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
