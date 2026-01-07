class Size:
    _width: int
    _height: int

    def __init__(self, width: int = 5, height: int = 5):
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("Width and height must be integer")

        self.width = width
        self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        if value > 0:
            self._width = value
        else:
            raise ValueError("Width must be greater than zero")

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        if value > 0:
            self._height = value
        else:
            raise ValueError("Height must be greater than zero")

    def to_tuple(self):
        return (self._width, self._height)

    def __deepcopy__(self, memo: dict[int, object]):
        size_copy = type(self)(self.width, self.height)

        memo[id(self)] = self
        memo[id(size_copy)] = size_copy

        return size_copy

    def __bool__(self):
        return self.width > 0 and self.height > 0

    def __repr__(self):
        return f"({self.width}; {self.height})"
