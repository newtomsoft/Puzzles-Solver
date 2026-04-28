from ortools.sat.python import cp_model
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class KuroshutoSolver(GameSolver):
    EMPTY = None
    BLACK = '■'
    WHITE = '□'

    def __init__(self, values_grid: Grid):
        self._values_grid = values_grid
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = {}
        self._clues = {}
        self.rows_number = values_grid.rows_number
        self.columns_number = values_grid.columns_number
        self._status = None

    def _init_model(self):
        self._create_variables()
        self._add_initial_clues()
        self._add_constraints()

    def _create_variables(self):
        self._grid_vars = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                position = Position(r, c)
                # 1 if BLACK, 0 if WHITE
                self._grid_vars[position] = self._model.new_bool_var(f"cell_{r}_{c}")

    def _add_initial_clues(self):
        for position, clue in self._values_grid:
            if clue is None or clue == 0:
                continue

            self._model.add(self._grid_vars[position] == 0)
            clue_val = int(clue)
            self._clues[position] = clue_val

    def _add_constraints(self):
        self._add_distance_clue_constraint()
        self._add_no_adjacent_black_cells_constraint()
        self._add_white_connectivity_constraint()

    def _add_distance_clue_constraint(self):
        for position, clue_val in self._clues.items():
            r, c = position.r, position.c
            candidates = []

            potential_positions = [
                Position(r + clue_val, c),
                Position(r - clue_val, c),
                Position(r, c + clue_val),
                Position(r, c - clue_val)
            ]

            for p in potential_positions:
                if 0 <= p.r < self.rows_number and 0 <= p.c < self.columns_number:
                    candidates.append(self._grid_vars[p])

            self._model.add(sum(candidates) == 1)

    def _add_no_adjacent_black_cells_constraint(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows_number and 0 <= nc < self.columns_number:
                        npos = Position(nr, nc)
                        self._model.add(self._grid_vars[pos] + self._grid_vars[npos] <= 1)

    def _add_white_connectivity_constraint(self):
        total_cells = self.rows_number * self.columns_number
        self._rank_vars = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                self._rank_vars[pos] = self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}")

        clue_positions = list(self._clues.keys())
        if not clue_positions:
            return

        root_pos = clue_positions[0]
        self._model.add(self._rank_vars[root_pos] == 0)

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                if pos == root_pos:
                    continue

                is_white = self._grid_vars[pos].negated()
                parent_literals = []

                for neighbor in self._values_grid.neighbors_positions(pos):
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._grid_vars[neighbor] == 0).OnlyEnforceIf(parent)
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)

                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf(is_white)
                else:
                    self._model.add(is_white == 0)

    def get_solution(self) -> Grid:
        if not self._grid_vars:
            self._init_model()
        self._status = self._solver.Solve(self._model)
        if self._status == cp_model.OPTIMAL or self._status == cp_model.FEASIBLE:
            return self._compute_solution()
        return Grid.empty()

    def _compute_solution(self) -> Grid:
        solution_matrix = [[self.WHITE for _ in range(self.columns_number)] for _ in range(self.rows_number)]
        for position, var in self._grid_vars.items():
            if self._solver.Value(var):
                solution_matrix[position.r][position.c] = self.BLACK
        return Grid(solution_matrix)

    def get_other_solution(self) -> Grid:
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        literals = []
        for position, var in self._grid_vars.items():
            if self._solver.Value(var):
                literals.append(var.Not())
            else:
                literals.append(var)

        if literals:
            self._model.add_bool_or(literals)
            return self.get_solution()

        return Grid.empty()
