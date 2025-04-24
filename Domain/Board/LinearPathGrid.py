from Domain.Board.Grid import Grid
from Domain.Board.Path import PathCell
from Domain.Board.Position import Position


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

    def next(self, position):
        value = self[position]
        if value.is_start():
            return position.get_next_position(value)
        return None


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