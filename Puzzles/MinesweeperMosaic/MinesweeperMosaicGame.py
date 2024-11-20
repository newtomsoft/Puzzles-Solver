from z3 import Bool, Solver, Not, And, sat, is_true, Sum

from Utils.Grid import Grid


class MinesweeperMosaicGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = None
        self._grid_z3 = None

    def get_solution(self) -> (Grid | None, int):
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._solver = Solver()
        self._add_constraints()
        if self._solver.check() != sat:
            return None
        model = self._solver.model()
        grid = Grid([[is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

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
                constraints.append(Sum([Not(cell) for cell in cells_in_cell_zone]) == self._grid.value(r, c))
        self._solver.add(And(constraints))
