class GridCoordinate:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def __add__(self, other) -> GridCoordinate:
        match other:
            case GridCoordinate():
                return GridCoordinate(self.x + other.x, self.y + other.y)
            case (x, y):
                return GridCoordinate(self.x + x, self.y + y)
            case _:
                raise TypeError(f"Grid Coordinate doesn't support type {type(other)}")

    def __iadd__(self, other):
        match other:
            case GridCoordinate():
                self.x += other.x
                self.y += other.y
                return self
            case (x, y):
                self.x += x
                self.y += y
                return self
            case _:
                raise TypeError(f"Grid Coordinate doesn't support type {type(other)}")

    def __imul__(self, other):
        match other:
            case GridCoordinate():
                self.x *= other.x
                self.y *= other.y
                return self
            case (x, y):
                self.x *= x
                self.y *= y
                return self
            case _:
                raise TypeError(f"Grid Coordinate doesn't support type {type(other)}")

    def __eq__(self, other):
        match other:
            case GridCoordinate():
                return (self.x == other.x and self.y == other.y)
            case (x, y):
                return (self.x == x and self.y == y)
            case _:
                raise TypeError(f"Grid Coordinate doesn't support type {type(other)}")

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"
