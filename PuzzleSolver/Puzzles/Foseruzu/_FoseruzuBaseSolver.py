from ortools.sat.python import cp_model

from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class _FoseruzuBaseSolver(GameSolver):
    REGION_SIZE = 4

    def __init__(self, grid: Grid, clues: dict[str, list[int]] | None = None):
        self._grid = grid
        self._clues = clues or {}
        self._rows = grid.rows_number
        self._cols = grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._right: dict[tuple[int, int], cp_model.IntVar] = {}
        self._bottom: dict[tuple[int, int], cp_model.IntVar] = {}
        self._region: dict[tuple[int, int], cp_model.IntVar] = {}
        self._previous_solution = None

    def _init_solver(self):
        self._create_variables()
        has_cell_clues = any(v is not None and v != GameSolver.cell_empty and v != GameSolver.cell_empty for _, v in self._grid)
        if has_cell_clues:
            self._add_cell_constraints()
        else:
            self._add_side_clues_constraints()
        self._add_anti_isolation_constraints()
        self._add_region_link_and_size_constraints()
        self._add_total_walls_constraint()

    def _create_variables(self):
        for i in range(self._rows):
            for j in range(self._cols):
                self._right[(i, j)] = self._model.NewBoolVar(f'r_{i}_{j}')
                self._bottom[(i, j)] = self._model.NewBoolVar(f'b_{i}_{j}')
        regions_count = self._rows * self._cols // self.REGION_SIZE
        for i in range(self._rows):
            for j in range(self._cols):
                self._region[(i, j)] = self._model.NewIntVar(0, regions_count - 1, f'region_{i}_{j}')

    def _add_region_link_and_size_constraints(self):
        regions_count = self._rows * self._cols // self.REGION_SIZE
        for i in range(self._rows):
            for j in range(self._cols - 1):
                are_different = self._model.NewBoolVar(f'diff_r_{i}_{j}')
                self._model.Add(self._region[(i, j)] != self._region[(i, j + 1)]).OnlyEnforceIf(are_different)
                self._model.Add(self._region[(i, j)] == self._region[(i, j + 1)]).OnlyEnforceIf(are_different.Not())
                self._model.Add(self._right[(i, j)] == are_different)

        for i in range(self._rows - 1):
            for j in range(self._cols):
                are_different = self._model.NewBoolVar(f'diff_b_{i}_{j}')
                self._model.Add(self._region[(i, j)] != self._region[(i + 1, j)]).OnlyEnforceIf(are_different)
                self._model.Add(self._region[(i, j)] == self._region[(i + 1, j)]).OnlyEnforceIf(are_different.Not())
                self._model.Add(self._bottom[(i, j)] == are_different)

        for k in range(regions_count):
            cell_indicators = []
            for i in range(self._rows):
                for j in range(self._cols):
                    is_in = self._model.NewBoolVar(f'in_{k}_{i}_{j}')
                    self._model.Add(self._region[(i, j)] == k).OnlyEnforceIf(is_in)
                    self._model.Add(self._region[(i, j)] != k).OnlyEnforceIf(is_in.Not())
                    cell_indicators.append(is_in)
            self._model.Add(sum(cell_indicators) == self.REGION_SIZE)

    def _add_total_walls_constraint(self):
        cells_number = self._rows * self._cols
        if cells_number % self.REGION_SIZE == 0:
            expected_walls = (self.REGION_SIZE + 1) * cells_number // self.REGION_SIZE - self._rows - self._cols
            effective_right = [self._right[(i, j)] for i in range(self._rows) for j in range(self._cols - 1)]
            effective_bottom = [self._bottom[(i, j)] for i in range(self._rows - 1) for j in range(self._cols)]
            self._model.Add(sum(effective_right) + sum(effective_bottom) == expected_walls)

    def _add_anti_isolation_constraints(self):
        for i in range(self._rows):
            for j in range(self._cols):
                is_top = i == 0
                is_bottom = i == self._rows - 1
                is_left = j == 0
                is_right = j == self._cols - 1
                if is_top and is_left:
                    internal_vars = [self._bottom[(i, j)], self._right[(i, j)]]
                    self._model.Add(sum(internal_vars) <= 1)
                elif is_top and is_right:
                    internal_vars = [self._bottom[(i, j)], self._right[(i, j - 1)]]
                    self._model.Add(sum(internal_vars) <= 1)
                elif is_bottom and is_left:
                    internal_vars = [self._bottom[(i - 1, j)], self._right[(i, j)]]
                    self._model.Add(sum(internal_vars) <= 1)
                elif is_bottom and is_right:
                    internal_vars = [self._bottom[(i - 1, j)], self._right[(i, j - 1)]]
                    self._model.Add(sum(internal_vars) <= 1)
                elif is_top:
                    internal_vars = [self._bottom[(i, j)], self._right[(i, j - 1)], self._right[(i, j)]]
                    self._model.Add(sum(internal_vars) <= 2)
                elif is_bottom:
                    internal_vars = [self._bottom[(i - 1, j)], self._right[(i, j - 1)], self._right[(i, j)]]
                    self._model.Add(sum(internal_vars) <= 2)
                elif is_left:
                    internal_vars = [self._bottom[(i - 1, j)], self._bottom[(i, j)], self._right[(i, j)]]
                    self._model.Add(sum(internal_vars) <= 2)
                elif is_right:
                    internal_vars = [self._bottom[(i - 1, j)], self._bottom[(i, j)], self._right[(i, j - 1)]]
                    self._model.Add(sum(internal_vars) <= 2)
                else:
                    internal_vars = [self._bottom[(i - 1, j)], self._bottom[(i, j)], self._right[(i, j - 1)], self._right[(i, j)]]
                    self._model.Add(sum(internal_vars) <= 3)

    def _add_side_clues_constraints(self):
        left = self._clues.get('left', [None] * self._rows)
        top = self._clues.get('top', [None] * self._cols)
        right = self._clues.get('right', [None] * self._rows)
        bottom = self._clues.get('bottom', [None] * self._cols)

        for i in range(self._rows):
            if left[i] is not None and left[i] != GameSolver.cell_empty:
                self._model.Add(sum(self._right[(i, j)] for j in range(self._cols)) == left[i])

        for j in range(self._cols):
            if top[j] is not None and top[j] != GameSolver.cell_empty:
                self._model.Add(sum(self._bottom[(i, j)] for i in range(self._rows)) == top[j])

        for i in range(self._rows):
            if right[i] is not None and right[i] != GameSolver.cell_empty:
                self._model.Add(sum(self._bottom[(i, j)] for j in range(self._cols)) == right[i])

        for j in range(self._cols):
            if bottom[j] is not None and bottom[j] != GameSolver.cell_empty:
                self._model.Add(sum(self._right[(i, j)] for i in range(self._rows)) == bottom[j])

    def _add_cell_constraints(self):
        for position, value in self._grid:
            i, j = position.r, position.c
            if value == GameSolver.cell_empty:
                continue
            if value == 0:
                if 0 < i < self._rows - 1 and 0 < j < self._cols - 1:
                    boundary_vars = [
                        self._bottom[(i - 1, j)],
                        self._bottom[(i, j)],
                        self._right[(i, j - 1)],
                        self._right[(i, j)],
                    ]
                    self._model.Add(sum(boundary_vars) <= 3)
                continue
            boundary_vars = []
            top_edge = self._model.NewBoolVar(f'ce_top_{i}_{j}')
            if i == 0:
                self._model.Add(top_edge == 1)
            else:
                self._model.Add(top_edge == self._bottom[(i - 1, j)])
            boundary_vars.append(top_edge)

            bottom_edge = self._model.NewBoolVar(f'ce_bottom_{i}_{j}')
            if i == self._rows - 1:
                self._model.Add(bottom_edge == 1)
            else:
                self._model.Add(bottom_edge == self._bottom[(i, j)])
            boundary_vars.append(bottom_edge)

            left_edge = self._model.NewBoolVar(f'ce_left_{i}_{j}')
            if j == 0:
                self._model.Add(left_edge == 1)
            else:
                self._model.Add(left_edge == self._right[(i, j - 1)])
            boundary_vars.append(left_edge)

            right_edge = self._model.NewBoolVar(f'ce_right_{i}_{j}')
            if j == self._cols - 1:
                self._model.Add(right_edge == 1)
            else:
                self._model.Add(right_edge == self._right[(i, j)])
            boundary_vars.append(right_edge)

            self._model.Add(sum(boundary_vars) == value)

    def get_solution(self) -> RegionsGrid:
        if not hasattr(self, '_solver_initialized') or not self._solver_initialized:
            self._init_solver()
            self._solver_initialized = True

        while True:
            status = self._solver.Solve(self._model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return RegionsGrid.empty()

            r_vals = {(i, j): self._solver.Value(self._right[(i, j)]) for i in range(self._rows) for j in range(self._cols)}
            b_vals = {(i, j): self._solver.Value(self._bottom[(i, j)]) for i in range(self._rows) for j in range(self._cols)}

            if self._is_valid_partition(r_vals, b_vals):
                solution = self._build_region_grid(r_vals, b_vals)
                self._previous_solution = (r_vals, b_vals, solution)
                return solution

            self._add_blocking_constraint(r_vals, b_vals)

    def _build_region_grid(self, r: dict, b: dict) -> RegionsGrid:
        region_matrix = [[-1 for _ in range(self._cols)] for _ in range(self._rows)]
        region_id = 0
        for i in range(self._rows):
            for j in range(self._cols):
                if region_matrix[i][j] != -1:
                    continue
                stack = [(i, j)]
                while stack:
                    ci, cj = stack.pop()
                    if region_matrix[ci][cj] != -1:
                        continue
                    region_matrix[ci][cj] = region_id
                    if cj + 1 < self._cols and r[(ci, cj)] == 0 and region_matrix[ci][cj + 1] == -1:
                        stack.append((ci, cj + 1))
                    if cj - 1 >= 0 and r[(ci, cj - 1)] == 0 and region_matrix[ci][cj - 1] == -1:
                        stack.append((ci, cj - 1))
                    if ci + 1 < self._rows and b[(ci, cj)] == 0 and region_matrix[ci + 1][cj] == -1:
                        stack.append((ci + 1, cj))
                    if ci - 1 >= 0 and b[(ci - 1, cj)] == 0 and region_matrix[ci - 1][cj] == -1:
                        stack.append((ci - 1, cj))
                region_id += 1
        return RegionsGrid(region_matrix)

    def _is_valid_partition(self, r: dict, b: dict) -> bool:
        visited = set()
        for i in range(self._rows):
            for j in range(self._cols):
                if (i, j) in visited:
                    continue
                stack = [(i, j)]
                component = []
                while stack:
                    ci, cj = stack.pop()
                    if (ci, cj) in visited:
                        continue
                    visited.add((ci, cj))
                    component.append((ci, cj))
                    if cj + 1 < self._cols and r[(ci, cj)] == 0 and (ci, cj + 1) not in visited:
                        stack.append((ci, cj + 1))
                    if cj - 1 >= 0 and r[(ci, cj - 1)] == 0 and (ci, cj - 1) not in visited:
                        stack.append((ci, cj - 1))
                    if ci + 1 < self._rows and b[(ci, cj)] == 0 and (ci + 1, cj) not in visited:
                        stack.append((ci + 1, cj))
                    if ci - 1 >= 0 and b[(ci - 1, cj)] == 0 and (ci - 1, cj) not in visited:
                        stack.append((ci - 1, cj))
                if len(component) != self.REGION_SIZE:
                    return False
        return True

    def _add_blocking_constraint(self, r: dict, b: dict):
        literals = []
        for (i, j), val in r.items():
            if j == self._cols - 1:
                continue
            literals.append(self._right[(i, j)] if val == 0 else self._right[(i, j)].Not())
        for (i, j), val in b.items():
            if i == self._rows - 1:
                continue
            literals.append(self._bottom[(i, j)] if val == 0 else self._bottom[(i, j)].Not())
        self._model.AddBoolOr(literals)

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return Grid.empty()
        r_vals, b_vals, _ = self._previous_solution
        self._add_blocking_constraint(r_vals, b_vals)
        return self.get_solution()
