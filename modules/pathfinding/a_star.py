from modules.pathfinding.node import Node
from modules.pathfinding.node import NodeMap
from modules.binary_space_partitioning.map_grid import MapGrid

class AStar:
    def __init__(self, map: MapGrid):
        self.node_map = NodeMap(map)
        self.start = None
        self.end   = None

        self.searching = []
        self.processed = []
        self.path = []
        self.current = None

    def reset_path(self, start, end):
        self.start = self.node_map.get(start)
        self.end   = self.node_map.get(end)
        self.start.distance_to_end = self.start.distance_to(self.end)

        self.searching = [self.start]
        self.current = self.searching[0]

        self.processed = []
        self.path = []
        self.node_map.reset()

    def update_map(self, new_map):
        self.node_map.update(new_map)

    def pathfind(self, start, end) -> list[tuple]:
        self.reset_path(start, end)

        returned = None
        while self.searching and not self.path:
            returned = self.step()
        return returned

    def step(self):
        self.current = self.searching[0]

        for node in self.searching:
            if (node.total_distance <  self.current.total_distance or
                node.total_distance == self.current.total_distance and
                node.distance_to_end < self.current.distance_to_end):
                self.current = node

        self.processed.append(self.current)
        self.searching.remove(self.current)

        if self.current == self.end:
            current_path_tile = self.current
            self.path = []

            while current_path_tile != self.start:
                self.path.append(current_path_tile - current_path_tile.connection)
                current_path_tile = current_path_tile.connection

            return self.path_to_coordinate()

        for neighbor in self.current.neighbors:
            if neighbor.walkable == False or neighbor in self.processed:
                continue
            
            already_searching = neighbor in self.searching
            cost_to_neighbor = self.current.distance_from_start + self.current.distance_to(neighbor)

            if not already_searching or cost_to_neighbor < neighbor.distance_from_start:
                neighbor.distance_from_start = cost_to_neighbor
                neighbor.connection = self.current

                if not already_searching:
                    neighbor.distance_to_end = neighbor.distance_to(self.end)
                    self.searching.append(neighbor)
        return None

    def path_to_coordinate(self):
        coordinate_list = []
        for node in self.path:
            coordinate_list.append((node.x, node.y))
        coordinate_list.reverse()
        return coordinate_list
