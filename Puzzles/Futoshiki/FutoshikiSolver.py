from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Grid import Grid
from Utils.Position import Position


class FutoshikiSolver(GameSolver):
    def __init__(self, grid: Grid, higher_positions: list[tuple[Position, Position]], solver_engine: SolverEngine):
        self._grid = grid
        self._higher_positions = higher_positions
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._last_solution_grid: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[self._solver.int(f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.has_constraints():
            self._init_solver()
        if not self._solver.has_solution():
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._number(Position(r, c)))() for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._last_solution_grid = grid
        return grid

    def get_other_solution(self):
        exclusion_constraint = self._solver.Not(self._solver.And([self._number(Position(r, c)) == self._last_solution_grid[Position(r, c)] for r in range(self.rows_number) for c in range(self.columns_number) if self._last_solution_grid.value(r, c)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _number(self, position):
        return self._grid_z3[position]

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_range_constraints()
        self._add_distinct_constraints()
        self._add_higher_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid:
            if value != -1:
                self._solver.add(self._number(position) == value)

    def _add_range_constraints(self):
        for position, value in self._grid_z3:
            self._solver.add(value >= 1)
            self._solver.add(value <= self.columns_number)

    def _add_distinct_constraints(self):
        for index, row in enumerate(self._grid_z3.matrix):
            self._solver.add(self._solver.distinct(row))

        for index, column_tuple in enumerate(zip(*self._grid_z3.matrix)):
            column = list(column_tuple)
            self._solver.add(self._solver.distinct(column))

    def _add_higher_constraints(self):
        for first_position, second_position in self._higher_positions:
            self._solver.add(self._number(first_position) > self._number(second_position))
