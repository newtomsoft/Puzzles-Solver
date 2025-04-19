from Domain.Board.Grid import Grid
from Domain.Ports.SolverEngine import SolverEngine


class Str8tsSolver:
    def __init__(self, numbers_grid: Grid[int], blacks_grid:Grid[bool], solver_engine: SolverEngine):
        self._numbers_grid = numbers_grid
        self._blacks_grid = blacks_grid
        self.rows_number = self._numbers_grid.rows_number
        self.columns_number = self._numbers_grid.columns_number
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None


    def get_solution(self) -> (Grid, int):
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if not self._solver.has_solution():
            return Grid.empty()
        return Grid([[(self._solver.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_distinct_constraints()
        self._add_adjacent_constraints()

    def _add_initial_constraints(self):
        for position, value in [(position, value) for position, value in self._numbers_grid if value > 0]:
            self._solver.add(self._grid_z3[position] == value)

        for position, is_black in self._blacks_grid:
            if is_black and self._numbers_grid[position] == 0:
                self._solver.add(self._grid_z3[position] == 0)
            else:
                self._solver.add(self._grid_z3[position] > 0)

    def _add_distinct_constraints(self):
        for index, row in enumerate(self._grid_z3.matrix):
            self._solver.add(self._solver.distinct(row))

        for index, column_tuple in enumerate(zip(*self._grid_z3.matrix)):
            column = list(column_tuple)
            self._solver.add(self._solver.distinct(column))

    def _add_adjacent_constraints(self):
        pass
