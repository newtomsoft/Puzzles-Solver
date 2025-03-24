from Domain.Grid.Grid import Grid
from Domain.Ports.SolverEngine import SolverEngine
from GameSolver import GameSolver


class MinesweeperSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> (Grid, int):
        self._grid_z3 = Grid([[self._solver.bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
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
        self._add_sum_constraints()

    def _add_sum_constraints(self):
        constraints = []
        for position, cell in [(position, cell) for position, cell in self._grid if cell != -1]:
            constraints.append(self._grid_z3[position])
            constraints.append(self._solver.sum([self._solver.Not(value) for value in self._grid_z3.neighbors_values(position, 'diagonal')]) == cell)
        self._solver.add(self._solver.And(constraints))
