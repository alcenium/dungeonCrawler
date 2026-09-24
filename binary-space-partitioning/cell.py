import pygame
import random

class Cell:
    """
    Cell được định nghĩa bởi góc trên cùng bên trái (x1, y1) và góc dưới bên phải (x2, y2).
    Nó chứa 2 Cell con chia ra theo đường dọc là trái và phải
    """
    def __init__(self, x1, y1, x2, y2):
        random.seed()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.left = None
        self.right = None

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
            if random.randint(1, 2) == 1:
                return self.left.divide(min_cell_dim)
            else:
                return self.right.divide(min_cell_dim)

        if w > h:
            new_mid_point = self.x1 + w * (random.randint(3, 6) / 10)
            self.left = Cell(self.x1, self.y1, new_mid_point, self.y2)
            self.right = Cell(new_mid_point, self.y1, self.x2, self.y2)
            return True
        else:
            new_mid_point = self.y1 + h * (random.randint(3, 6) / 10)
            self.left = Cell(self.x1, self.y1, self.x2, new_mid_point)
            self.right = Cell(self.x1, new_mid_point, self.x2, self.y2)
            return True

    def shrink(self, min_cell_dim):
        """
        Thu nhỏ cell trong 1 khoảng ngẫu nhiên cố định bằng cách dịch 4 góc về phía trung tâm của cell
        Nếu cell con có tồn tại, thu nhỏ chúng thay vì cell hiện tại
        """
        if self.left == None:
            w = self.x2 - self.x1
            h = self.y2 - self.y1
            new_w = max(w * random.uniform(0.25, 0.9), min_cell_dim)
            new_h = max(h * random.uniform(0.25, 0.9), min_cell_dim)

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
            pygame.draw.rect(surface, 'purple',
                             (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))
            pygame.draw.rect(surface, 'white',
                             (self.x1+3, self.y1+3, self.x2-self.x1-6, self.y2-self.y1-6))
