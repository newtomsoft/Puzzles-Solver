
from Domain.Board.Direction import Direction
from Domain.Board.Position import Position


class Island:
    def __init__(self, position: Position, bridges: int, positions_bridges: dict[Position, int] = None):
        self.position = position
        self.bridges_count = bridges
        if bridges < 0 or bridges > 8:
            raise ValueError("Bridges must be between 0 and 8")
        self.direction_position_bridges: dict[Direction, tuple[Position, int]] = {}
        if positions_bridges is not None:
            for position, bridges in positions_bridges.items():
                self.set_bridge_to_position(position, bridges)

    def set_bridge_to_position(self, position: Position, number: int):
        direction = self.position.direction_to(position)
        self.direction_position_bridges[direction] = position, number

    def set_bridge_to_direction(self, direction: Direction, number: int):
        to_position = self.position.after(direction)
        self.direction_position_bridges[direction] = to_position, number

    def set_bridges_count_according_to_directions_bridges(self):
        self.bridges_count = sum([bridges for (_, bridges) in self.direction_position_bridges.values()])

    def has_no_bridge(self):
        return self.bridges_count == 0

    def __eq__(self, other):
        return isinstance(other, Island) and self.position == other.position and self.bridges_count == other.bridges_count and self.direction_position_bridges == other.direction_position_bridges

    def __repr__(self):
        if self.has_no_bridge():
            return '   '
        if self.bridges_number(Direction.up()) != 0 and self.bridges_number(Direction.down()) != 0 and self.bridges_number(Direction.left()) != 0 and self.bridges_number(Direction.right()) != 0:
            return '─┼─'
        if self.bridges_number(Direction.up()) != 0 and self.bridges_number(Direction.left()) != 0 and self.bridges_number(Direction.right()) != 0:
            return '─┴─'
        if self.bridges_number(Direction.down()) != 0 and self.bridges_number(Direction.left()) != 0 and self.bridges_number(Direction.right()) != 0:
            return '─┬─'
        if self.bridges_number(Direction.up()) != 0 and self.bridges_number(Direction.down()) != 0 and self.bridges_number(Direction.left()) != 0:
            return '─┤ '
        if self.bridges_number(Direction.up()) != 0 and self.bridges_number(Direction.down()) != 0 and self.bridges_number(Direction.right()) != 0:
            return ' ├─'
        if self.bridges_number(Direction.up()) != 0 and self.bridges_number(Direction.left()) != 0:
            return '─┘ '
        if self.bridges_number(Direction.up()) != 0 and self.bridges_number(Direction.right()) != 0:
            return ' └─'
        if self.bridges_number(Direction.down()) != 0 and self.bridges_number(Direction.left()) != 0:
            return '─┐ '
        if self.bridges_number(Direction.right()) != 0 and self.bridges_number(Direction.down()) != 0:
            return ' ┌─'
        if self.bridges_number(Direction.up()) != 0 and self.bridges_number(Direction.down()) != 0:
            return ' │ '
        if self.bridges_number(Direction.down()) != 0:
            return ' ╷ '
        if self.bridges_number(Direction.up()) != 0:
            return ' ╵ '
        if self.bridges_number(Direction.right()) != 0 and self.bridges_number(Direction.left()) != 0:
            return '───'
        if self.bridges_number(Direction.right()) != 0:
            return ' ╶─'
        if self.bridges_number(Direction.left()) != 0:
            return '─╴ '
        return ' X '

    def bridges_number(self, direction: Direction):
        return self.direction_position_bridges.get(direction, (0, 0))[1]
