from z3 import Solver, Not, And, unsat, Int, Distinct, If

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


class TrilogySolver:
    def __init__(self, grid: Grid[int]):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"grid_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> (Grid, Grid):
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution if value > 0])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        solution = Grid([[(model.eval(self._grid_z3[Position(i, j)])).as_long() for j in range(self._columns_number)] for i in range(self._rows_number)])
        return solution

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_row_constraints()
        self._add_columns_constraints()
        self._add_up_right_diagonals_constraints()
        self._add_up_left_diagonals_constraints()

    def _add_initial_constraints(self):
        for position, value in [(position, value) for position, value in self._grid if value > 0]:
            self._solver.add(self._grid_z3[position] == value)
        for position, value in [(position, value) for position, value in self._grid if value == 0]:
            self._solver.add(self._grid_z3[position] > 0, self._grid_z3[position] < 4)

    def _add_row_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number - 2):
                first_position = Position(r, c)
                second_position = Position(r, c + 1)
                third_position = Position(r, c + 2)
                self._add_not_same_constraint(first_position, second_position, third_position)
                self._add_not_all_different_constraint(first_position, second_position, third_position)

    def _add_columns_constraints(self):
        for r in range(self._rows_number - 2):
            for c in range(self._columns_number):
                first_position = Position(r, c)
                second_position = Position(r + 1, c)
                third_position = Position(r + 2, c)
                self._add_not_same_constraint(first_position, second_position, third_position)
                self._add_not_all_different_constraint(first_position, second_position, third_position)

    def _add_up_right_diagonals_constraints(self):
        for r in range(2, self._rows_number):
            for c in range(self._columns_number - 2):
                first_position = Position(r, c)
                second_position = Position(r - 1, c + 1)
                third_position = Position(r - 2, c + 2)
                self._add_not_same_constraint(first_position, second_position, third_position)
                self._add_not_all_different_constraint(first_position, second_position, third_position)

    def _add_up_left_diagonals_constraints(self):
        for r in range(2, self._rows_number):
            for c in range(2, self._columns_number):
                first_position = Position(r, c)
                second_position = Position(r - 1, c - 1)
                third_position = Position(r - 2, c - 2)
                self._add_not_same_constraint(first_position, second_position, third_position)
                self._add_not_all_different_constraint(first_position, second_position, third_position)

    def _add_not_all_different_constraint(self, first_position, second_position, third_position):
        self._solver.add(Not(And(
            self._grid_z3[first_position] != self._grid_z3[second_position],
            self._grid_z3[first_position] != self._grid_z3[third_position],
            self._grid_z3[second_position] != self._grid_z3[third_position]
        )))

    def _add_not_same_constraint(self, first_position, second_position, third_position):
        self._solver.add(Not(And(
            self._grid_z3[first_position] == self._grid_z3[second_position],
            self._grid_z3[first_position] == self._grid_z3[third_position]
        )))
