from z3 import Bool, Solver, Not, And, sat, is_true, Sum, Implies

from Grid import Grid


class QueensGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        self._regions = self._grid.get_regions()
        if self.rows_number != len(self._regions):
            raise ValueError("The grid must have the same number of regions as rows/column")
        self._solver = None
        self._grid_z3 = None

    def get_solution(self) -> Grid | None:
        self._grid_z3 = [[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._solver = Solver()
        self._add_constrains()
        if self._solver.check() != sat:
            return None
        model = self._solver.model()
        grid = Grid([[is_true(model.eval(self._grid_z3[i][j])) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_constrain_single_queen_by_row()
        self._add_constrain_single_queen_by_column()
        self._add_constrain_single_queen_by_region()
        self._add_constrain_no_adjacent_queen()

    def _add_constrain_single_queen_by_row(self):
        for r in range(self.rows_number):
            self._solver.add(Sum([self._grid_z3[r][c] for c in range(self.columns_number)]) == 1)

    def _add_constrain_single_queen_by_column(self):
        for c in range(self.columns_number):
            self._solver.add(Sum([self._grid_z3[r][c] for r in range(self.rows_number)]) == 1)

    def _add_constrain_single_queen_by_region(self):
        for region in self._regions.values():
            self._solver.add(Sum([self._grid_z3[r][c] for r, c in region]) == 1)

    def _add_constrain_no_adjacent_queen(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if r > 0 and c > 0:
                    self._solver.add(Implies(self._grid_z3[r][c], Not(self._grid_z3[r - 1][c - 1])))
                if r > 0 and c < self.columns_number - 1:
                    self._solver.add(Implies(self._grid_z3[r][c], Not(self._grid_z3[r - 1][c + 1])))
                if r < self.rows_number - 1 and c > 0:
                    self._solver.add(Implies(self._grid_z3[r][c], Not(self._grid_z3[r + 1][c - 1])))
                if r < self.rows_number - 1 and c < self.columns_number - 1:
                    self._solver.add(Implies(self._grid_z3[r][c], Not(self._grid_z3[r + 1][c + 1])))

    def _add_constrain_not_this_solution(self, solution):
        constraints_to_add = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if solution[r][c]:
                    constraints_to_add.append(self._grid_z3[r][c])
                else:
                    constraints_to_add.append(Not(self._grid_z3[r][c]))
        self._solver.add(Not(And(constraints_to_add)))
