from modules.pathfinding.node import Node

class AStar:
    def __init__(self, start: Node, end: Node, debug=False):
        self.start = start
        self.end   = end
        self.start.distance_to_end = self.start.distance_to(self.end)

        self.searching = [self.start]
        self.processed = []
        self.path = []
        self.current = self.searching[0]

        self.debug = debug

    def pathfind(self):
        while self.searching and not self.path:
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
                    self.processed.remove(current_path_tile)
                    self.path.append(current_path_tile)
                    current_path_tile = current_path_tile.connection
                self.path.append(current_path_tile)
                return self.path_to_coordinate()

            for neighbor in self.current.neighbors:
                if neighbor.walkable == False or neighbor in self.processed:
                    continue
                
                already_searching = neighbor in self.searching
                cost_to_neighbor = self.current.distance_to_start + self.current.distance_to(neighbor)

                if not already_searching or cost_to_neighbor < neighbor.distance_to_start:
                    neighbor.distance_to_start = cost_to_neighbor
                    neighbor.connection = self.current

                    if not already_searching:
                        neighbor.distance_to_end = neighbor.distance_to(self.end)
                        self.searching.append(neighbor)
            if self.debug:
                break

    def path_to_coordinate(self):
        coordinate_list = []
        for node in self.path:
            coordinate_list.append((node.x, node.y))
        coordinate_list.reverse()
        return coordinate_list
