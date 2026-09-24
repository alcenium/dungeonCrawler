from cell import Cell
grid_size = 20

class Map:
    """
    Map được định nghĩa bởi số phòng cần tạo, kích thước nhỏ nhất của 1 cell,
    và root cell là cell bao quát tất cả
    """
    def __init__(self, width, height):
        self.num_room = 10
        self.min_cell_dim = grid_size * 2
        self.root = Cell(32, 32, width-32, height-32)
   
    def shrink(self):
        self.root.shrink(self.min_cell_dim)

    def divide(self):
        """
        Chia nhỏ root cho đến khi có đủ số phòng yêu cầu
        """
        room = 1
        while room < self.num_room:
            if self.root.divide(self.min_cell_dim):
                room += 1

    def display(self, surface):
        self.root.display(surface)
