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

    def straddled_neighbors(self) -> set['Position']:
        r_floor = math.floor(self.r)
        c_floor = math.floor(self.c)
        r_ceil = math.ceil(self.r)
        c_ceil = math.ceil(self.c)
        return {Position(r_floor, c_floor), Position(r_floor, c_ceil), Position(r_ceil, c_floor), Position(r_ceil, c_ceil)}

    def direction_to(self, other: 'Position') -> Direction:
        if other is None or self == other:
            return Direction(Direction.none())
        if self.r == other.r:
            if self.c < other.c:
                return Direction.right()
            return Direction.left()
        if self.c == other.c:
            if self.r < other.r:
                return Direction.down()
            return Direction.up()
        return Direction(Direction.none())

    def direction_from(self, other: 'Position') -> Direction:
        return other.direction_to(self)

    def distance_to(self, other: 'Position') -> float:
        return math.sqrt(math.pow(abs(self.r - other.r), 2) + math.pow(abs(self.c - other.c), 2))

    def next(self, direction: Direction, count=1) -> 'Position':
        if direction == Direction.down():
            return Position(self.r + count, self.c)
        if direction == Direction.right():
            return Position(self.r, self.c + count)
        if direction == Direction.up():
            return Position(self.r - count, self.c)
        if direction == Direction.left():
            return Position(self.r, self.c - count)
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

    def get_positions_to(self, position: 'Position') -> list['Position']:
        if self.r == position.r:
            return [Position(self.r, c) for c in range(min(self.c, position.c) + 1, max(self.c, position.c))]
        if self.c == position.c:
            return [Position(r, self.c) for r in range(min(self.r, position.r) + 1, max(self.r, position.r))]
        return []

    def symmetric(self, position, to_int=True) -> 'Position':
        if to_int:
            return Position(int(2 * position.r - self.r), int(2 * position.c - self.c))
        return Position(2 * position.r - self.r, 2 * position.c - self.c)

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
