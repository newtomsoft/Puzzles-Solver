from ortools.sat.python import cp_model
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class NuribouSolver(GameSolver):
    cell_empty = 0
    BLACK = -1

    def __init__(self, values_grid: Grid):
        super().__init__()
        self._values_grid = values_grid
        self._model = cp_model.CpModel()
        self._grid_vars = {}
        self._clues = {}
        self.rows_number = values_grid.rows_number
        self.columns_number = values_grid.columns_number
        self._status = None

    def _init_model(self):
        self._create_grid_variables()
        self._add_initial_clues()
        self._create_segment_variables()
        self._create_region_variables()
        self._add_constraints()

    def _create_variables(self):
        self._create_grid_variables()
        self._create_segment_variables()
        self._create_region_variables()

    def _create_grid_variables(self):
        self._grid_vars = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                position = Position(r, c)
                self._grid_vars[position] = self._model.new_bool_var(f"cell_{r}_{c}")

    def _add_initial_clues(self):
        for position, clue in self._values_grid:
            clue_val = int(clue) if clue else 0
            if clue_val > 0:
                self._model.add(self._grid_vars[position] == 0)
                self._clues[position] = clue_val

        self._num_clues = len(self._clues)

    def _create_segment_variables(self):
        max_run = max(self.rows_number, self.columns_number)

        self._h_left = Grid([[self._model.new_int_var(0, max_run, f"h_left_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._h_right = Grid([[self._model.new_int_var(0, max_run, f"h_right_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._v_up = Grid([[self._model.new_int_var(0, max_run, f"v_up_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._v_down = Grid([[self._model.new_int_var(0, max_run, f"v_down_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])

        self._is_horizontal = Grid([[self._model.new_bool_var(f"is_horizontal_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._segment_length = Grid([[self._model.new_int_var(0, max_run, f"segment_len_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_black = self._grid_vars[pos]
                is_white = is_black.negated()

                # Horizontal lengths
                if c == 0:
                    self._model.add(self._h_left[pos] == 1).OnlyEnforceIf(is_black)
                else:
                    self._model.add(self._h_left[pos] == self._h_left[r, c - 1] + 1).OnlyEnforceIf(is_black)
                self._model.add(self._h_left[pos] == 0).OnlyEnforceIf(is_white)

                if c == self.columns_number - 1:
                    self._model.add(self._h_right[pos] == 1).OnlyEnforceIf(is_black)
                else:
                    self._model.add(self._h_right[pos] == self._h_right[r, c + 1] + 1).OnlyEnforceIf(is_black)
                self._model.add(self._h_right[pos] == 0).OnlyEnforceIf(is_white)

                # Vertical lengths
                if r == 0:
                    self._model.add(self._v_up[pos] == 1).OnlyEnforceIf(is_black)
                else:
                    self._model.add(self._v_up[pos] == self._v_up[r - 1, c] + 1).OnlyEnforceIf(is_black)
                self._model.add(self._v_up[pos] == 0).OnlyEnforceIf(is_white)

                if r == self.rows_number - 1:
                    self._model.add(self._v_down[pos] == 1).OnlyEnforceIf(is_black)
                else:
                    self._model.add(self._v_down[pos] == self._v_down[r + 1, c] + 1).OnlyEnforceIf(is_black)
                self._model.add(self._v_down[pos] == 0).OnlyEnforceIf(is_white)

                total_h = self._model.new_int_var(0, max_run, f"total_h_{r}_{c}")
                total_v = self._model.new_int_var(0, max_run, f"total_v_{r}_{c}")
                self._model.add(total_h == self._h_left[pos] + self._h_right[pos] - 1).OnlyEnforceIf(is_black)
                self._model.add(total_v == self._v_up[pos] + self._v_down[pos] - 1).OnlyEnforceIf(is_black)
                self._model.add(total_h == 0).OnlyEnforceIf(is_white)
                self._model.add(total_v == 0).OnlyEnforceIf(is_white)

                h_len_ge2 = self._model.new_bool_var(f"h_len_ge2_{r}_{c}")
                self._model.add(total_h >= 2).OnlyEnforceIf(h_len_ge2)
                self._model.add(total_h <= 1).OnlyEnforceIf(h_len_ge2.negated())

                v_len_ge2 = self._model.new_bool_var(f"v_len_ge2_{r}_{c}")
                self._model.add(total_v >= 2).OnlyEnforceIf(v_len_ge2)
                self._model.add(total_v <= 1).OnlyEnforceIf(v_len_ge2.negated())

                self._model.add(self._is_horizontal[pos] == 1).OnlyEnforceIf(h_len_ge2)
                self._model.add(self._is_horizontal[pos] == 0).OnlyEnforceIf(v_len_ge2)

                self._model.add(self._segment_length[pos] == total_h).OnlyEnforceIf(self._is_horizontal[pos])
                self._model.add(self._segment_length[pos] == total_v).OnlyEnforceIf(self._is_horizontal[pos].negated())

    def _create_region_variables(self):
        clue_positions = list(self._clues.keys())
        self._num_clues = len(clue_positions)
        self._belong_vars = []
        for i, clue_pos in enumerate(clue_positions):
            grid_bool = Grid([[self._model.new_bool_var(f"belong_{i}_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
            self._belong_vars.append(grid_bool)
            self._model.add(grid_bool[clue_pos] == 1)

        self._clue_id_vars = Grid([[self._model.new_int_var(0, self._num_clues - 1, f"clue_id_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])

        total_cells = self.rows_number * self.columns_number
        self._rank_vars = Grid([[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_black = self._grid_vars[pos]
                is_white = is_black.negated()

                for i in range(self._num_clues):
                    self._model.add(self._belong_vars[i][pos] == 0).OnlyEnforceIf(is_black)
                    self._model.add(self._clue_id_vars[pos] == i).OnlyEnforceIf(self._belong_vars[i][pos])

                belongs = [self._belong_vars[i][pos] for i in range(self._num_clues)]
                self._model.add(sum(belongs) == 1).OnlyEnforceIf(is_white)

                # Neighbor same clue
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows_number and 0 <= nc < self.columns_number:
                        npos = Position(nr, nc)
                        nis_white = self._grid_vars[npos].negated()
                        self._model.add(self._clue_id_vars[pos] == self._clue_id_vars[npos]).OnlyEnforceIf([is_white, nis_white])

    def _add_constraints(self):
        self._add_no_segments_neighbors()
        self._add_straight_segments_constraint()
        self._add_region_size_and_unique_clue_constraints()
        self._add_region_connectivity_constraints()
        self._add_diagonal_segment_size_inequality_constraint()

    def _add_region_size_and_unique_clue_constraints(self):
        for i, clue_pos in enumerate(self._clues.keys()):
            clue_value = self._clues[clue_pos]
            belongs = [self._belong_vars[i][r, c] for r in range(self.rows_number) for c in range(self.columns_number)]
            self._model.add(sum(belongs) == clue_value)

    def _add_region_connectivity_constraints(self):
        for clue_pos in self._clues.keys():
            self._model.add(self._rank_vars[clue_pos] == 0)

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                if pos in self._clues:
                    continue

                is_white = self._grid_vars[pos].negated()
                parent_literals = []
                for neighbor in self._values_grid.neighbors_positions(pos):
                    nis_white = self._grid_vars[neighbor].negated()
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    self._model.add(nis_white == 1).OnlyEnforceIf(parent)
                    parent_literals.append(parent)

                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf(is_white)
                else:
                    self._model.add(is_white == 0)

    def _add_diagonal_segment_size_inequality_constraint(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                p1 = Position(r, c)
                p2 = Position(r + 1, c + 1)
                self._model.add(self._segment_length[p1] != self._segment_length[p2]).OnlyEnforceIf([self._grid_vars[p1], self._grid_vars[p2]])

        for r in range(self.rows_number - 1):
            for c in range(1, self.columns_number):
                p1 = Position(r, c)
                p2 = Position(r + 1, c - 1)
                self._model.add(self._segment_length[p1] != self._segment_length[p2]).OnlyEnforceIf([self._grid_vars[p1], self._grid_vars[p2]])

    def _add_no_segments_neighbors(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                b1 = self._grid_vars[Position(r, c)]
                b2 = self._grid_vars[Position(r, c + 1)]
                b3 = self._grid_vars[Position(r + 1, c)]
                b4 = self._grid_vars[Position(r + 1, c + 1)]
                self._model.add(b1 + b2 + b3 + b4 <= 2)

    def _add_straight_segments_constraint(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_black = self._grid_vars[pos]

                v_neighs = [self._grid_vars[p] for p in self._values_grid.neighbors_positions(pos) if p.c == c]
                h_neighs = [self._grid_vars[p] for p in self._values_grid.neighbors_positions(pos) if p.r == r]

                for v in v_neighs:
                    for h in h_neighs:
                        self._model.add_bool_or([is_black.negated(), v.negated(), h.negated()])

    def get_solution(self) -> Grid:
        if len(self._grid_vars) == 0:
            self._init_model()
        self._status = self._solver.Solve(self._model)
        if self._status == cp_model.OPTIMAL or self._status == cp_model.FEASIBLE:
            return self._compute_solution()
        return Grid.empty()

    def _compute_solution(self) -> Grid:
        solution_matrix = [[self.cell_empty for _ in range(self.columns_number)] for _ in range(self.rows_number)]
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
