from z3 import Bool

from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Grid import Grid


class MinesweeperMosaicSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = solver_engine
        self._grid_z3 = None

    def get_solution(self) -> (Grid | None, int):
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        if not self._solver.has_solution():
            return None
        model = self._solver.model()
        grid = Grid([[self._solver.is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def get_other_solution(self) -> Grid:
        raise NotImplemented("This method is not yet implemented")

    def _add_constraints(self):
        constraints = []

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == -1:
                    continue
                cells_in_cell_zone = []
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if 0 <= r + dr < self.rows_number and 0 <= c + dc < self.columns_number:
                            cells_in_cell_zone.append(self._grid_z3.value(r + dr, c + dc))
                constraints.append(self._solver.sum([self._solver.Not(cell) for cell in cells_in_cell_zone]) == self._grid.value(r, c))
        self._solver.add(self._solver.And(constraints))
