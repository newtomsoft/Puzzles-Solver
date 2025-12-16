import typing

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
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


class LinearPathGrid(Grid[PathCell]):
    def __init__(self, matrix: list[list[PathCell]]):
        super().__init__(matrix)
        self.path: list[Position] | None = None

    def __repr__(self) -> str:
        if self.is_empty():
            return 'Grid.empty()'
        return '\n'.join(''.join(str(cell) if cell is not None else ' · ' for cell in row) for row in self._matrix)

    @staticmethod
    def from_grid_and_checkpoints(grid: Grid[int], checkpoints: dict[int, Position]) -> ('LinearPathGrid', list[Position]):
        path = LinearPathGrid._compute_path(grid, checkpoints)
        if not path:
            return Grid.empty()
        grid = LinearPath(path).get_grid()
        grid._set_path(path)
        return grid

    def _set_path(self, path: list[Position]):
        self.path = path

    @staticmethod
    def _compute_path(grid: Grid, checkpoints: dict[int, Position]) -> list[Position]:
        path = []
        for checkpoint_value, checkpoint_position in sorted(checkpoints.items(), key=lambda item: item[0]):
            grid_positions_with_checkpoint_value = set([position for position, value in grid if value == checkpoint_value])
            if not grid_positions_with_checkpoint_value:
                continue
            next_checkpoint_position = checkpoints.get(checkpoint_value + 1)
            checkpoint_path = LinearPathGrid._find_checkpoint_path(grid, checkpoint_position, grid_positions_with_checkpoint_value, next_checkpoint_position)
            if not checkpoint_path:
                return []
            path.extend(checkpoint_path)
        return path

    @staticmethod
    def _find_checkpoint_path(grid: Grid, start_position: Position, positions: set[Position], end_position: Position, current_path=None):
        if current_path is None:
            current_path = [start_position]
        if len(current_path) == len(positions) and (end_position is None or start_position in grid.neighbors_positions(end_position)):
            return current_path
        for next_position in grid.neighbors_positions(start_position):
            if next_position in positions and next_position not in current_path:
                new_path = current_path.copy()
                new_path.append(next_position)
                result = LinearPathGrid._find_checkpoint_path(grid, next_position, positions, end_position, new_path)
                if result is not None:
                    return result
        return None

    @staticmethod
    def has_multy_path(grid: Grid, start_position: Position, end_position: Position) -> bool:
        grid_positions_with_start_value = set([position for position, value in grid if value == grid[start_position]])
        count_found = LinearPathGrid._has_multy_path(grid, start_position, grid_positions_with_start_value, end_position)
        return count_found > 1

    @staticmethod
    def _has_multy_path(grid: Grid, start_position: Position, positions: set[Position], end_position: Position, current_path=None, found_count=0):
        if current_path is None:
            current_path = [start_position]
        if len(current_path) == len(positions) and start_position in grid.neighbors_positions(end_position):
            found_count += 1
            return found_count
        for next_position in grid.neighbors_positions(start_position):
            if next_position in positions and next_position not in current_path:
                new_path = current_path.copy()
                new_path.append(next_position)
                found_count = LinearPathGrid._has_multy_path(grid, next_position, positions, end_position, new_path, found_count)
                if found_count > 1:
                    return found_count
        return found_count

    def next(self, position):
        value = self[position]
        if value.is_start():
            return position.get_next_position(value)
        return None

    @staticmethod
    def empty() -> 'LinearPathGrid':
        return LinearPathGrid([[]])


class LinearPath:
    def __init__(self, path: list[Position]):
        self.path = path
        max_row = max(path, key=lambda pos: pos.r).r
        max_col = max(path, key=lambda pos: pos.c).c
        self.rows_number = max_row + 1
        self.columns_number = max_col + 1

        first_direction = path[0].direction_to(path[1])
        linear_path_cells = [PathCell.from_connections(frozenset([first_direction]))]
        previous_direction = first_direction.opposite
        for index, position in enumerate(path[1:-1]):
            current_direction = position.direction_to(path[index + 2])
            linear_path_cell = PathCell.from_connections(frozenset([previous_direction, current_direction]))
            linear_path_cells.append(linear_path_cell)
            previous_direction = current_direction.opposite
        linear_path_cell = PathCell.end_from_connection(previous_direction.opposite)
        linear_path_cells.append(linear_path_cell)

        linear_path_matrix: list[list[PathCell | None]] = [[None for _ in range(self.columns_number)] for _ in range(self.rows_number)]
        for index, position in enumerate(path):
            linear_path_matrix[position.r][position.c] = linear_path_cells[index]

        linear_path_grid = LinearPathGrid(linear_path_matrix)
        self._grid = linear_path_grid

    def get_grid(self) -> LinearPathGrid:
        return self._grid
