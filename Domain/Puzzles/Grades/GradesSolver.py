from z3 import Solver, Not, And, unsat, Int, If, Implies

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class GradesGameSolver(GameSolver):
    no_value = None

    def __init__(self, grid: Grid, clues: dict[str, list[int]]):
        self._grid = grid
        self._clues: dict[str, list[int]] = clues
        self.rows_number = len(clues['left'])
        self.columns_number = len(clues['up'])
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution_grid = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._grid_z3[Position(r, c)]).as_long() for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._previous_solution_grid = grid
        return grid

    def get_other_solution(self):
        exclusion_constraint = Not(And([self._grid_z3[Position(r, c)] == self._previous_solution_grid[Position(r, c)] for r in range(self.rows_number) for c in
                                        range(self.columns_number) if self._previous_solution_grid.value(r, c)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraint()
        self._add_counts_clues_constraint()
        self._add_sums_clues_constraint()
        self._add_no_neighbors_constraints()

    def _add_initial_constraint(self):
        for position, value in self._grid:
            if value == self.no_value:
                self._solver.add(self._grid_z3[position] >= 0)
            else:
                self._solver.add(self._grid_z3[position] == value)

    def _add_counts_clues_constraint(self):
        for row, count in enumerate(self._clues['left']):
            if count != self.no_value:
                self._solver.add(sum([If(self._grid_z3[row, col] != 0, 1, 0) for col in range(self.columns_number)]) == count)

        for col, count in enumerate(self._clues['up']):
            if count != self.no_value:
                self._solver.add(sum([If(self._grid_z3[row, col] != 0, 1, 0) for row in range(self.rows_number)]) == count)

    def _add_sums_clues_constraint(self):
        for row, sum_value in enumerate(self._clues['right']):
            if sum_value != self.no_value:
                self._solver.add(sum([self._grid_z3[row, col] for col in range(self.columns_number)]) == sum_value)

        for col, sum_value in enumerate(self._clues['down']):
            if sum_value != self.no_value:
                self._solver.add(sum([self._grid_z3[row, col] for row in range(self.rows_number)]) == sum_value)

    def _add_no_neighbors_constraints(self):
        for position, value in self._grid_z3:
            self._solver.add(Implies(value != 0, And(neighbors_value == 0 for neighbors_value in self._grid_z3.neighbors_values(position, 'diagonal'))))
