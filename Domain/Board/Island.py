import typing

from Domain.Board.Direction import Direction
from Domain.Board.Position import Position

IslandString0Bridge = typing.Literal[
    '   ', ' X ', ' · '
]
IslandString1Bridge = typing.Literal[
    ' ╶─', ' ╵ ', '─╴ ', ' ╷ ',
]
IslandString2Bridges = typing.Literal[
    ' └─', '─┘ ', '─┐ ', ' ┌─',
    ' │ ', '───',
]
IslandString3Bridges = typing.Literal[
    '─┬─', ' ├─', '─┴─', '─┤ ',
]
IslandString4Bridges = typing.Literal[
    '─┼─'
]
IslandString = typing.Union[
    IslandString0Bridge,
    IslandString1Bridge,
    IslandString2Bridges,
    IslandString3Bridges,
    IslandString4Bridges
]
IslandWithBridgesString = typing.Union[
    IslandString1Bridge,
    IslandString2Bridges,
    IslandString3Bridges,
    IslandString4Bridges,
]


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

    @staticmethod
    def from_str(position: Position, island_string: IslandString):
        initial_position_bridges = {
            position.up: 0,
            position.down: 0,
            position.left:  0,
            position.right: 0,
        }
        island = Island(position, 0, initial_position_bridges)

        match island_string:
            case ' ╵ ':
                island.set_bridge_to_direction(Direction.up(), 1)
            case ' ╷ ':
                island.set_bridge_to_direction(Direction.down(), 1)
            case ' ╶─':
                island.set_bridge_to_direction(Direction.right(), 1)
            case '─╴ ':
                island.set_bridge_to_direction(Direction.left(), 1)

            case ' └─':
                island.set_bridge_to_direction(Direction.up(), 1)
                island.set_bridge_to_direction(Direction.right(), 1)
            case '─┘ ':
                island.set_bridge_to_direction(Direction.up(), 1)
                island.set_bridge_to_direction(Direction.left(), 1)
            case '─┐ ':
                island.set_bridge_to_direction(Direction.down(), 1)
                island.set_bridge_to_direction(Direction.left(), 1)
            case ' ┌─':
                island.set_bridge_to_direction(Direction.down(), 1)
                island.set_bridge_to_direction(Direction.right(), 1)
            case ' │ ':
                island.set_bridge_to_direction(Direction.up(), 1)
                island.set_bridge_to_direction(Direction.down(), 1)
            case '───':
                island.set_bridge_to_direction(Direction.left(), 1)
                island.set_bridge_to_direction(Direction.right(), 1)

            case '─┬─':
                island.set_bridge_to_direction(Direction.down(), 1)
                island.set_bridge_to_direction(Direction.left(), 1)
                island.set_bridge_to_direction(Direction.right(), 1)
            case ' ├─':
                island.set_bridge_to_direction(Direction.up(), 1)
                island.set_bridge_to_direction(Direction.down(), 1)
                island.set_bridge_to_direction(Direction.right(), 1)
            case '─┴─':
                island.set_bridge_to_direction(Direction.up(), 1)
                island.set_bridge_to_direction(Direction.left(), 1)
                island.set_bridge_to_direction(Direction.right(), 1)
            case '─┤ ':
                island.set_bridge_to_direction(Direction.up(), 1)
                island.set_bridge_to_direction(Direction.down(), 1)
                island.set_bridge_to_direction(Direction.left(), 1)

            case '─┼─':
                island.set_bridge_to_direction(Direction.up(), 1)
                island.set_bridge_to_direction(Direction.down(), 1)
                island.set_bridge_to_direction(Direction.left(), 1)
                island.set_bridge_to_direction(Direction.right(), 1)

        island.set_bridges_count_according_to_directions_bridges()
        return island

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
        return isinstance(other,
                          Island) and self.position == other.position and self.bridges_count == other.bridges_count and self.direction_position_bridges == other.direction_position_bridges

    def __hash__(self):
        return hash(self.position)

    def __repr__(self):
        if self.has_no_bridge():
            return ' · '
        if self.bridges_number(Direction.up()) != 0 and self.bridges_number(Direction.down()) != 0 and self.bridges_number(Direction.left()) != 0 and self.bridges_number(
                Direction.right()) != 0:
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
