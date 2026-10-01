import pygame

class Cell:
    """
    Cell được định nghĩa bởi góc trên cùng bên trái (x1, y1) và góc dưới bên phải (x2, y2).
    Nó chứa 2 Cell con chia ra theo đường dọc là trái và phải
    """
    def __init__(self, x1, y1, x2, y2, randomizer):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.left = None
        self.right = None
        self.randomizer = randomizer
        self.horizontal_neighbors = []
        self.vertical_neighbors = []
        self.horizontal_corridors = []
        self.vertical_corridors = []

    def get_leaves(self, cells):
        if self.left == None:
            cells.append(self)
        else:
            self.left.get_leaves(cells)
            self.right.get_leaves(cells)

    def divide(self, min_cell_dim):
        """
        Chia nhỏ cell ra thành cell trái & phải/trên & dưới, trên cạnh lớn hơn
        Nếu cell có cell con, chọn ngẫu nhiên 1 cell con và chia nhỏ nó
        """
        w = self.x2 - self.x1
        h = self.y2 - self.y1

        if w < min_cell_dim and h < min_cell_dim:
            return False

        if self.left != None:
            if self.randomizer.randint(1, 2) == 1:
                return self.left.divide(min_cell_dim)
            else:
                return self.right.divide(min_cell_dim)

        if w > h:
            new_mid_point = self.x1 + w * (self.randomizer.randint(3, 6) / 10)
            self.left = Cell(self.x1, self.y1, new_mid_point, self.y2, self.randomizer)
            self.right = Cell(new_mid_point, self.y1, self.x2, self.y2, self.randomizer)
            return True
        else:
            new_mid_point = self.y1 + h * (self.randomizer.randint(3, 6) / 10)
            self.left = Cell(self.x1, self.y1, self.x2, new_mid_point, self.randomizer)
            self.right = Cell(self.x1, new_mid_point, self.x2, self.y2, self.randomizer)
            return True

    def shrink(self, min_cell_dim):
        """
        Thu nhỏ cell trong 1 khoảng ngẫu nhiên cố định bằng cách dịch 4 góc về phía trung tâm của cell
        Nếu cell con có tồn tại, thu nhỏ chúng thay vì cell hiện tại
        """
        if self.left == None:
            w = self.x2 - self.x1
            h = self.y2 - self.y1
            new_w = max(w * self.randomizer.uniform(0.25, 0.9), min_cell_dim)
            new_h = max(h * self.randomizer.uniform(0.25, 0.9), min_cell_dim)

            self.x1 += 0.5 * (w - new_w)
            self.x2 -= 0.5 * (w - new_w)
            self.y1 += 0.5 * (h - new_h)
            self.y2 -= 0.5 * (h - new_h)
        else:
            self.left.shrink(min_cell_dim)
            self.right.shrink(min_cell_dim)

    def display(self, surface):
        """ Vẽ viền ngoài màu tím, bên trong màu trắng để thể hiện 1 cell """
        if self.left != None:
            self.left.display(surface)
            self.right.display(surface)
        else:
            pygame.draw.rect(surface, 'purple', (self.x1,
                                                 self.y1,
                                                 self.x2-self.x1,
                                                 self.y2-self.y1))

            pygame.draw.rect(surface, 'white',  (self.x1+3,
                                                 self.y1+3,
                                                 self.x2-self.x1-6,
                                                 self.y2-self.y1-6))
            if self.horizontal_neighbors:
                pygame.draw.rect(surface, 'green', (self.x2-3,
                                                    self.y1,
                                                    3,
                                                    self.y2-self.y1))
            if self.vertical_neighbors:
                pygame.draw.rect(surface, 'cyan',  (self.x1,
                                                    self.y2-3,
                                                    self.x2-self.x1,
                                                    3))
            for corridor in self.horizontal_corridors:
                corridor.display(surface)
            for corridor in self.vertical_corridors:
                corridor.display(surface)

    def align(self, grid_size):
        self.x1 -= self.x1 % grid_size
        self.y1 -= self.y1 % grid_size
        self.x2 -= self.x2 % grid_size
        self.y2 -= self.y2 % grid_size
        for corridor in self.horizontal_corridors:
            corridor.align(grid_size)
        for corridor in self.vertical_corridors:
            corridor.align(grid_size)

    def reduce_corridor(self):
        if self.horizontal_corridors and self.vertical_corridors:
            match self.randomizer.randint(1, 2):
                case 1:
                    self.vertical_corridors.pop(0)
                case 2:
                    self.horizontal_corridors.pop(0)

    def __str__(self):
        return f'[(x1:{self.x1}, y1:{self.y1}), (x2:{self.x2}, y2:{self.y2})]'
