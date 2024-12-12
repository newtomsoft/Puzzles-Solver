from z3 import Solver, sat, Int, And, Not, Distinct

from Utils.Position import Position
from Utils.Grid import Grid


class FutoshikiGame:
    def __init__(self, params: (Grid, list[tuple[Position, Position]])):
        self._grid: Grid = params[0]
        self._higher_positions: list[tuple[Position, Position]] = params[1]
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        self._solver: Solver | None = None
        self._grid_z3: Grid | None = None
        self._last_solution_grid: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._solver = Solver()
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._solver is None:
            self._init_solver()
        if self._solver.check() != sat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._number(Position(r, c))).as_long() for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._last_solution_grid = grid
        return grid

    def get_other_solution(self):
        exclusion_constraint = Not(And([self._number(Position(r, c)) == self._last_solution_grid[Position(r, c)] for r in range(self.rows_number) for c in range(self.columns_number) if self._last_solution_grid.value(r, c)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _number(self, position):
        return self._grid_z3[position]

    def _add_constraints(self):
        self.add_range_constraints()
        self._add_distinct_constraints()
        self._add_initial_constraints()
        self.add_higher_constraints()

    def add_range_constraints(self):
        for position, value in self._grid_z3:
            self._solver.add(1 <= value, value <= self.rows_number)

    def _add_distinct_constraints(self):
        for index, row in enumerate(self._grid_z3.matrix):
            self._solver.add(Distinct(row))

        for index, column_tuple in enumerate(zip(*self._grid_z3.matrix)):
            column = list(column_tuple)
            self._solver.add(Distinct(column))

    def _add_initial_constraints(self):
        for position, value in self._grid:
            if value != -1:
                self._solver.add(self._number(position) == value)

    def add_higher_constraints(self):
        for first_position, second_position in self._higher_positions:
            self._solver.add(self._number(first_position) > self._number(second_position))
