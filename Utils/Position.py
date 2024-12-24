import math

from Utils.Direction import Direction


class Position:
    def __init__(self, row, column):
        self.r = row
        self.c = column

    def neighbors(self, mode='orthogonal') -> list['Position']:
        neighbors = [self.down, self.up, self.right, self.left]
        if mode == 'diagonal':
            neighbors.extend([self.up_left, self.up_right, self.down_left, self.down_right])
        return neighbors

    def direction_to(self, other: 'Position') -> Direction:
        if other is None or self == other:
            return Direction(Direction.NONE)
        if self.r == other.r:
            if self.c < other.c:
                return Direction(Direction.RIGHT)
            return Direction(Direction.LEFT)
        if self.c == other.c:
            if self.r < other.r:
                return Direction(Direction.DOWN)
            return Direction(Direction.UP)
        return Direction(Direction.NONE)

    def direction_from(self, other: 'Position') -> Direction:
        return other.direction_to(self)

    def distance_to(self, other: 'Position') -> float:
        return math.sqrt(math.pow(abs(self.r - other.r),2) + math.pow(abs(self.c - other.c),2))

    def next(self, direction: Direction) -> 'Position':
        if direction == Direction.DOWN:
            return self.down
        if direction == Direction.RIGHT:
            return self.right
        if direction == Direction.UP:
            return self.up
        if direction == Direction.LEFT:
            return self.left
        return self

    @property
    def left(self):
        return Position(self.r, self.c - 1)

    @property
    def right(self):
        return Position(self.r, self.c + 1)

    @property
    def up(self):
        return Position(self.r - 1, self.c)

    @property
    def down(self):
        return Position(self.r + 1, self.c)

    @property
    def up_left(self):
        return Position(self.r - 1, self.c - 1)

    @property
    def up_right(self):
        return Position(self.r - 1, self.c + 1)

    @property
    def down_left(self):
        return Position(self.r + 1, self.c - 1)

    @property
    def down_right(self):
        return Position(self.r + 1, self.c + 1)

    def __eq__(self, other):
        return isinstance(other, Position) and self.r == other.r and self.c == other.c

    def __hash__(self):
        return hash((self.r, self.c))

    def __str__(self):
        return f'({self.r}, {self.c})'

    def __repr__(self):
        return f'Position{self.__str__()}'

    def __add__(self, other):
        return Position(self.r + other.r, self.c + other.c)

    def __sub__(self, other):
        return Position(self.r - other.r, self.c - other.c)

    def __mul__(self, other):
        return Position(self.r * other, self.c * other)

    def __truediv__(self, other):
        return Position(self.r / other, self.c / other)

    def __floordiv__(self, other):
        return Position(self.r // other, self.c // other)

    def __mod__(self, other):
        return Position(self.r % other, self.c % other)

    def __lt__(self, other):
        return self.r < other.r or (self.r == other.r and self.c < other.c)

    def __le__(self, other):
        return self.r <= other.r or (self.r == other.r and self.c <= other.c)

    def __gt__(self, other):
        return self.r > other.r or (self.r == other.r and self.c > other.c)

    def __ge__(self, other):
        return self.r >= other.r or (self.r == other.r and self.c >= other.c)

    def __getitem__(self, item):
        return self.r if item == 0 else self.c

    def __setitem__(self, key, value):
        if key == 0:
            self.r = value
        else:
            self.c = value

    def __iter__(self):
        return iter([self.r, self.c])

    def __neg__(self):
        return Position(-self.r, -self.c)
