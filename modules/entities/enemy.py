from modules.coordinate import Coordinate, CoordinateLike

class Enemy:
    def __init__(self, coordinate: Coordinate, _type: Enemies):
        self.coordinate = coordinate
        self._type      = _type
        self.hp         = 1

    def update(self, world):
        pass

    def move(self):
        pass

    def reduce_hp(self, ammount: int = 1):
        self.hp -= ammount
        print(f'{self.hp}')

    def is_nearby(self, target_position: CoordinateLike | tuple[int, int], range: int):
        target_coordinate = Coordinate.to_coordinate(target_position)

        return (abs(target_coordinate.x - self.coordinate.x) <= range and
                abs(target_coordinate.y - self.coordinate.y) <= range)

    def __repl__(self):
        return f'<x: {self.coordinate.x}, y: {self.coordinate.y}, {self._type}>'
