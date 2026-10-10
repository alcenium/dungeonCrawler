from modules.binary_space_partitioning.cell import Cell
from modules.binary_space_partitioning.corridor import Corridor
from modules.binary_space_partitioning.map_grid import MapGrid

class Map:
    """
    Map được định nghĩa bởi số phòng cần tạo, kích thước nhỏ nhất của 1 cell,
    và root cell là cell bao quát tất cả
    """
    def __init__(self, width, height, randomizer, grid_size=16, room_count=10):
        self.width        = width
        self.height       = height
        self.randomizer   = randomizer
        self.room_count   = room_count
        self.grid_size    = grid_size
        self.min_cell_dim = grid_size * 2
        self.root         = Cell(grid_size, grid_size, width-grid_size, height-grid_size, randomizer, grid_size)
        self.cells        = []
   
    def divide(self):
        """
        Chia nhỏ root cho đến khi có đủ số phòng yêu cầu
        """
        room = 1
        while room < self.room_count:
            if self.root.divide(self.min_cell_dim):
                room += 1

    def get_neighbors(self):
        self.root.get_leaves(self.cells)
        for cell in self.cells:
            for other in self.cells:
                if cell == other:
                    continue

                if cell.x2 == other.x1:
                    if max(cell.y1, other.y1) < min(cell.y2, other.y2):
                        cell.horizontal_neighbors.append(other)

                if cell.y2 == other.y1:
                    if max(cell.x1, other.x1) < min(cell.x2, other.x2):
                        cell.vertical_neighbors.append(other)

    def shrink(self):
        self.root.shrink(self.min_cell_dim)

    def add_corridors(self):
        for cell in self.cells:
            for neighbor in cell.horizontal_neighbors:
                if min(cell.y2, neighbor.y2) - max(cell.y1, neighbor.y1) > self.grid_size:
                    y = self.randomizer.uniform(max(cell.y1, neighbor.y1),
                                       min(cell.y2, neighbor.y2) - self.grid_size)
                    cell.horizontal_corridors.append(Corridor(cell.x2, y, neighbor.x1, y + self.grid_size))

            for neighbor in cell.vertical_neighbors:
                if min(cell.x2, neighbor.x2) - max(cell.x1, neighbor.x1) > self.grid_size:
                    x = self.randomizer.uniform(max(cell.x1, neighbor.x1),
                                       min(cell.x2, neighbor.x2) - self.grid_size)
                    cell.vertical_corridors.append(Corridor(x, cell.y2, x + self.grid_size, neighbor.y1))

    def reduce_corridor(self):
        for cell in self.cells:
            cell.reduce_corridor()

    def align(self):
        for cell in self.cells:
            cell.align()

    def display(self, surface):
        self.root.display(surface)

    def add_spawn_point(self):
        cell = self.randomizer.choice(self.cells)
        cell.add_spawn_point()

    def to_grid(self):
        map_grid = MapGrid(self.width // self.grid_size,
                           self.height // self.grid_size, self.grid_size)

        for cell in self.cells:
            cell.to_grid(map_grid)

        return map_grid
