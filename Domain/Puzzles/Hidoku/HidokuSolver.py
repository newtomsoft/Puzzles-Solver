from z3 import Solver, sat, Not, Int, And, Distinct, Or, unsat

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class HidokuSolver(GameSolver):
    empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._solver = Solver()
        self._grid_var = Grid.empty()
        self._previous_solution = Grid.empty()
        self.position_value_min = next((p for p, v in self._grid if v == 1), None)
        self.position_value_max = next((p for p, v in self._grid if v == self._rows_number * self._columns_number), None)

    def get_solution(self) -> Grid:
        self._grid_var = Grid(
            [[Int(f"grid_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)]
        )
        self._add_constraints()
        if not self._solver.check() == sat:
            return Grid.empty()

        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        if self._previous_solution.is_empty():
            return Grid.empty()

        constraint = Not(And([self._grid_var[position] == number for position, number in self._previous_solution]))
        self._solver.add(constraint)
        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        if self._solver.check() == unsat:
            return Grid.empty()

        model = self._solver.model()

        self._previous_solution = Grid(
            [
                [model.eval(self._grid_var[Position(r, c)]).as_long() for c in range(self._columns_number)]
                for r in range(self._rows_number)
            ]
        )
        return self._previous_solution

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_distinct_number_constraints()
        self._add_neighbors_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid:
            if value == self.empty:
                self._solver.add(self._grid_var[position] > 1, self._grid_var[position] < self._rows_number * self._columns_number)
            else:
                self._solver.add(self._grid_var[position] == value)

    def _add_distinct_number_constraints(self):
        self._solver.add(Distinct(self._grid_var.values))

    def _add_neighbors_constraints(self):
        for position, value in self._grid_var:
            neighbors_values = self._grid_var.neighbors_values(position, "diagonal")
            if position != self.position_value_min:
                add = [value == neighbor_value + 1 for neighbor_value in neighbors_values]
                self._solver.add(Or(add))
            if position != self.position_value_max:
                less = [value == neighbor_value - 1 for neighbor_value in neighbors_values]
                self._solver.add(Or(less))
