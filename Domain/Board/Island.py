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

        up = self.bridges_number(Direction.up())
        down = self.bridges_number(Direction.down())
        left = self.bridges_number(Direction.left())
        right = self.bridges_number(Direction.right())

        left_char = ' '
        if left == 1:
            left_char = '─'
        elif left == 2:
            left_char = '═'

        right_char = ' '
        if right == 1:
            right_char = '─'
        elif right == 2:
            right_char = '═'

        center_map = {
            (1, 1, 1, 1): '┼',
            (2, 2, 2, 2): '╬',
            (2, 2, 1, 1): '╫',
            (1, 1, 2, 2): '╪',

            (0, 1, 1, 1): '┬',
            (0, 2, 2, 2): '╦',
            (0, 1, 2, 2): '╤',
            (0, 2, 1, 1): '╥',

            (1, 0, 1, 1): '┴',
            (2, 0, 2, 2): '╩',
            (1, 0, 2, 2): '╧',
            (2, 0, 1, 1): '╨',

            (1, 1, 0, 1): '├',
            (2, 2, 0, 2): '╠',
            (1, 1, 0, 2): '╞',
            (2, 2, 0, 1): '╟',

            (1, 1, 1, 0): '┤',
            (2, 2, 2, 0): '╣',
            (1, 1, 2, 0): '╡',
            (2, 2, 1, 0): '╢',

            (1, 0, 1, 0): '┘', (2, 0, 2, 0): '╝', (2, 0, 1, 0): '╜', (1, 0, 2, 0): '╛',
            (1, 0, 0, 1): '└', (2, 0, 0, 2): '╚', (2, 0, 0, 1): '╙', (1, 0, 0, 2): '╘',
            (0, 1, 1, 0): '┐', (0, 2, 2, 0): '╗', (0, 2, 1, 0): '╖', (0, 1, 2, 0): '╕',
            (0, 1, 0, 1): '┌', (0, 2, 0, 2): '╔', (0, 2, 0, 1): '╓', (0, 1, 0, 2): '╒',

            (1, 1, 0, 0): '│', (2, 2, 0, 0): '║',
            (0, 0, 1, 1): '─', (0, 0, 2, 2): '═',

            (1, 0, 0, 0): '╵', (2, 0, 0, 0): '║',
            (0, 1, 0, 0): '╷', (0, 2, 0, 0): '║',
            (0, 0, 1, 0): '╴', (0, 0, 2, 0): '═',
            (0, 0, 0, 1): '╶', (0, 0, 0, 2): '═',
        }

        center_char = center_map.get((up, down, left, right))

        if center_char is None:
            if up and down and left and right:
                center_char = '┼'
            elif up and left and right:
                center_char = '┴'
            elif down and left and right:
                center_char = '┬'
            elif up and down and left:
                center_char = '┤'
            elif up and down and right:
                center_char = '├'
            elif up and down:
                center_char = '│' if up == 1 else '║'  # Approximation verticale
            elif left and right:
                center_char = '─' if left == 1 else '═'  # Approximation horizontale
            else:
                center_char = 'X'

        return f'{left_char}{center_char}{right_char}'

    def bridges_number(self, direction: Direction):
        return self.direction_position_bridges.get(direction, (0, 0))[1]
