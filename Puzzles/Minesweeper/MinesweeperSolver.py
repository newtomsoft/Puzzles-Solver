from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Grid import Grid


class MinesweeperSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._solver = solver_engine

    def get_solution(self) -> (Grid | None, int):
        self._grid_z3 = Grid([[self._solver.bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        if not self._solver.has_solution():
            return None
        grid = Grid([[(self._solver.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constraints(self):
        self._add_sum_constraints()

    def _add_sum_constraints(self):
        constraints = []
        for position, cell in [(position, cell) for position, cell in self._grid if cell != -1]:
            constraints.append(self._grid_z3[position])
            constraints.append(self._solver.sum([self._solver.Not(value) for value in self._grid_z3.neighbors_values(position, 'diagonal')]) == cell)
        self._solver.add(self._solver.And(constraints))


