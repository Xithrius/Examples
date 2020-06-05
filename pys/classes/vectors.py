import math
import typing as t


class Vector:
    """Class for a very simple vector of [x, y]."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return '<Vector Object; {0.x=}, {0.y=}>'.format(self)

    def __abs__(self) -> t.Union[int, float]:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __len__(self):
        return abs(self)

    def __add__(self, vector0):
        return Vector(self.x + vector0.x, self.y + vector0.y)

    def __sub__(self, vector0):
        return Vector(self.x - vector0.x, self.y - vector0.y)
