from z3 import Distinct

from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Grid import Grid


class KakuroSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 3:
            raise ValueError("The grid must be at least 3x3")
        self._solver = solver_engine
        self._grid_z3 = None

    def get_solution(self) -> Grid:
        self._grid_z3 = [[self._solver.int(f"grid_{r}_{c}") if not isinstance(self._grid.value(r, c), list) else None for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()
        if not self._solver.has_solution():
            return Grid.empty()
        grid = Grid([[self._solver.eval(self._grid_z3[r][c]) if self._grid_z3[r][c] is not None else 0 for c in range(self.columns_number)] for r in range(self.rows_number)])
        return grid

    def get_other_solution(self) -> Grid:
        raise NotImplemented("This method is not yet implemented")

    def _add_constraints(self):
        self._add_constraint_numbers_between_1_9()
        self._add_constraint_rows()
        self._add_constraint_columns()

    def _add_constraint_numbers_between_1_9(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid_z3[r][c] is not None:
                    self._solver.add(self._grid_z3[r][c] >= 1)
                    self._solver.add(self._grid_z3[r][c] <= 9)

    def _add_constraint_rows(self):
        constraints = []
        for r in range(1, self.rows_number):
            sums = [self._grid.value(r, c)[0] if self._grid.value(r, c) != 0 and self._grid.value(r, c)[0] != 0 else None for c in range(self.columns_number)]
            if all(current_sum is None for current_sum in sums):
                continue
            c_min = None
            current_sum = None
            for c in range(self.columns_number):
                if current_sum is None and sums[c] is None:
                    continue
                if current_sum is None and sums[c] is not None:
                    c_min = c + 1
                    current_sum = sums[c]
                    continue
                if sums[c] is not None and c_min < c - 1:
                    selected_z3 = [self._grid_z3[r][i] for i in range(c_min, c) if self._grid_z3[r][i] is not None]
                    constraints.append(self._solver.sum(selected_z3) == current_sum)
                    constraints.append(Distinct(selected_z3))
                    current_sum = sums[c]
                    c_min = c + 1
                    continue
                if c == self.columns_number - 1:
                    selected_z3 = [self._grid_z3[r][i] for i in range(c_min, c + 1) if self._grid_z3[r][i] is not None]
                    constraints.append(self._solver.sum(selected_z3) == current_sum)
                    if len(selected_z3) > 1:
                        constraints.append(Distinct(selected_z3))
        self._solver.add(self._solver.And(constraints))

    def _add_constraint_columns(self):
        constraints = []
        for c in range(1, self.columns_number):
            sums = [self._grid.value(r, c)[1] if self._grid.value(r, c) != 0 and self._grid.value(r, c)[1] != 0 else None for r in range(self.rows_number)]
            if all(current_sum is None for current_sum in sums):
                continue
            r_min = None
            current_sum = None
            for r in range(self.rows_number):
                if current_sum is None and sums[r] is None:
                    continue
                if current_sum is None and sums[r] is not None:
                    r_min = r + 1
                    current_sum = sums[r]
                    continue
                if sums[r] is not None and r_min < r - 1:
                    selected_z3 = [self._grid_z3[i][c] for i in range(r_min, r) if self._grid_z3[i][c] is not None]
                    constraints.append(self._solver.sum(selected_z3) == current_sum)
                    if len(selected_z3) > 1:
                        constraints.append(Distinct(selected_z3))
                    current_sum = sums[r]
                    r_min = r + 1
                    continue
                if r == self.rows_number - 1:
                    selected_z3 = [self._grid_z3[i][c] for i in range(r_min, r + 1) if self._grid_z3[i][c] is not None]
                    constraints.append(self._solver.sum(selected_z3) == current_sum)
                    if len(selected_z3) > 1:
                        constraints.append(Distinct(selected_z3))
        self._solver.add(self._solver.And(constraints))
