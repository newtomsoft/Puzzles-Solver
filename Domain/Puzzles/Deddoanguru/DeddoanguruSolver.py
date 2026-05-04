from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Board.RegionsGrid import RegionsGrid
from Domain.Puzzles.GameSolver import GameSolver


class DeddoanguruSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._region_vars = None
        self._previous_solution: RegionsGrid | None = None

        self._eyes = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = grid[r, c]
                if val != -1:
                    self._eyes.append((r, c, val))

        if not self._eyes:
            raise ValueError("No eye found in the grid")
        self._region_count = len(self._eyes)

    def get_solution(self) -> RegionsGrid:
        self._init_model()
        return self._solve()

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._region_vars = [[self._model.new_int_var(0, self._region_count - 1, "") for _ in range(self._columns_number)] for _ in range(self._rows_number)]
        self._add_constraints()

    def _add_constraints(self):
        self._add_one_eye_per_region()
        self._add_region_visibility_constraints()
        self._add_connectivity_constraints()

    def _add_one_eye_per_region(self):
        for i, (eye_r, eye_c, _) in enumerate(self._eyes):
            self._model.add(self._region_vars[eye_r][eye_c] == i)
            for j, (other_r, other_c, _) in enumerate(self._eyes):
                if j != i:
                    self._model.add(self._region_vars[other_r][other_c] != i)

    def _add_region_visibility_constraints(self):
        for i, (eye_r, eye_c, n) in enumerate(self._eyes):
            region_cells = {}
            for r in range(self._rows_number):
                for c in range(self._columns_number):
                    is_same = self._model.new_bool_var("")
                    self._model.add(self._region_vars[r][c] == i).only_enforce_if(is_same)
                    self._model.add(self._region_vars[r][c] != i).only_enforce_if(is_same.negated())
                    region_cells[(r, c)] = is_same

            t = self._model.new_int_var(1, self._rows_number * self._columns_number, "")
            self._model.add(t == cp_model.LinearExpr.sum(list(region_cells.values())))
            v = self._model.new_int_var(0, self._rows_number + self._columns_number - 2, "")
            self._add_visibility_count(eye_r, eye_c, region_cells, v)
            self._model.add(t == n + v + 1)

    def _add_visibility_count(self, eye_r, eye_c, region_cells, v_var):
        visible_vars = []
        for direction in Direction.orthogonal_directions():
            positions = self._grid.all_positions_in_direction(Position(eye_r, eye_c), direction)
            prev_visible = None
            for pos in positions:
                r, c = pos.r, pos.c
                is_visible = self._model.new_bool_var("")
                same_region = region_cells[(r, c)]
                if prev_visible is None:
                    self._model.add(is_visible == same_region)
                else:
                    self._model.add_min_equality(is_visible, [prev_visible, same_region])
                visible_vars.append(is_visible)
                prev_visible = is_visible
        self._model.add(sum(visible_vars) == v_var)

    def _add_connectivity_constraints(self):
        max_dist = self._rows_number + self._columns_number
        order = [[self._model.new_int_var(0, max_dist, "")
                  for c in range(self._columns_number)]
                 for r in range(self._rows_number)]

        eye_cells = {(er, ec) for er, ec, _ in self._eyes}
        for er, ec, _ in self._eyes:
            self._model.add(order[er][ec] == 0)

        same_region_edge = {}
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self._rows_number and 0 <= nc < self._columns_number:
                        b = self._model.new_bool_var("")
                        self._model.add(self._region_vars[r][c] == self._region_vars[nr][nc]).only_enforce_if(b)
                        self._model.add(self._region_vars[r][c] != self._region_vars[nr][nc]).only_enforce_if(b.negated())
                        same_region_edge[(r, c, nr, nc)] = b
                        same_region_edge[(nr, nc, r, c)] = b

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                if (r, c) in eye_cells:
                    continue
                in_same_region_as_neighbor_and_smaller = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < self._rows_number and 0 <= nc < self._columns_number):
                        continue
                    same = same_region_edge[(r, c, nr, nc)]
                    smaller = self._model.new_bool_var("")
                    self._model.add(order[nr][nc] < order[r][c]).only_enforce_if(smaller)
                    self._model.add(order[nr][nc] >= order[r][c]).only_enforce_if(smaller.negated())
                    combined = self._model.new_bool_var("")
                    self._model.add_bool_and([same, smaller]).only_enforce_if(combined)
                    self._model.add_bool_or([same.negated(), smaller.negated()]).only_enforce_if(combined.negated())
                    in_same_region_as_neighbor_and_smaller.append(combined)
                self._model.add_bool_or(in_same_region_as_neighbor_and_smaller)

    @staticmethod
    def _to_regions_grid(region_matrix: list[list[int]]) -> RegionsGrid:
        return RegionsGrid([row[:] for row in region_matrix])

    def _solve(self) -> RegionsGrid:
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 8
        solver.parameters.linearization_level = 2
        status = solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return RegionsGrid.empty()
        region_matrix = [
            [int(solver.value(self._region_vars[r][c])) for c in range(self._columns_number)]
            for r in range(self._rows_number)
        ]
        solution = self._to_regions_grid(region_matrix)
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> RegionsGrid:
        if self._previous_solution is None:
            return self.get_solution()
        if self._previous_solution.is_empty():
            return RegionsGrid.empty()

        diff_vars = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                prev_region = self._previous_solution[r, c]
                diff = self._model.new_bool_var(f"diff_{r}_{c}")
                self._model.add(self._region_vars[r][c] != prev_region).only_enforce_if(diff)
                self._model.add(self._region_vars[r][c] == prev_region).only_enforce_if(diff.negated())
                diff_vars.append(diff)

        self._model.add_bool_or(diff_vars)
        return self._solve()
