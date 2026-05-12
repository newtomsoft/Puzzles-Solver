from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class HitoriSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self._solver = cp_model.CpSolver()
        self._model = cp_model.CpModel()
        self._grid_vars = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._model = cp_model.CpModel()
        self._grid_vars = Grid([[self._model.new_bool_var(f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        self._init_solver()
        return self._solve_and_ensure_connectivity()

    def get_other_solution(self):
        if self._previous_solution is None:
             return self.get_solution()

        previous_black_cells = [pos for pos, val in self._previous_solution if not val]
        self._model.add_bool_or([self._grid_vars[p] for p in previous_black_cells])

        return self._solve_and_ensure_connectivity()

    def _solve_and_ensure_connectivity(self):
        while True:
            status = self._solver.solve(self._model)
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                 boolean_grid = self._build_boolean_grid_from_solution()
                 white_shapes = boolean_grid.get_all_shapes()
                 if len(white_shapes) == 1:
                      solution_grid = self._build_solution_grid(boolean_grid)
                      self._previous_solution = solution_grid
                      return solution_grid
                 else:
                      self._add_connectivity_constraints(white_shapes)
            else:
                 return Grid.empty()

    def _build_boolean_grid_from_solution(self):
        return Grid([[self._solver.boolean_value(self._grid_vars[r][c]) for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])

    def _build_solution_grid(self, boolean_grid):
        return Grid([[self._grid.value(r, c) if boolean_grid.value(r, c) else False for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])

    def _add_connectivity_constraints(self, white_shapes: set[frozenset[Position]]):

        biggest_white_shapes = max(white_shapes, key=len)
        white_shapes.remove(biggest_white_shapes)
        for white_shape in white_shapes:
            around_white = ShapeGenerator.around_shape(white_shape)
            valid_around = [p for p in around_white if p in self._grid]
            if valid_around:
                 self._model.add_bool_or([self._grid_vars[p] for p in valid_around])

    def _add_constraints(self):
        self._add_no_adjacent_black_cells_constraint()
        self._add_no_duplicate_numbers_in_rows_constraint()
        self._add_no_duplicate_numbers_in_columns_constraint()
        self._add_three_consecutive_identical_constraint()
        self._add_one_between_identical_constraint()

    def _add_no_adjacent_black_cells_constraint(self):
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                if r + 1 < self._grid.rows_number:
                    self._model.add(self._grid_vars[r][c] + self._grid_vars[r + 1][c] >= 1)
                if c + 1 < self._grid.columns_number:
                    self._model.add(self._grid_vars[r][c] + self._grid_vars[r][c + 1] >= 1)

    def _add_no_duplicate_numbers_in_rows_constraint(self):
        for r in range(self._grid.rows_number):
            vals = {}
            for c in range(self._grid.columns_number):
                val = self._grid[r][c]
                if val not in vals:
                    vals[val] = []
                vals[val].append(c)
            for val, cols in vals.items():
                if len(cols) > 1:
                    self._model.add(sum(self._grid_vars[r][c] for c in cols) <= 1)

    def _add_no_duplicate_numbers_in_columns_constraint(self):
        for c in range(self._grid.columns_number):
            vals = {}
            for r in range(self._grid.rows_number):
                val = self._grid[r][c]
                if val not in vals:
                    vals[val] = []
                vals[val].append(r)
            for val, rows in vals.items():
                if len(rows) > 1:
                    self._model.add(sum(self._grid_vars[r][c] for r in rows) <= 1)

    def _add_three_consecutive_identical_constraint(self):
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number - 2):
                if self._grid[r][c] == self._grid[r][c + 1] == self._grid[r][c + 2]:
                    self._model.add(self._grid_vars[r][c + 1] == 1)
                    self._model.add(self._grid_vars[r][c] == 0)
                    self._model.add(self._grid_vars[r][c + 2] == 0)

        for c in range(self._grid.columns_number):
            for r in range(self._grid.rows_number - 2):
                if self._grid[r][c] == self._grid[r + 1][c] == self._grid[r + 2][c]:
                    self._model.add(self._grid_vars[r + 1][c] == 1)
                    self._model.add(self._grid_vars[r][c] == 0)
                    self._model.add(self._grid_vars[r + 2][c] == 0)

    def _add_one_between_identical_constraint(self):
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number - 2):
                if self._grid[r][c] == self._grid[r][c + 2]:
                    self._model.add(self._grid_vars[r][c + 1] == 1)

        for c in range(self._grid.columns_number):
            for r in range(self._grid.rows_number - 2):
                if self._grid[r][c] == self._grid[r + 2][c]:
                    self._model.add(self._grid_vars[r + 1][c] == 1)
