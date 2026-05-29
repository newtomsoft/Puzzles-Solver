from ortools.sat.python import cp_model
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
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._region_id = [[self._model.new_int_var(0, len([pos for pos, val in self._numbers_grid if val is not None]) - 1, f"region_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)]
        self._hint_positions = [pos for pos, val in self._numbers_grid if val is not None]
        self._circle_positions = [pos for pos, val in self._circles_grid if val == self.Circle]
        self._regions_count = len(self._hint_positions)
        self._constraints_added = False

    def get_solution(self) -> Grid:
        if not self._constraints_added:
            self._constraints_added = True
            self._add_constraints()
        status = self._solver.Solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            solution_matrix = [[self._solver.Value(self._region_id[r][c]) for c in range(self._cols)] for r in range(self._rows)]
            return RegionsGrid(solution_matrix)
        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if not self._constraints_added:
            self._constraints_added = True
            self._add_constraints()

        status = self._solver.Solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            solution_matrix = [[self._solver.Value(self._region_id[r][c]) for c in range(self._cols)] for r in range(self._rows)]

            diff_vars = []
            for r in range(self._rows):
                for c in range(self._cols):
                    b = self._model.new_bool_var(f"diff_{r}_{c}")
                    self._model.Add(self._region_id[r][c] != solution_matrix[r][c]).OnlyEnforceIf(b)
                    self._model.Add(self._region_id[r][c] == solution_matrix[r][c]).OnlyEnforceIf(b.Not())
                    diff_vars.append(b)
            self._model.AddBoolOr(diff_vars)

            status = self._solver.Solve(self._model)
            if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                new_solution_matrix = [[self._solver.Value(self._region_id[r][c]) for c in range(self._cols)] for r in range(self._rows)]
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
                self._model.Add(self._region_id[r][c] >= 0)
                self._model.Add(self._region_id[r][c] < self._regions_count)

    def _add_hint_location_constraints(self):
        for i, pos in enumerate(self._hint_positions):
            self._model.Add(self._region_id[pos.r][pos.c] == i)

    def _add_rectangular_constraints(self):
        for i in range(self._regions_count):
            min_r = self._model.new_int_var(0, self._rows - 1, f"min_r_{i}")
            max_r = self._model.new_int_var(0, self._rows - 1, f"max_r_{i}")
            min_c = self._model.new_int_var(0, self._cols - 1, f"min_c_{i}")
            max_c = self._model.new_int_var(0, self._cols - 1, f"max_c_{i}")

            self._model.Add(min_r <= max_r)
            self._model.Add(min_c <= max_c)

            for r in range(self._rows):
                for c in range(self._cols):
                    is_in_region = self._model.new_bool_var(f"region_{i}_{r}_{c}")
                    self._model.Add(self._region_id[r][c] == i).OnlyEnforceIf(is_in_region)
                    self._model.Add(self._region_id[r][c] != i).OnlyEnforceIf(is_in_region.Not())

                    self._model.Add(r >= min_r).OnlyEnforceIf(is_in_region)
                    self._model.Add(r <= max_r).OnlyEnforceIf(is_in_region)
                    self._model.Add(c >= min_c).OnlyEnforceIf(is_in_region)
                    self._model.Add(c <= max_c).OnlyEnforceIf(is_in_region)

                    lt_min_r = self._model.new_bool_var(f"lt_min_r_{i}_{r}_{c}")
                    gt_max_r = self._model.new_bool_var(f"gt_max_r_{i}_{r}_{c}")
                    lt_min_c = self._model.new_bool_var(f"lt_min_c_{i}_{r}_{c}")
                    gt_max_c = self._model.new_bool_var(f"gt_max_c_{i}_{r}_{c}")

                    self._model.Add(r < min_r).OnlyEnforceIf(lt_min_r)
                    self._model.Add(r >= min_r).OnlyEnforceIf(lt_min_r.Not())
                    self._model.Add(r > max_r).OnlyEnforceIf(gt_max_r)
                    self._model.Add(r <= max_r).OnlyEnforceIf(gt_max_r.Not())
                    self._model.Add(c < min_c).OnlyEnforceIf(lt_min_c)
                    self._model.Add(c >= min_c).OnlyEnforceIf(lt_min_c.Not())
                    self._model.Add(c > max_c).OnlyEnforceIf(gt_max_c)
                    self._model.Add(c <= max_c).OnlyEnforceIf(gt_max_c.Not())

                    self._model.AddBoolOr([lt_min_r, gt_max_r, lt_min_c, gt_max_c]).OnlyEnforceIf(is_in_region.Not())

    def _add_circle_count_constraints(self):
        for i, pos in enumerate(self._hint_positions):
            hint_val = self._numbers_grid.value(pos)

            circle_bools = []
            for p in self._circle_positions:
                b = self._model.new_bool_var(f"circle_{i}_{p.r}_{p.c}")
                self._model.Add(self._region_id[p.r][p.c] == i).OnlyEnforceIf(b)
                self._model.Add(self._region_id[p.r][p.c] != i).OnlyEnforceIf(b.Not())
                circle_bools.append(b)

            if isinstance(hint_val, int) and hint_val >= 0:
                self._model.Add(sum(circle_bools) == hint_val)
            elif hint_val == self.Unknown:
                self._model.Add(sum(circle_bools) >= 1)

    def _add_adjacent_circle_constraints(self):
        for p in self._circle_positions:
            for neighbor in p.neighbors(mode='orthogonal'):
                if 0 <= neighbor.r < self._rows and 0 <= neighbor.c < self._cols:
                    if self._circles_grid.value(neighbor) == self.Circle:
                        self._model.Add(self._region_id[p.r][p.c] == self._region_id[neighbor.r][neighbor.c])
