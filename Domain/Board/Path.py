import typing

from Domain.Board.Direction import Direction

StartPathCellString = typing.Literal["S0", "S1", "S2", "S3",]
EndPathCellString = typing.Literal["E0", "E1", "E2", "E3",]
LPathCellString = typing.Literal["L0", "L1", "L2", "L3",]
IPathCellString = typing.Literal["I0", "I1",]
TPathCellString = typing.Literal["T0", "T1", "T2", "T3",]
PathCellString = StartPathCellString | EndPathCellString | LPathCellString | IPathCellString | TPathCellString

PathCellShapeString = typing.Literal[
    ' └─', '─┘ ', '─┐ ', ' ┌─',
    ' │ ', '───',
    '─┬─', ' ├─', '─┴─', '─┤ ',
    '→  ', ' ↑ ', '  ←', ' ↓ ',
    ' ╶─', ' ╵ ', '─╴ ', ' ╷ '
]

PATH_CELL_SHAPE_STRING_TO_PATH_CELL_STRING: dict[PathCellShapeString, PathCellString] = {
    ' └─': "L0", '─┘ ': "L1", '─┐ ': "L2", ' ┌─': "L3",
    ' │ ': "I0", '───': "I1",
    '─┬─': "T0", ' ├─': "T1", '─┴─': "T2", '─┤ ': "T3",
    '→  ': "E0", ' ↑ ': "E1", '  ←': "E2", ' ↓ ': "E3",
    ' ╶─': "S0", ' ╵ ': "S1", '─╴ ': "S2", ' ╷ ': "S3",
}
PATH_CELL_STRING_TO_PATH_CELL_SHAPE_STRING = {p_string: p_shape_string for p_shape_string, p_string in PATH_CELL_SHAPE_STRING_TO_PATH_CELL_STRING.items()}

CONNECTIONS_TO_PATH_CELL_STRING: dict[frozenset[Direction], PathCellString] = {
    frozenset([Direction.up(), Direction.right()]): "L0",
    frozenset([Direction.up(), Direction.left()]): "L1",
    frozenset([Direction.down(), Direction.left()]): "L2",
    frozenset([Direction.down(), Direction.right()]): "L3",
    frozenset([Direction.up(), Direction.down()]): "I0",
    frozenset([Direction.left(), Direction.right()]): "I1",
    frozenset([Direction.down(), Direction.left(), Direction.right()]): "T0",
    frozenset([Direction.up(), Direction.down(), Direction.right()]): "T1",
    frozenset([Direction.up(), Direction.right(), Direction.left()]): "T2",
    frozenset([Direction.up(), Direction.left(), Direction.down()]): "T3",
    frozenset([Direction.right()]): "S0",
    frozenset([Direction.up()]): "S1",
    frozenset([Direction.left()]): "S2",
    frozenset([Direction.down()]): "S3",
}
PATH_STRING_TO_CONNECTIONS = {v: k for k, v in CONNECTIONS_TO_PATH_CELL_STRING.items()}

CONNECTION_TO_END_PATH_CELL_STRING: dict[Direction, PathCellString] = {
    Direction.right(): "E0",
    Direction.up(): "E1",
    Direction.left(): "E2",
    Direction.down(): "E3",
}


class PathCell:
    def __init__(self, input_string: PathCellString):
        self._string = input_string
        self.shape, rotation = input_string
        self.counterclockwise_rotation = int(input_string[1])
        self.clockwise_rotation = (4 - self.counterclockwise_rotation) % 4

    @staticmethod
    def from_connections(directions: frozenset[Direction]) -> 'PathCell':
        if Direction.none() in directions:
            raise ValueError(f"Invalid direction set: {directions}")
        return PathCell(CONNECTIONS_TO_PATH_CELL_STRING[directions])

    @staticmethod
    def end_from_connection(direction: Direction) -> 'PathCell':
        return PathCell(CONNECTION_TO_END_PATH_CELL_STRING[direction])

    @staticmethod
    def from_repr(pipe_shape_cell_string: PathCellShapeString) -> 'PathCell':
        return PathCell(PATH_CELL_SHAPE_STRING_TO_PATH_CELL_STRING[pipe_shape_cell_string])

    def __str__(self) -> str:
        return PATH_CELL_STRING_TO_PATH_CELL_SHAPE_STRING[self.shape + str(self.counterclockwise_rotation)]

    def __repr__(self) -> str:
        return str(self)

    def get_connected_to(self) -> frozenset[Direction]:
        return PATH_STRING_TO_CONNECTIONS[self._string]

    def is_start(self) -> bool:
        return True if self._string in StartPathCellString else False

    def is_end(self) -> bool:
        return True if self._string in EndPathCellString else False

