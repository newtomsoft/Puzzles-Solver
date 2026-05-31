from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class ContextSolver(GameSolver):
    cell_empty = None
    black = 0
    white = 1

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = []
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_vars = [[self._model.new_bool_var(f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)]
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._grid_vars:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        solution = Grid([[self._solver.value(self._grid_vars[r][c]) for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        terms = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = self._previous_solution.value(r, c)
                terms.append(self._grid_vars[r][c].negated()) if val == self.white else terms.append(self._grid_vars[r][c])

        self._model.add_bool_or(terms)

        return self.get_solution()

    def _add_constraints(self):
        self._add_no_adjacent_black_cells_constraint()
        self._add_white_connectivity_constraint()
        self._add_number_constraints()

    def _add_no_adjacent_black_cells_constraint(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                if r + 1 < self._rows_number:
                    self._model.add(self._grid_vars[r][c] + self._grid_vars[r + 1][c] >= 1)
                if c + 1 < self._columns_number:
                    self._model.add(self._grid_vars[r][c] + self._grid_vars[r][c + 1] >= 1)

    def _add_white_connectivity_constraint(self):
        total_cells = self._rows_number * self._columns_number
        self._rank_vars = [[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)]
        is_root_vars = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)
                is_white = self._grid_vars[r][c]
                self._model.add(is_root <= is_white)
                self._model.add(self._rank_vars[r][c] == 0).OnlyEnforceIf(is_root)
        self._model.add(sum(is_root_vars) == 1)
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                is_white = self._grid_vars[r][c]
                is_root = is_root_vars[r * self._columns_number + c]
                parent_literals = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self._rows_number and 0 <= nc < self._columns_number:
                        parent = self._model.new_bool_var(f"parent_{r}_{c}_{nr}_{nc}")
                        self._model.add(self._grid_vars[nr][nc] == 1).OnlyEnforceIf(parent)
                        self._model.add(self._rank_vars[nr][nc] < self._rank_vars[r][c]).OnlyEnforceIf(parent)
                        parent_literals.append(parent)
                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_white, is_root.negated()])

    def _add_number_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                clue = self._grid[r][c]
                if clue is None or clue == self.empty:
                    continue
                clue = int(clue)
                pos = Position(r, c)
                is_white = self._grid_vars[r][c]
                is_black = is_white.negated()

                orthogonal_neighbors = self._get_orthogonal_neighbors(r, c)
                if orthogonal_neighbors:
                    orthogonal_black_sum = sum(1 - self._grid_vars[nr][nc] for nr, nc in orthogonal_neighbors)
                    self._model.add(orthogonal_black_sum == clue).OnlyEnforceIf(is_white)

                diagonal_neighbors = self._get_diagonal_neighbors(r, c)
                if diagonal_neighbors:
                    diagonal_black_sum = sum(1 - self._grid_vars[nr][nc] for nr, nc in diagonal_neighbors)
                    self._model.add(diagonal_black_sum == clue).OnlyEnforceIf(is_black)

    def _get_orthogonal_neighbors(self, r, c):
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self._rows_number and 0 <= nc < self._columns_number:
                neighbors.append((nr, nc))
        return neighbors

    def _get_diagonal_neighbors(self, r, c):
        neighbors = []
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self._rows_number and 0 <= nc < self._columns_number:
                neighbors.append((nr, nc))
        return neighbors
