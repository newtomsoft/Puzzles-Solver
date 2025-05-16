from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class RenzokuSolver(GameSolver):
    def __init__(self, grid: Grid, consecutive_positions: list[tuple[Position, Position]]):
        self._grid: Grid = grid
        self._consecutive_positions: list[tuple[Position, Position]] = consecutive_positions
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars: Grid | None = None
        self._previous_solution_grid: Grid | None = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.NewIntVar(1, self.rows_number, f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.Solve(self._model)
        if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        grid = Grid([[self._solver.Value(self._grid_vars[r][c]) for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._previous_solution_grid = grid
        return grid

    def get_other_solution(self):
        if self._previous_solution_grid is None:
            return self.get_solution()

        different_cells = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                previous_value = self._previous_solution_grid.value(r, c)
                if previous_value != -1:
                    diff_cell = self._model.NewBoolVar(f"diff_cell_{r}_{c}")
                    self._model.Add(self._grid_vars[r][c] != previous_value).OnlyEnforceIf(diff_cell)
                    self._model.Add(self._grid_vars[r][c] == previous_value).OnlyEnforceIf(diff_cell.Not())
                    different_cells.append(diff_cell)

        self._model.AddBoolOr(different_cells)
        return self.get_solution()

    def _number(self, position: Position):
        return self._grid_vars[position]

    def _add_constraints(self):
        self._add_distinct_constraints()
        self._add_initial_constraints()
        self._add_consecutive_constraints()
        self._add_non_consecutive_constraints()

    def _add_distinct_constraints(self):
        for row in self._grid_vars.matrix:
            self._model.AddAllDifferent(row)

        for c in range(self.columns_number):
            column = [self._grid_vars[r][c] for r in range(self.rows_number)]
            self._model.AddAllDifferent(column)

    def _add_initial_constraints(self):
        for position, value in [(position, value) for position, value in self._grid if value != -1]:
            self._model.Add(self._number(position) == value)

    def _add_consecutive_constraints(self):
        for first_position, second_position in self._consecutive_positions:
            consecutive = self._model.NewBoolVar(f"consecutive_{first_position.r}_{first_position.c}_{second_position.r}_{second_position.c}")

            a = self._number(first_position)
            b = self._number(second_position)

            a_minus_b_eq_1 = self._model.NewBoolVar(f"a_minus_b_eq_1_{first_position.r}_{first_position.c}_{second_position.r}_{second_position.c}")
            b_minus_a_eq_1 = self._model.NewBoolVar(f"b_minus_a_eq_1_{first_position.r}_{first_position.c}_{second_position.r}_{second_position.c}")

            self._model.Add(a - b == 1).OnlyEnforceIf(a_minus_b_eq_1)
            self._model.Add(a - b != 1).OnlyEnforceIf(a_minus_b_eq_1.Not())

            self._model.Add(b - a == 1).OnlyEnforceIf(b_minus_a_eq_1)
            self._model.Add(b - a != 1).OnlyEnforceIf(b_minus_a_eq_1.Not())

            self._model.AddBoolOr([a_minus_b_eq_1, b_minus_a_eq_1]).OnlyEnforceIf(consecutive)
            self._model.AddBoolAnd([a_minus_b_eq_1.Not(), b_minus_a_eq_1.Not()]).OnlyEnforceIf(consecutive.Not())

            self._model.Add(consecutive == 1)

    def _add_non_consecutive_constraints(self):
        non_consecutive_positions = (
                [(Position(r, c), Position(r + 1, c)) for r in range(self.rows_number - 1)
                 for c in range(self.columns_number)
                 if (Position(r, c), Position(r + 1, c)) not in self._consecutive_positions]
                + [(Position(r, c), Position(r, c + 1)) for r in range(self.rows_number)
                   for c in range(self.columns_number - 1)
                   if (Position(r, c), Position(r, c + 1)) not in self._consecutive_positions]
        )

        for first_position, second_position in non_consecutive_positions:
            a = self._number(first_position)
            b = self._number(second_position)

            self._model.Add(a - b != 1)
            self._model.Add(b - a != 1)
