class Enemy:
    def __init__(self, coordinate: GridCoordinate, _type: Enemies):
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

    def __repl__(self):
        return f'<x: {self.coordinate.x}, y: {self.coordinate.y}, {self._type}>'
