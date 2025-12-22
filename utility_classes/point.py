from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __init__(self, x: int = 0, y: int = 0) -> None:
        types = (int, float)
        if not isinstance(x, types) or not isinstance(y, types):
            raise TypeError("Width and height must be integer")

        self.x = x
        self.y = y

    def to_tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"({self.x}; {self.y})"
