from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class KakuroSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 3:
            raise ValueError("The grid must be at least 3x3")
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = None
        self._status = None

    def get_solution(self) -> Grid:
        self._grid_vars = [[self._model.NewIntVar(1, 9, f"grid_{r}_{c}") if not isinstance(self._grid.value(r, c), list) else None for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()

        self._status = self._solver.Solve(self._model)

        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        solution_grid = self._create_solution_grid()
        return solution_grid

    def get_other_solution(self) -> Grid:
        raise NotImplementedError("This method is not yet implemented")

    def _create_solution_grid(self) -> Grid:
        return Grid([[self._solver.Value(self._grid_vars[r][c]) if self._grid_vars[r][c] is not None else 0 for c in range(self.columns_number)] for r in range(self.rows_number)])

    def _add_constraints(self):
        self._add_rows_constraint()
        self._add_columns_constraint()

    def _add_rows_constraint(self):
        for r in range(1, self.rows_number):
            sums = [self._grid[r][c][0] if self._grid[r][c] != 0 and self._grid[r][c][0] != 0 else None for c in range(self.columns_number)]
            self._add_segment_constraints_to_model(sums, self.columns_number, get_cell=lambda idx: self._grid_vars[r][idx])

    def _add_columns_constraint(self):
        for c in range(1, self.columns_number):
            sums = [self._grid[r][c][1] if self._grid[r][c] != 0 and self._grid[r][c][1] != 0 else None for r in range(self.rows_number)]
            self._add_segment_constraints_to_model(sums, self.rows_number, get_cell=lambda idx: self._grid_vars[idx][c])

    def _add_segment_constraints_to_model(self, sums: list[int], dimension_size: int, get_cell: 'callable'):
        if all(current_sum is None for current_sum in sums):
            return

        segment_start_idx = None
        current_sum = None

        for idx in range(dimension_size):
            if current_sum is None and sums[idx] is None:
                continue

            if current_sum is None and sums[idx] is not None:
                segment_start_idx = idx + 1
                current_sum = sums[idx]
                continue

            if sums[idx] is not None and segment_start_idx < idx - 1:
                self._add_segment_constraint(segment_start_idx, idx, current_sum, get_cell)
                current_sum = sums[idx]
                segment_start_idx = idx + 1
                continue

            if idx == dimension_size - 1:
                self._add_segment_constraint(segment_start_idx, idx + 1, current_sum, get_cell)

    def _add_segment_constraint(self, start_idx: int, end_idx: int, target_sum: int, get_cell: 'callable'):
        segment_cells = [cell for i in range(start_idx, end_idx) if (cell := get_cell(i)) is not None]

        if not segment_cells:
            return

        self._model.Add(sum(segment_cells) == target_sum)

        if len(segment_cells) > 1:
            self._model.AddAllDifferent(segment_cells)
