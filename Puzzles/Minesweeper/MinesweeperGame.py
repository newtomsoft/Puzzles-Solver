from z3 import Bool, Solver, Not, And, sat, is_true, Sum

from Utils.Grid import Grid


class MinesweeperGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = None
        self._grid_z3: Grid | None = None

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
        self._add_sum_constraints()

    def _add_sum_constraints(self):
        constraints = []
        for position, cell in [(position, cell) for position, cell in self._grid if cell != -1]:
            constraints.append(self._grid_z3[position])
            constraints.append(Sum([Not(value) for value in self._grid_z3.neighbors_values(position, 'diagonal')]) == cell)
        self._solver.add(And(constraints))

