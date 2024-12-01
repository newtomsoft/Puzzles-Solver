from z3 import Bool, Solver, Not, sat, is_true, Sum, Implies, Or

from Utils.Grid import Grid


class TentsGame:
    def __init__(self, params: (Grid, dict[str, list[int]])):
        self._grid: Grid = params[0]
        self.tents_numbers_by_column_row: dict[str, list[int]] = params[1]
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 6:
            raise ValueError("The grid must be at least 6x6")
        self.columns_tents_numbers = self.tents_numbers_by_column_row['column']
        self.rows_tents_numbers = self.tents_numbers_by_column_row['row']
        self._solver = None
        self._grid_z3 = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._solver = Solver()
        self._add_constraints()
        if self._solver.check() != sat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[is_true(model.eval(self._grid_z3[i, j])) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constraints(self):
        self._add_sum_constraints()
        self.add_no_adjacent_tent_constraint()
        self.add_no_tent_over_tree_constraint()
        self.add_one_tent_for_each_tree_constraint()

    def _add_sum_constraints(self):
        constraints = []
        for i, row in enumerate(self._grid_z3.matrix):
            constraints.append(Sum(row) == self.rows_tents_numbers[i])
        for i, column in enumerate(zip(*self._grid_z3.matrix)):
            constraints.append(Sum(column) == self.columns_tents_numbers[i])
        self._solver.add(constraints)

    def add_no_adjacent_tent_constraint(self):
        for position, value in self._grid_z3:
            r, c = position
            if r > 0:
                self._solver.add(Implies(self._grid_z3[position], Not(self._grid_z3[r - 1, c])))
                if c > 0:
                    self._solver.add(Implies(self._grid_z3[position], Not(self._grid_z3[r, c - 1])))
                    self._solver.add(Implies(self._grid_z3[position], Not(self._grid_z3[r - 1, c - 1])))
                if c < self.columns_number - 1:
                    self._solver.add(Implies(self._grid_z3[position], Not(self._grid_z3[r, c + 1])))
                    self._solver.add(Implies(self._grid_z3[position], Not(self._grid_z3[r - 1, c + 1])))

            if r < self.rows_number - 1:
                self._solver.add(Implies(self._grid_z3[position], Not(self._grid_z3[r + 1, c])))
                if c > 0:
                    self._solver.add(Implies(self._grid_z3[position], Not(self._grid_z3[r, c - 1])))
                    self._solver.add(Implies(self._grid_z3[position], Not(self._grid_z3[r + 1, c - 1])))
                if c < self.columns_number - 1:
                    self._solver.add(Implies(self._grid_z3[position], Not(self._grid_z3[r, c + 1])))
                    self._solver.add(Implies(self._grid_z3[position], Not(self._grid_z3[r + 1, c + 1])))

    def add_no_tent_over_tree_constraint(self):
        for position, value in self._grid:
            if value == -1:
                self._solver.add(Not(self._grid_z3[position]))

    def add_one_tent_for_each_tree_constraint(self):
        for position, value in self._grid:
            if value == -1:
                neighbors_positions = self._grid.neighbors_positions(position)
                if len(neighbors_positions) > 0:
                    self._solver.add(Or([self._grid_z3[position] for position in neighbors_positions]))
