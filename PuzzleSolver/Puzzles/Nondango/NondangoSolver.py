from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class NondangoSolver(GameSolver):
    WHITE = 0
    BLACK = 1

    def __init__(self, regions_grid: Grid, has_circle_mask: Grid):
        super().__init__()
        self._regions_grid = regions_grid
        self._has_circle_mask = has_circle_mask
        self.rows_number = regions_grid.rows_number
        self.columns_number = regions_grid.columns_number
        self._model: cp_model.CpModel | None = None
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None
        self._status = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._grid_vars = Grid([[self._model.new_bool_var(f"grid_{r}_{c}") if self._has_circle_mask.value(r, c) == 1 else None for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()

        self._status = self._solver.solve(self._model)

        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        solution = self._compute_solution()
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return self.get_solution()

        current_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                var = self._grid_vars[r][c]
                if var is None:
                    continue
                if self._solver.boolean_value(var):
                    current_vars.append(var.Not())
                else:
                    current_vars.append(var)
        self._model.add_bool_or(current_vars)

        self._status = self._solver.solve(self._model)

        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        grid = Grid([[1 if self._has_circle_mask.value(r, c) == 1 and self._solver.boolean_value(self._grid_vars[r][c]) else 0 if self._has_circle_mask.value(r, c) == 1 and not self._solver.boolean_value(self._grid_vars[r][c]) else None for c in range(self.columns_number)] for r in range(self.rows_number)])
        return grid

    def _add_constraints(self):
        self._add_one_black_circle_per_region_constraint()
        self._add_no_three_consecutive_same_color_constraint()

    def _add_one_black_circle_per_region_constraint(self):
        regions = self._regions_grid.get_regions()
        for region_positions in regions.values():
            circled_positions = [p for p in region_positions if self._has_circle_mask[p] == 1]
            if not circled_positions:
                continue
            black_circles = [self._grid_vars[p] for p in circled_positions]
            self._model.add(sum(black_circles) == 1)

    def _add_no_three_consecutive_same_color_constraint(self):
        self._add_no_three_consecutive_in_rows()
        self._add_no_three_consecutive_in_columns()
        self._add_no_three_consecutive_in_diagonals()

    def _add_no_three_consecutive_in_rows(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number - 2):
                if not all(self._has_circle_mask.value(r, c + i) == 1 for i in range(3)):
                    continue
                cell1 = self._grid_vars[r][c]
                cell2 = self._grid_vars[r][c + 1]
                cell3 = self._grid_vars[r][c + 2]

                self._model.add_bool_or([cell1.Not(), cell2.Not(), cell3.Not()])
                self._model.add_bool_or([cell1, cell2, cell3])

    def _add_no_three_consecutive_in_columns(self):
        for c in range(self.columns_number):
            for r in range(self.rows_number - 2):
                if not all(self._has_circle_mask.value(r + i, c) == 1 for i in range(3)):
                    continue
                cell1 = self._grid_vars[r][c]
                cell2 = self._grid_vars[r + 1][c]
                cell3 = self._grid_vars[r + 2][c]

                self._model.add_bool_or([cell1.Not(), cell2.Not(), cell3.Not()])
                self._model.add_bool_or([cell1, cell2, cell3])

    def _add_no_three_consecutive_in_diagonals(self):
        for r in range(self.rows_number - 2):
            for c in range(self.columns_number - 2):
                if not all(self._has_circle_mask.value(r + i, c + i) == 1 for i in range(3)):
                    continue
                cell1 = self._grid_vars[r][c]
                cell2 = self._grid_vars[r + 1][c + 1]
                cell3 = self._grid_vars[r + 2][c + 2]

                self._model.add_bool_or([cell1.Not(), cell2.Not(), cell3.Not()])
                self._model.add_bool_or([cell1, cell2, cell3])

        for r in range(self.rows_number - 2):
            for c in range(2, self.columns_number):
                if not all(self._has_circle_mask.value(r + i, c - i) == 1 for i in range(3)):
                    continue
                cell1 = self._grid_vars[r][c]
                cell2 = self._grid_vars[r + 1][c - 1]
                cell3 = self._grid_vars[r + 2][c - 2]

                self._model.add_bool_or([cell1.Not(), cell2.Not(), cell3.Not()])
                self._model.add_bool_or([cell1, cell2, cell3])
