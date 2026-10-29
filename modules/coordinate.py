from typing import TypeAlias

class Coordinate:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    @staticmethod
    def to_coordinate(input):
        match input:
            case Coordinate():
                return input
            case (x, y):
                return Coordinate(x, y)
            case _:
                raise ValueError(f'Unsupported type of {type(input)}')
    
    @staticmethod
    def to_tuple(*inputs):
        x, y = 0, 0
        match inputs[0]:
            case int():
                x = inputs[0]
                y = inputs[1]
            case (pos1, pos2):
                x = pos1
                y = pos2
            case Coordinate():
                x = inputs[0].x
                y = inputs[0].y
            case _:
                print(inputs[0])
                print(type(inputs[0]))
                raise ValueError(f"Cannot handle type {type(inputs[0])}")
        return (x, y)

    def __add__(self, other) -> Coordinate:
        match other:
            case Coordinate():
                return Coordinate(self.x + other.x, self.y + other.y)
            case (x, y):
                return Coordinate(self.x + x, self.y + y)
            case _:
                raise TypeError(f"Coordinate doesn't support type {type(other)}")

    def __iadd__(self, other):
        match other:
            case Coordinate():
                self.x += other.x
                self.y += other.y
                return self
            case (x, y):
                self.x += x
                self.y += y
                return self
            case _:
                raise TypeError(f"Coordinate doesn't support type {type(other)}")

    def __imul__(self, other):
        match other:
            case Coordinate():
                self.x *= other.x
                self.y *= other.y
                return self
            case (x, y):
                self.x *= x
                self.y *= y
                return self
            case _:
                raise TypeError(f"Coordinate doesn't support type {type(other)}")

    def __eq__(self, other):
        match other:
            case Coordinate():
                return (self.x == other.x and self.y == other.y)
            case (x, y):
                return (self.x == x and self.y == y)
            case _:
                raise TypeError(f"Coordinate doesn't support type {type(other)}")

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"

CoordinateLike: TypeAlias = (
    Coordinate
    | tuple[int, int]
    | list[int]
)
