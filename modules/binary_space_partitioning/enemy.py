from modules.registry import Enemies

class Enemy:
    def __init__(self, x: int, y: int, type: Enemies):
        self.x = x
        self.y = y
        self.type: Enemies = type

    def __eq__(self, point) -> bool:
        if type(point) == tuple:
            return (self.x == point[0] and self.y == point[1])
        else:
            raise ValueError(f'Cannot compare enemy to {type(point)}')

    def __ne__(self, point):
        if type(point) == tuple:
            return (self.x != point[0] or self.y != point[1])
        else:
            raise ValueError(f'Cannot compare enemy to {type(point)}')
