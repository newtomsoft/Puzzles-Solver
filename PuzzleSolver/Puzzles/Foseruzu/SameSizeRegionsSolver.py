from ortools.sat.python import cp_model

from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class SameSizeRegionsSolver(GameSolver):
    REGION_SIZE = 0
    ALL_SHAPES = []

    def __init__(self, grid: Grid, clues: dict[str, list[int]] | None = None):
        super().__init__()
        self._grid = grid
        self._clues = clues or {}
        self._rows = grid.rows_number
        self._cols = grid.columns_number

        self._blocked: set[tuple[int, int]] = set()
        self._active: set[tuple[int, int]] = set()
        for i in range(self._rows):
            for j in range(self._cols):
                if grid[(i, j)] == self.__class__.cell_blocked:
                    self._blocked.add((i, j))
                else:
                    self._active.add((i, j))
        self._active_count = len(self._active)

        self._model = cp_model.CpModel()
        self._right: dict[tuple[int, int], cp_model.IntVar] = {}
        self._bottom: dict[tuple[int, int], cp_model.IntVar] = {}
        self._use: list[cp_model.BoolVar] | None = None
        self._placements: list[list[tuple[int, int]]] = []
        self._previous_solution = None

    def _init_solver(self):
        self._create_variables()
        self._add_cell_constraints()
        self._init_fast_path()

    def _init_fast_path(self):
        self._placements = self._generate_placements()
        self._use = [self._model.new_bool_var(f'use_{p}') for p in range(len(self._placements))]
        self._add_cover_constraints()
        self._add_wall_constraints()

    def _generate_placements(self) -> list[list[tuple[int, int]]]:
        placements = []
        for shape in self.ALL_SHAPES:
            max_r = max(dr for dr, _ in shape)
            max_c = max(dc for _, dc in shape)
            for i in range(self._rows - max_r):
                for j in range(self._cols - max_c):
                    cells = [(i + dr, j + dc) for dr, dc in shape]
                    if any(c in self._blocked for c in cells):
                        continue
                    placements.append(cells)
        return placements

    def _create_variables(self):
        for i in range(self._rows):
            for j in range(self._cols):
                self._right[(i, j)] = self._model.new_bool_var(f'r_{i}_{j}')
                self._bottom[(i, j)] = self._model.new_bool_var(f'b_{i}_{j}')

    def _add_cover_constraints(self):
        for i in range(self._rows):
            for j in range(self._cols):
                covering = [self._use[p] for p, cells in enumerate(self._placements) if (i, j) in cells]
                if (i, j) in self._blocked:
                    self._model.add(sum(covering) == 0)
                else:
                    self._model.add(sum(covering) == 1)

    def _add_wall_constraints(self):
        for i in range(self._rows):
            for j in range(self._cols - 1):
                left_blocked = (i, j) in self._blocked
                right_blocked = (i, j + 1) in self._blocked
                if left_blocked or right_blocked:
                    self._model.add(self._right[(i, j)] == 1)
                else:
                    covering_both = [self._use[p] for p, cells in enumerate(self._placements) if (i, j) in cells and (i, j + 1) in cells]
                    self._model.add(self._right[(i, j)] == 1 - sum(covering_both))
        for i in range(self._rows - 1):
            for j in range(self._cols):
                top_blocked = (i, j) in self._blocked
                bottom_blocked = (i + 1, j) in self._blocked
                if top_blocked or bottom_blocked:
                    self._model.add(self._bottom[(i, j)] == 1)
                else:
                    covering_both = [self._use[p] for p, cells in enumerate(self._placements) if (i, j) in cells and (i + 1, j) in cells]
                    self._model.add(self._bottom[(i, j)] == 1 - sum(covering_both))

    def _add_side_clues_constraints(self):
        left = self._clues.get('left', [None] * self._rows)
        top = self._clues.get('top', [None] * self._cols)
        right = self._clues.get('right', [None] * self._rows)
        bottom = self._clues.get('bottom', [None] * self._cols)

        for i in range(self._rows):
            if left[i] is not None and left[i] != GameSolver.cell_empty:
                self._model.add(sum(self._right[(i, j)] for j in range(self._cols)) == left[i])

        for j in range(self._cols):
            if top[j] is not None and top[j] != GameSolver.cell_empty:
                self._model.add(sum(self._bottom[(i, j)] for i in range(self._rows)) == top[j])

        for i in range(self._rows):
            if right[i] is not None and right[i] != GameSolver.cell_empty:
                self._model.add(sum(self._bottom[(i, j)] for j in range(self._cols)) == right[i])

        for j in range(self._cols):
            if bottom[j] is not None and bottom[j] != GameSolver.cell_empty:
                self._model.add(sum(self._right[(i, j)] for i in range(self._rows)) == bottom[j])

    def _add_cell_constraints(self):
        for position, value in self._grid:
            i, j = position.r, position.c
            if value == GameSolver.cell_empty or (i, j) in self._blocked:
                continue

            edge_terms = []

            if i == 0 or (i - 1, j) in self._blocked:
                edge_terms.append(1)
            else:
                edge_terms.append(self._bottom[(i - 1, j)])

            if i == self._rows - 1 or (i + 1, j) in self._blocked:
                edge_terms.append(1)
            else:
                edge_terms.append(self._bottom[(i, j)])

            if j == 0 or (i, j - 1) in self._blocked:
                edge_terms.append(1)
            else:
                edge_terms.append(self._right[(i, j - 1)])

            if j == self._cols - 1 or (i, j + 1) in self._blocked:
                edge_terms.append(1)
            else:
                edge_terms.append(self._right[(i, j)])

            self._model.add(sum(edge_terms) == value)

    def get_solution(self) -> RegionsGrid:
        if not hasattr(self, '_solver_initialized') or not self._solver_initialized:
            self._init_solver()
            self._solver_initialized = True

        status = self._solver.Solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return RegionsGrid.empty()

        r_vals = {(i, j): self._solver.Value(self._right[(i, j)]) for i in range(self._rows) for j in range(self._cols)}
        b_vals = {(i, j): self._solver.Value(self._bottom[(i, j)]) for i in range(self._rows) for j in range(self._cols)}
        use_vals = {p: self._solver.Value(self._use[p]) for p in range(len(self._use))}

        solution = self._build_region_grid(r_vals, b_vals)
        self._previous_solution = (r_vals, b_vals, use_vals, solution)
        return solution

    def _build_region_grid(self, r: dict, b: dict) -> RegionsGrid:
        region_matrix = [[-1 for _ in range(self._cols)] for _ in range(self._rows)]
        region_id = 0
        for i in range(self._rows):
            for j in range(self._cols):
                if (i, j) in self._blocked or region_matrix[i][j] != -1:
                    continue
                stack = [(i, j)]
                while stack:
                    ci, cj = stack.pop()
                    if (ci, cj) in self._blocked or region_matrix[ci][cj] != -1:
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
        for (i, j) in self._blocked:
            region_matrix[i][j] = region_id
            region_id += 1
        return RegionsGrid(region_matrix)

    def _add_blocking_constraint_use(self, use_vals: dict[int, int]):
        literals = [self._use[p] if val == 0 else self._use[p].Not() for p, val in use_vals.items()]
        self._model.add_bool_or(literals)

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return Grid.empty()
        _, _, use_vals, _ = self._previous_solution
        self._add_blocking_constraint_use(use_vals)
        return self.get_solution()
