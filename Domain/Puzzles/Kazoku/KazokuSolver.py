from z3 import Solver, Int, And, Or, sat, Distinct, If, Sum
from Domain.Board.Grid import Grid
from Domain.Board.RegionsGrid import RegionsGrid
from Domain.Puzzles.GameSolver import GameSolver


class KazokuSolver(GameSolver):
    Circle = 1
    Unknown = '?'

    def __init__(self, numbers_grid: Grid, circles_grid: Grid):
        self._numbers_grid = numbers_grid
        self._circles_grid = circles_grid
        self._rows = numbers_grid.rows_number
        self._cols = numbers_grid.columns_number
        self._solver = Solver()
        self._region_id = [[Int(f"region_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)]
        self._hint_positions = [pos for pos, val in self._numbers_grid if val is not None]
        self._circle_positions = [pos for pos, val in self._circles_grid if val == self.Circle]
        self._regions_count = len(self._hint_positions)

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._add_constraints()
        if self._solver.check() == sat:
            model = self._solver.model()
            solution_matrix = [[model.eval(self._region_id[r][c]).as_long() for c in range(self._cols)] for r in range(self._rows)]
            return RegionsGrid(solution_matrix)
        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if not self._solver.assertions():
            self._add_constraints()
        
        if self._solver.check() == sat:
            model = self._solver.model()
            solution_matrix = [[model.eval(self._region_id[r][c]).as_long() for c in range(self._cols)] for r in range(self._rows)]
            
            diff_constraints = []
            for r in range(self._rows):
                for c in range(self._cols):
                    diff_constraints.append(self._region_id[r][c] != solution_matrix[r][c])
            self._solver.add(Or(diff_constraints))
            
            if self._solver.check() == sat:
                model = self._solver.model()
                new_solution_matrix = [[model.eval(self._region_id[r][c]).as_long() for c in range(self._cols)] for r in range(self._rows)]
                return RegionsGrid(new_solution_matrix)
        return Grid.empty()

    def _add_constraints(self):
        self._add_domain_constraints()
        self._add_hint_location_constraints()
        self._add_rectangular_constraints()
        self._add_circle_count_constraints()
        self._add_adjacent_circle_constraints()

    def _add_domain_constraints(self):
        for r in range(self._rows):
            for c in range(self._cols):
                self._solver.add(self._region_id[r][c] >= 0)
                self._solver.add(self._region_id[r][c] < self._regions_count)

    def _add_hint_location_constraints(self):
        for i, pos in enumerate(self._hint_positions):
            self._solver.add(self._region_id[pos.r][pos.c] == i)

    def _add_rectangular_constraints(self):
        for i in range(self._regions_count):
            min_r = Int(f"min_r_{i}")
            max_r = Int(f"max_r_{i}")
            min_c = Int(f"min_c_{i}")
            max_c = Int(f"max_c_{i}")

            self._solver.add(min_r >= 0, min_r < self._rows)
            self._solver.add(max_r >= 0, max_r < self._rows)
            self._solver.add(min_c >= 0, min_c < self._cols)
            self._solver.add(max_c >= 0, max_c < self._cols)
            self._solver.add(min_r <= max_r)
            self._solver.add(min_c <= max_c)

            for r in range(self._rows):
                for c in range(self._cols):
                    self._solver.add(
                        If(self._region_id[r][c] == i,
                           And(r >= min_r, r <= max_r, c >= min_c, c <= max_c),
                           Or(r < min_r, r > max_r, c < min_c, c > max_c))
                    )

    def _add_circle_count_constraints(self):
        for i, pos in enumerate(self._hint_positions):
            hint_val = self._numbers_grid.value(pos)

            circle_count_in_region = Sum([
                If(self._region_id[p.r][p.c] == i, 1, 0)
                for p in self._circle_positions
            ])

            if isinstance(hint_val, int) and hint_val >= 0:
                self._solver.add(circle_count_in_region == hint_val)
            elif hint_val == self.Unknown:
                self._solver.add(circle_count_in_region >= 1)

    def _add_adjacent_circle_constraints(self):
        for p in self._circle_positions:
            for neighbor in p.neighbors(mode='orthogonal'):
                if 0 <= neighbor.r < self._rows and 0 <= neighbor.c < self._cols:
                    if self._circles_grid.value(neighbor) == self.Circle:
                        self._solver.add(self._region_id[p.r][p.c] == self._region_id[neighbor.r][neighbor.c])
