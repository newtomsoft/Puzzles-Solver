from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class FutoshikiSolver(GameSolver):
    def __init__(self, grid: Grid, higher_positions: list[tuple[Position, Position]]):
        self._grid = grid
        self._higher_positions = higher_positions
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        self._model = None
        self._grid_vars = None
        self._previous_solution_grid: Grid | None = None
        self._solver = None

    def _init_solver(self):
        self._model = cp_model.CpModel()
        self._grid_vars = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                self._grid_vars[(r, c)] = self._model.NewIntVar(1, self.columns_number, f'grid_{r}_{c}')
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_solver()

        self._solver = cp_model.CpSolver()
        status = self._solver.Solve(self._model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            grid = Grid([[self._solver.Value(self._number(Position(r, c))) for c in range(self.columns_number)] 
                         for r in range(self.rows_number)])
            self._previous_solution_grid = grid
            return grid
        else:
            return Grid.empty()

    def get_other_solution(self):
        if self._previous_solution_grid is None:
            return Grid.empty()

        different_cells = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._previous_solution_grid.value(r, c) != -1:
                    is_different = self._model.NewBoolVar(f'diff_{r}_{c}')
                    self._model.Add(self._number(Position(r, c)) != self._previous_solution_grid.value(r, c)).OnlyEnforceIf(is_different)
                    self._model.Add(self._number(Position(r, c)) == self._previous_solution_grid.value(r, c)).OnlyEnforceIf(is_different.Not())
                    different_cells.append(is_different)

        if different_cells:
            self._model.AddBoolOr(different_cells)

        return self.get_solution()

    def _number(self, position):
        return self._grid_vars[(position.r, position.c)]

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_distinct_constraints()
        self._add_higher_constraints()

    def _add_initial_constraints(self):
        for position, value in [(p, v) for p, v in self._grid if v != -1]:
            self._model.Add(self._number(position) == value)

    def _add_distinct_constraints(self):
        for r in range(self.rows_number):
            row_vars = [self._number(Position(r, c)) for c in range(self.columns_number)]
            self._model.AddAllDifferent(row_vars)

        for c in range(self.columns_number):
            col_vars = [self._number(Position(r, c)) for r in range(self.rows_number)]
            self._model.AddAllDifferent(col_vars)

    def _add_higher_constraints(self):
        for item in self._higher_positions:
            if isinstance(item, tuple):
                first_position, second_position = item
            else:
                first_pos_tuple, second_pos_tuple = item
                first_position = Position(first_pos_tuple[0], first_pos_tuple[1])
                second_position = Position(second_pos_tuple[0], second_pos_tuple[1])

            self._model.Add(self._number(first_position) > self._number(second_position))
