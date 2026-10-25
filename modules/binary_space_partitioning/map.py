from random import Random

from modules.binary_space_partitioning.cell import Cell
from modules.binary_space_partitioning.corridor import Corridor
from modules.binary_space_partitioning.map_grid import MapGrid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.binary_space_partitioning.spawn_point import SpawnPoint

class Map:
    """ Map được định nghĩa bởi số phòng cần tạo, kích thước nhỏ nhất của 1 cell,
        và root cell là cell bao quát tất cả
    """
    def __init__(self, width: int,
                 height: int,
                 randomizer: Random,
                 grid_size: int = 16,
                 room_count: int = 10,
                 min_size: int = 2) -> None:
        self.width             = width
        self.height            = height
        self.randomizer        = randomizer
        self.room_count        = room_count
        self.grid_size         = grid_size
        self.min_cell_dim      = min_size

        self.root : Cell       = Cell(grid_size, grid_size, width-grid_size, height-grid_size, randomizer, grid_size)
        self.cells: list[Cell] = []
   
    def divide(self) -> None:
        """ Chia nhỏ root cho đến khi có đủ số phòng yêu cầu """
        room = 1
        while room < self.room_count:
            if self.root.divide(self.min_cell_dim):
                room += 1

    def get_neighbors(self) -> None:
        """ Thêm các phòng vào danh sách cells,
            Thêm hàng xóm chiều ngang và dọc vào danh sách hàng xóm của từng phòng
        """
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

    def shrink(self) -> None:
        """ Thu nhỏ tất cả các cell con của cell root """
        self.root.shrink(self.min_cell_dim)

    def add_corridors(self) -> None:
        """ Thêm hành lang kết nối các phòng dựa trên hàng xóm của từng cell """
        for cell in self.cells:
            for neighbor in cell.horizontal_neighbors:
                if min(cell.y2, neighbor.y2) - max(cell.y1, neighbor.y1) > self.grid_size:
                    y = self.randomizer.randint(max(cell.y1, neighbor.y1),
                                                min(cell.y2, neighbor.y2) - self.grid_size)
                    cell.horizontal_corridors.append(Corridor(cell.x2, y, neighbor.x1, y + self.grid_size))

            for neighbor in cell.vertical_neighbors:
                if min(cell.x2, neighbor.x2) - max(cell.x1, neighbor.x1) > self.grid_size:
                    x = self.randomizer.randint(max(cell.x1, neighbor.x1),
                                                min(cell.x2, neighbor.x2) - self.grid_size)
                    cell.vertical_corridors.append(Corridor(x, cell.y2, x + self.grid_size, neighbor.y1))

    def reduce_corridor(self) -> None:
        """ Note: sửa sau """
        for cell in self.cells:
            cell.reduce_corridor()

    def align(self) -> None:
        """ Căn tọa độ các phòng và hành lang cho trùng với grid tọa độ """
        for cell in self.cells:
            cell.align()

    def display(self, surface) -> None:
        """ Hiển thị tất cả lên mặt phẳng được chỉ định """
        self.root.display(surface)

    def to_grid(self) -> MapGrid:
        """ Chuyển tất cả vật thể trong map thành grid tọa độ, và các
            điểm trên grid tọa độ và trả về MapGrid object chứa tất cả vật thể, tile
        """
        map_grid = MapGrid(self.width // self.grid_size,
                           self.height // self.grid_size,
                           self.grid_size,
                           self.randomizer)

        for cell in self.cells:
            map_grid.rooms.append(cell.to_room_on_grid())
            cell.to_grid(map_grid)

        return map_grid
