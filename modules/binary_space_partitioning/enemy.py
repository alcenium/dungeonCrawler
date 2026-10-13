from modules.registry import Enemies

class Enemy:
    def __init__(self, x: int, y: int, type: Enemies):
        self.x = x
        self.y = y
        self.type: Enemies = type

    def align(self, grid_size: int) -> None:
        self.x -= self.x % grid_size
        self.y -= self.y % grid_size

    def to_grid(self, grid_size: int):
        x = self.x // grid_size
        y = self.y // grid_size
        return Enemy(x, y, self.type)
