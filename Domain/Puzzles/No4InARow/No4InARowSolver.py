from z3 import Solver, Bool, Not, And, unsat, is_true

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class No4InARowSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 4:
            raise ValueError("No 4 in a Row grid must be at least 4x4")
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Bool(f"matrix_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if self._solver.check() == unsat:
            return Grid.empty()

        model = self._solver.model()
        return Grid([[is_true(model.eval(self._grid_z3[r][c])) for c in range(self.columns_number)] for r in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_not_same_4_adjacent_horizontally_constraints()
        self._add_not_same_4_adjacent_vertically_constraints()
        self._add_not_same_4_adjacent_diagonally_constraints()

    def _add_initial_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == 0:
                    self._solver.add(Not(self._grid_z3[r][c]))
                elif self._grid.value(r, c) == 1:
                    self._solver.add(self._grid_z3[r][c])

    def _add_not_same_4_adjacent_horizontally_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number - 3):
                self._solver.add(Not(And(
                    self._grid_z3[r][c] == self._grid_z3[r][c + 1], self._grid_z3[r][c] == self._grid_z3[r][c + 2], self._grid_z3[r][c] == self._grid_z3[r][c + 3]))
                )

    def _add_not_same_4_adjacent_vertically_constraints(self):
        for c in range(self.columns_number):
            for r in range(self.rows_number - 3):
                self._solver.add(Not(And(
                    self._grid_z3[r][c] == self._grid_z3[r + 1][c], self._grid_z3[r][c] == self._grid_z3[r + 2][c], self._grid_z3[r][c] == self._grid_z3[r + 3][c]))
                )

    def _add_not_same_4_adjacent_diagonally_constraints(self):
        for r in range(self.rows_number - 3):
            for c in range(self.columns_number - 3):
                self._solver.add(Not(And(
                    self._grid_z3[r][c] == self._grid_z3[r + 1][c + 1], self._grid_z3[r][c] == self._grid_z3[r + 2][c + 2], self._grid_z3[r][c] == self._grid_z3[r + 3][c + 3]))
                )
        for r in range(self.rows_number - 3):
            for c in range(3, self.columns_number):
                self._solver.add(Not(And(
                    self._grid_z3[r][c] == self._grid_z3[r + 1][c - 1], self._grid_z3[r][c] == self._grid_z3[r + 2][c - 2], self._grid_z3[r][c] == self._grid_z3[r + 3][c - 3]))
                )
