import typing

from Domain.Board.Direction import Direction

PipeString = typing.Literal[
    "L0", "L1", "L2", "L3",
    "I0", "I1",
    "T0", "T1", "T2", "T3",
    "E0", "E1", "E2", "E3",
]

PipeShapeString = typing.Literal[
    ' └─', '─┘ ', '─┐ ', ' ┌─',
    ' │ ', '───',
    '─┬─', ' ├─', '─┴─', '─┤ ',
    ' ╶─', ' ╵ ', '─╴ ', ' ╷ ',
]

PIPE_SHAPE_STRING_TO_PIPE_STRING: dict[PipeShapeString, PipeString] = {
    ' └─': "L0", '─┘ ': "L1", '─┐ ': "L2", ' ┌─': "L3",
    ' │ ': "I0", '───': "I1",
    '─┬─': "T0", ' ├─': "T1", '─┴─': "T2", '─┤ ': "T3",
    ' ╶─': "E0", ' ╵ ': "E1", '─╴ ': "E2", ' ╷ ': "E3",
}
PIPE_STRING_TO_PIPE_SHAPE_STRING = {pipe_string: pipe_shape_string for pipe_shape_string, pipe_string in PIPE_SHAPE_STRING_TO_PIPE_STRING.items()}

CONNECTIONS_TO_PIPE_STRING: dict[frozenset[Direction], PipeString] = {
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
    frozenset([Direction.right()]): "E0",
    frozenset([Direction.up()]): "E1",
    frozenset([Direction.left()]): "E2",
    frozenset([Direction.down()]): "E3",
}
PIPE_STRING_TO_CONNECTIONS = {v: k for k, v in CONNECTIONS_TO_PIPE_STRING.items()}


class Pipe:
    def __init__(self, input_string: PipeString):
        self._string = input_string
        self.shape, rotation = input_string
        self.counterclockwise_rotation = int(input_string[1])
        self.clockwise_rotation = (4 - self.counterclockwise_rotation) % 4

    @staticmethod
    def from_connection(directions: frozenset[Direction]):
        return Pipe(CONNECTIONS_TO_PIPE_STRING[directions])

    @staticmethod
    def from_repr(pipe_shape_string: PipeShapeString):
        return Pipe(PIPE_SHAPE_STRING_TO_PIPE_STRING[pipe_shape_string])

    def __str__(self):
        return PIPE_STRING_TO_PIPE_SHAPE_STRING[self.shape + str(self.counterclockwise_rotation)]

    def __repr__(self):
        return str(self)

    def get_connected_to(self) -> frozenset[Direction]:
        return PIPE_STRING_TO_CONNECTIONS[self._string]
