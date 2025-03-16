from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Grid import Grid


class SumpleteSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number - 1
        self.columns_number = self._grid.columns_number - 1
        if self.rows_number != self.columns_number:
            raise ValueError("Sumplete grid must be square")
        if self.rows_number < 2:
            raise ValueError("Sumplete grid (without sums) must be at least 2x2")
        self._row_sums = [self._grid.value(-1, r) for r in range(self.columns_number)]
        self._column_sums = [self._grid.value(r, -1) for r in range(self.rows_number)]
        self._solver = solver_engine
        self._grid_z3 = None

    def get_solution(self) -> (Grid | None, int):
        self._grid_z3 = Grid([[self._solver.bool(f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()
        if not self._solver.has_solution():
            return None
        model = self._solver.model()
        grid = Grid([[model.eval(self._grid_z3.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def get_other_solution(self) -> Grid:
        raise NotImplemented("This method is not yet implemented")

    def _add_constraints(self):
        self._add_constraint_sums_by_rows()
        self._add_constraint_sums_by_columns()

    def _add_constraint_sums_by_rows(self):
        constraints = []
        for r in range(self.rows_number):
            constraints.append(self._solver.sum([self._grid_z3.value(r, c) * self._grid.value(r, c) for c in range(self.columns_number)]) == self._column_sums[r])
        self._solver.add(constraints)

    def _add_constraint_sums_by_columns(self):
        constraints = []
        for c in range(self.columns_number):
            constraints.append(self._solver.sum([self._grid_z3.value(r, c) * self._grid.value(r, c) for r in range(self.rows_number)]) == self._row_sums[c])
        self._solver.add(constraints)
