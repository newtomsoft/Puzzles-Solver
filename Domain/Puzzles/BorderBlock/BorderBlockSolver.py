from itertools import combinations

from z3 import Solver, Int, And, Not, unsat, Or, Distinct, ArithRef

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class BorderBlockSolver(GameSolver):
    empty = None

    def __init__(self, grid: Grid, dots: list[Position]):
        self._input_grid = grid
        self.dots = dots
        self._rows_number = self._input_grid.rows_number
        self._columns_number = self._input_grid.columns_number
        self._max_region_id = max(value for position, value in self._input_grid if value is not None)
        self._grid_z3: Grid = Grid.empty()
        self._solver = Solver()
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"region_id_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self):
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._grid_z3[Position(i, j)]).as_long() for j in range(self._columns_number)] for i in range(self._rows_number)])
        return grid

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_dots_constraints()

    def _add_initials_constraints(self):
        for position, value in self._input_grid:
            if value is None:
                self._solver.add(self._grid_z3[position] > 0, self._grid_z3[position] <= self._max_region_id)
            else:
                self._solver.add(self._grid_z3[position] == value)

    def _add_dots_constraints(self):
        for dot in self.dots:
            self._add_dot_constraint(dot)

    def _add_dot_constraint(self, dot: Position):
        neighbors_value = [self._grid_z3[position] for position in dot.straddled_neighbors() if position in self._input_grid]

        if self._add_edge_dot_constraints(neighbors_value):
            return

        self._add_not_edge_dot_constraint(neighbors_value)

    def _add_edge_dot_constraints(self, neighbors_value: list[ArithRef]) -> bool:
        if len(neighbors_value) == 2:
            self._solver.add(neighbors_value[0] != neighbors_value[1])
            return True

        return False

    def _add_not_edge_dot_constraint(self, neighbors_value: list[ArithRef]):
        self._solver.add(Or([Distinct(*trio) for trio in combinations(neighbors_value, 3)]))


