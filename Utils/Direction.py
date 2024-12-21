class Direction:
    DOWN = 1
    RIGHT = 2
    UP = 3
    LEFT = 4
    NONE = 0

    def __init__(self, value):
        if isinstance(value, str):
            if value == 'down':
                self._value = Direction.DOWN
                return
            if value == 'right':
                self._value = Direction.RIGHT
                return
            if value == 'up':
                self._value = Direction.UP
                return
            if value == 'left':
                self._value = Direction.LEFT
                return
            else:
                raise ValueError(f"Unknown direction {value}")
        if value not in [Direction.DOWN, Direction.RIGHT, Direction.UP, Direction.LEFT] and value != Direction.NONE:
            raise ValueError(f"Unknown direction {value}")
        self._value = value

    @staticmethod
    def get_directions():
        return [Direction.DOWN, Direction.RIGHT, Direction.UP, Direction.LEFT]

    @property
    def opposite(self):
        if self.value == Direction.DOWN:
            return Direction(Direction.UP)
        if self.value == Direction.UP:
            return Direction(Direction.DOWN)
        if self.value == Direction.RIGHT:
            return Direction(Direction.LEFT)
        if self.value == Direction.LEFT:
            return Direction(Direction.RIGHT)
        return Direction(Direction.NONE)

    @property
    def value(self):
        return self._value

    def __str__(self):
        if self._value == Direction.DOWN:
            return '↓'
        if self._value == Direction.RIGHT:
            return '→'
        if self._value == Direction.UP:
            return '↑'
        if self._value == Direction.LEFT:
            return '←'
        return 'x'

    def __eq__(self, other):
        if isinstance(other, Direction) and self.value == other.value:
            return True
        if isinstance(other, str):
            return self.__str__() == other
        if isinstance(other, int) and self.value == other:
            return True
        return False

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def between(position1, position2):
        if position1.r == position2.r and position1.c == position2.c:
            return Direction(Direction.NONE)
        if position1.r == position2.r:
            if position1.c < position2.c:
                return Direction(Direction.RIGHT)
            return Direction(Direction.LEFT)
        if position1.c == position2.c:
            if position1.r < position2.r:
                return Direction(Direction.DOWN)
            return Direction(Direction.UP)
        return Direction(Direction.NONE)
