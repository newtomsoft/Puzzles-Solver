from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class FoseruzuSolver(GameSolver):
    def __init__(self, grid: Grid, clues: dict[str, list[int]] | None = None):
        self._grid = grid
        self._clues = clues or {}
        has_cell_clues = any(v is not None and v != GameSolver.empty for _, v in grid)
        if has_cell_clues:
            self._rows = grid.rows_number
            self._cols = grid.columns_number
        else:
            self._rows = len(self._clues.get('left', []))
            self._cols = len(self._clues.get('top', []))
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._r: dict[tuple[int, int], cp_model.IntVar] = {}
        self._b: dict[tuple[int, int], cp_model.IntVar] = {}
        self._previous_solution = None

    def _init_solver(self):
        for i in range(self._rows):
            for j in range(self._cols):
                self._r[(i, j)] = self._model.NewBoolVar(f'r_{i}_{j}')
                self._b[(i, j)] = self._model.NewBoolVar(f'b_{i}_{j}')

        has_cell_clues = any(v is not None and v != GameSolver.empty for _, v in self._grid)
        if has_cell_clues:
            self._add_cell_constraints()
        else:
            self._add_side_clues_constraints()

    def _add_side_clues_constraints(self):
        left = self._clues.get('left', [None] * self._rows)
        top = self._clues.get('top', [None] * self._cols)
        right = self._clues.get('right', [None] * self._rows)
        bottom = self._clues.get('bottom', [None] * self._cols)

        for i in range(self._rows):
            if left[i] is not None and left[i] != GameSolver.empty:
                self._model.Add(sum(self._r[(i, j)] for j in range(self._cols)) == left[i])

        for j in range(self._cols):
            if top[j] is not None and top[j] != GameSolver.empty:
                self._model.Add(sum(self._b[(i, j)] for i in range(self._rows)) == top[j])

        for i in range(self._rows):
            if right[i] is not None and right[i] != GameSolver.empty:
                self._model.Add(sum(self._b[(i, j)] for j in range(self._cols)) == right[i])

        for j in range(self._cols):
            if bottom[j] is not None and bottom[j] != GameSolver.empty:
                self._model.Add(sum(self._r[(i, j)] for i in range(self._rows)) == bottom[j])

    def _add_cell_constraints(self):
        for position, value in self._grid:
            i, j = position.r, position.c
            if value is None or value == GameSolver.empty:
                continue
            boundary_vars = []
            top_edge = self._model.NewBoolVar(f'ce_top_{i}_{j}')
            if i == 0:
                self._model.Add(top_edge == 1)
            else:
                self._model.Add(top_edge == self._b[(i - 1, j)])
            boundary_vars.append(top_edge)

            bottom_edge = self._model.NewBoolVar(f'ce_bottom_{i}_{j}')
            if i == self._rows - 1:
                self._model.Add(bottom_edge == 1)
            else:
                self._model.Add(bottom_edge == self._b[(i, j)])
            boundary_vars.append(bottom_edge)

            left_edge = self._model.NewBoolVar(f'ce_left_{i}_{j}')
            if j == 0:
                self._model.Add(left_edge == 1)
            else:
                self._model.Add(left_edge == self._r[(i, j - 1)])
            boundary_vars.append(left_edge)

            right_edge = self._model.NewBoolVar(f'ce_right_{i}_{j}')
            if j == self._cols - 1:
                self._model.Add(right_edge == 1)
            else:
                self._model.Add(right_edge == self._r[(i, j)])
            boundary_vars.append(right_edge)

            self._model.Add(sum(boundary_vars) == value)

    def get_solution(self) -> Grid:
        if not hasattr(self, '_solver_initialized') or not self._solver_initialized:
            self._init_solver()
            self._solver_initialized = True

        while True:
            status = self._solver.Solve(self._model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return Grid.empty()

            r_vals = {(i, j): self._solver.Value(self._r[(i, j)]) for i in range(self._rows) for j in range(self._cols)}
            b_vals = {(i, j): self._solver.Value(self._b[(i, j)]) for i in range(self._rows) for j in range(self._cols)}

            if self._is_valid_partition(r_vals, b_vals):
                matrix = [[r_vals[(i, j)] + 2 * b_vals[(i, j)] for j in range(self._cols)] for i in range(self._rows)]
                solution = Grid(matrix)
                self._previous_solution = (r_vals, b_vals, solution)
                return solution

            self._add_blocking_constraint(r_vals, b_vals)

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
                if len(component) != 4:
                    return False
        return True

    def _add_blocking_constraint(self, r: dict, b: dict):
        literals = []
        for (i, j), val in r.items():
            literals.append(self._r[(i, j)] if val == 0 else self._r[(i, j)].Not())
        for (i, j), val in b.items():
            literals.append(self._b[(i, j)] if val == 0 else self._b[(i, j)].Not())
        self._model.AddBoolOr(literals)

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return Grid.empty()
        r_vals, b_vals, _ = self._previous_solution
        self._add_blocking_constraint(r_vals, b_vals)
        return self.get_solution()
