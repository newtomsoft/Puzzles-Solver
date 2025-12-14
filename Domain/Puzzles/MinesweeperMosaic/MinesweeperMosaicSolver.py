from z3 import Solver, Bool, Not, And, unsat, is_true

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class MinesweeperMosaicSolver(GameSolver):
    empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = Solver()
        self._grid_z3 = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        self._previous_solution = grid
        return grid

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        from z3 import Or
        current_solution_constraints = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                val = self._previous_solution[r][c]
                if val:
                    current_solution_constraints.append(self._grid_z3.value(r, c) == False)
                else:
                    current_solution_constraints.append(self._grid_z3.value(r, c) == True)
        self._solver.add(Or(*current_solution_constraints))
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        self._previous_solution = grid
        return grid

    def _add_constraints(self):
        constraints = []

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == self.empty:
                    continue
                cells_in_cell_zone = []
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if 0 <= r + dr < self.rows_number and 0 <= c + dc < self.columns_number:
                            cells_in_cell_zone.append(self._grid_z3.value(r + dr, c + dc))
                constraints.append(sum([cell for cell in cells_in_cell_zone]) == self._grid.value(r, c))
        self._solver.add(And(constraints))
