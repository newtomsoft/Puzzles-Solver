from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.GameSolver import GameSolver
from ortools.sat.python import cp_model


class SashikazuneSolver(GameSolver):
    def __init__(self, data_game: Grid):
        self._grid = data_game
        self.rows = self._grid.rows_number
        self.cols = self._grid.columns_number
        self._previous_solution = None
        self._model = cp_model.CpModel()
        self._pivot_rows = Grid([[self._model.new_int_var(0, self.rows - 1, f'pr_{r}_{c}') for c in range(self.cols)] for r in range(self.rows)])
        self._pivot_cols = Grid([[self._model.new_int_var(0, self.cols - 1, f'pc_{r}_{c}') for c in range(self.cols)] for r in range(self.rows)])
        self._is_pivot = Grid([[self._model.new_bool_var(f'is_pivot_{r}_{c}') for c in range(self.cols)] for r in range(self.rows)])
        self._constraints_added = False

    def get_solution(self) -> RegionsGrid:
        self._add_constraints()
        solution = self._solve()
        if solution.is_empty():
            self._previous_solution = RegionsGrid.empty()
            return RegionsGrid.empty()
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> RegionsGrid:
        self._add_exclusion_constraints()
        solution = self._solve()
        self._previous_solution = solution
        return solution

    def _solve(self) -> RegionsGrid:
        rows, cols = self.rows, self.cols
        solver = cp_model.CpSolver()
        status = solver.solve(self._model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return RegionsGrid([[solver.value(self._pivot_rows.value(r, c)) * cols + solver.value(self._pivot_cols.value(r, c)) for c in range(cols)] for r in range(rows)])

        return RegionsGrid.empty()

    def _add_constraints(self):
        self._add_cross_and_is_pivot_constraints()
        self._add_clue_distance_constraints()
        self._add_pivot_consistency_constraints()
        self._add_connectivity_constraints()
        self._add_l_shape_constraints()
        self._add_region_size_and_clue_count_constraints()
        self._constraints_added = True

    def _add_cross_and_is_pivot_constraints(self):
        for pos, _ in self._grid:
            r, c = pos.r, pos.c
            # Une cellule (r, c) doit être sur la croix de son pivot (pr, pc)
            row_equals_pivot = self._model.new_bool_var(f'r_eq_{r}_{c}')
            self._model.add(self._pivot_rows.value(pos) == r).only_enforce_if(row_equals_pivot)
            self._model.add(self._pivot_rows.value(pos) != r).only_enforce_if(~row_equals_pivot)
            col_equals_pivot = self._model.new_bool_var(f'c_eq_{r}_{c}')
            self._model.add(self._pivot_cols.value(pos) == c).only_enforce_if(col_equals_pivot)
            self._model.add(self._pivot_cols.value(pos) != c).only_enforce_if(~col_equals_pivot)
            self._model.add_bool_or([row_equals_pivot, col_equals_pivot])

            # is_p[r, c] est vrai si la cellule est son propre pivot
            self._model.add_bool_and([row_equals_pivot, col_equals_pivot]).only_enforce_if(self._is_pivot.value(pos))
            self._model.add_bool_or([~row_equals_pivot, ~col_equals_pivot]).only_enforce_if(~self._is_pivot.value(pos))

    def _add_clue_distance_constraints(self):
        for pos, val in [(p, v) for p, v in self._grid if v is not None]:
            delta_r = self._model.new_int_var(0, self.rows, f'dr_{pos}')
            self._model.add_abs_equality(delta_r, pos.r - self._pivot_rows.value(pos))
            delta_c = self._model.new_int_var(0, self.cols, f'dc_{pos}')
            self._model.add_abs_equality(delta_c, pos.c - self._pivot_cols.value(pos))
            self._model.add(delta_r + delta_c == val - 1)

    def _add_pivot_consistency_constraints(self):
        rows, cols = self.rows, self.cols
        pivot_rows_flat = [self._pivot_rows.value(pos) for pos, _ in self._grid]
        pivot_cols_flat = [self._pivot_cols.value(pos) for pos, _ in self._grid]
        for pos, _ in self._grid:
            idx = self._model.new_int_var(0, rows * cols - 1, f'idx_{pos}')
            self._model.add(idx == self._pivot_rows.value(pos) * cols + self._pivot_cols.value(pos))

            target_pivot_row = self._model.new_int_var(0, rows - 1, f'tpr_{pos}')
            self._model.add_element(idx, pivot_rows_flat, target_pivot_row)
            self._model.add(target_pivot_row == self._pivot_rows.value(pos))

            target_pivot_col = self._model.new_int_var(0, cols - 1, f'tpc_{pos}')
            self._model.add_element(idx, pivot_cols_flat, target_pivot_col)
            self._model.add(target_pivot_col == self._pivot_cols.value(pos))

    def _add_connectivity_constraints(self):
        rows, cols = self.rows, self.cols
        for pos, _ in self._grid:
            r, c = pos.r, pos.c
            if r > 0:
                is_beyond_pivot = self._model.new_bool_var(f'beyond_r_{r}_{c}')
                self._model.add(r > self._pivot_rows.value(pos)).only_enforce_if(is_beyond_pivot)
                self._model.add(r <= self._pivot_rows.value(pos)).only_enforce_if(~is_beyond_pivot)
                self._model.add(self._pivot_rows.value(r - 1, c) == self._pivot_rows.value(pos)).only_enforce_if(is_beyond_pivot)
                self._model.add(self._pivot_cols.value(r - 1, c) == self._pivot_cols.value(pos)).only_enforce_if(is_beyond_pivot)
            if r < rows - 1:
                is_beyond_pivot = self._model.new_bool_var(f'beyond_r_pos_{r}_{c}')
                self._model.add(r < self._pivot_rows.value(pos)).only_enforce_if(is_beyond_pivot)
                self._model.add(r >= self._pivot_rows.value(pos)).only_enforce_if(~is_beyond_pivot)
                self._model.add(self._pivot_rows.value(r + 1, c) == self._pivot_rows.value(pos)).only_enforce_if(is_beyond_pivot)
                self._model.add(self._pivot_cols.value(r + 1, c) == self._pivot_cols.value(pos)).only_enforce_if(is_beyond_pivot)
            if c > 0:
                is_beyond_pivot = self._model.new_bool_var(f'beyond_c_{r}_{c}')
                self._model.add(c > self._pivot_cols.value(pos)).only_enforce_if(is_beyond_pivot)
                self._model.add(c <= self._pivot_cols.value(pos)).only_enforce_if(~is_beyond_pivot)
                self._model.add(self._pivot_rows.value(r, c - 1) == self._pivot_rows.value(pos)).only_enforce_if(is_beyond_pivot)
                self._model.add(self._pivot_cols.value(r, c - 1) == self._pivot_cols.value(pos)).only_enforce_if(is_beyond_pivot)
            if c < cols - 1:
                is_beyond_pivot = self._model.new_bool_var(f'beyond_c_pos_{r}_{c}')
                self._model.add(c < self._pivot_cols.value(pos)).only_enforce_if(is_beyond_pivot)
                self._model.add(c >= self._pivot_cols.value(pos)).only_enforce_if(~is_beyond_pivot)
                self._model.add(self._pivot_rows.value(r, c + 1) == self._pivot_rows.value(pos)).only_enforce_if(is_beyond_pivot)
                self._model.add(self._pivot_cols.value(r, c + 1) == self._pivot_cols.value(pos)).only_enforce_if(is_beyond_pivot)

    def _add_l_shape_constraints(self):
        rows, cols = self.rows, self.cols
        for pos, _ in self._grid:
            r, c = pos.r, pos.c
            legs = []
            neighbors = [
                (self._grid.neighbor_up(pos), 'N'),
                (self._grid.neighbor_down(pos), 'S'),
                (self._grid.neighbor_left(pos), 'W'),
                (self._grid.neighbor_right(pos), 'E')
            ]
            for n_pos, name in neighbors:
                has_leg = self._model.new_bool_var(f'leg_{name}_{r}_{c}')
                if n_pos is not None:
                    neighbor_points_to_current = self._model.new_bool_var(f'np_{name}_{r}_{c}')
                    neighbor_pivot_row = self._model.new_bool_var(f'npr_{name}_{r}_{c}')
                    self._model.add(self._pivot_rows.value(n_pos) == r).only_enforce_if(neighbor_pivot_row)
                    self._model.add(self._pivot_rows.value(n_pos) != r).only_enforce_if(~neighbor_pivot_row)
                    neighbor_pivot_col = self._model.new_bool_var(f'npc_{name}_{r}_{c}')
                    self._model.add(self._pivot_cols.value(n_pos) == c).only_enforce_if(neighbor_pivot_col)
                    self._model.add(self._pivot_cols.value(n_pos) != c).only_enforce_if(~neighbor_pivot_col)
                    self._model.add_bool_and([neighbor_pivot_row, neighbor_pivot_col]).only_enforce_if(neighbor_points_to_current)
                    self._model.add_bool_or([~neighbor_pivot_row, ~neighbor_pivot_col]).only_enforce_if(~neighbor_points_to_current)
                    self._model.add(has_leg == neighbor_points_to_current)
                else:
                    self._model.add(has_leg == 0)
                legs.append(has_leg)

            # Chaque région est un L (un coude au pivot)
            self._model.add(legs[0] + legs[1] == 1).only_enforce_if(self._is_pivot.value(pos))
            self._model.add(legs[2] + legs[3] == 1).only_enforce_if(self._is_pivot.value(pos))

    def _add_region_size_and_clue_count_constraints(self):
        rows, cols = self.rows, self.cols
        p_cells = {pos: [] for pos, _ in self._grid}
        p_clues = {pos: [] for pos, _ in self._grid}

        for pos, val in self._grid:
            r, c = pos.r, pos.c
            # Les pivots potentiels pour (r, c) sont sur sa ligne ou colonne
            for i in range(rows):
                p_pos = Position(i, c)
                is_assigned_to_pivot = self._model.new_bool_var(f'm_{r}_{c}_{i}_{c}')
                match_row = self._model.new_bool_var(f'mr_{r}_{c}_{i}_{c}')
                self._model.add(self._pivot_rows.value(pos) == i).only_enforce_if(match_row)
                self._model.add(self._pivot_rows.value(pos) != i).only_enforce_if(~match_row)
                match_col = self._model.new_bool_var(f'mc_{r}_{c}_{i}_{c}')
                self._model.add(self._pivot_cols.value(pos) == c).only_enforce_if(match_col)
                self._model.add(self._pivot_cols.value(pos) != c).only_enforce_if(~match_col)
                self._model.add_bool_and([match_row, match_col]).only_enforce_if(is_assigned_to_pivot)
                self._model.add_bool_or([~match_row, ~match_col]).only_enforce_if(~is_assigned_to_pivot)

                p_cells[p_pos].append(is_assigned_to_pivot)
                if val is not None:
                    p_clues[p_pos].append(is_assigned_to_pivot)

            for j in range(cols):
                if j == c: continue
                p_pos = Position(r, j)
                is_assigned_to_pivot = self._model.new_bool_var(f'm_{r}_{c}_{r}_{j}')
                match_row = self._model.new_bool_var(f'mr_{r}_{c}_{r}_{j}')
                self._model.add(self._pivot_rows.value(pos) == r).only_enforce_if(match_row)
                self._model.add(self._pivot_rows.value(pos) != r).only_enforce_if(~match_row)
                match_col = self._model.new_bool_var(f'mc_{r}_{c}_{r}_{j}')
                self._model.add(self._pivot_cols.value(pos) == j).only_enforce_if(match_col)
                self._model.add(self._pivot_cols.value(pos) != j).only_enforce_if(~match_col)
                self._model.add_bool_and([match_row, match_col]).only_enforce_if(is_assigned_to_pivot)
                self._model.add_bool_or([~match_row, ~match_col]).only_enforce_if(~is_assigned_to_pivot)

                p_cells[p_pos].append(is_assigned_to_pivot)
                if val is not None:
                    p_clues[p_pos].append(is_assigned_to_pivot)

        for pos, _ in self._grid:
            # Taille >= 3 pour chaque pivot
            self._model.add(sum(p_cells[pos]) >= 3).only_enforce_if(self._is_pivot.value(pos))
            self._model.add(sum(p_cells[pos]) == 0).only_enforce_if(~self._is_pivot.value(pos))

            # Chaque région doit avoir au plus 3 indices
            self._model.add(sum(p_clues[pos]) <= 3)

    def _add_exclusion_constraints(self):
        rows, cols = self.rows, self.cols
        changes = []
        for pos, _ in self._grid:
            # pivot_id pour (r, c) = pr * cols + pc
            pivot_id = self._model.new_int_var(0, rows * cols - 1, f'pid_{pos.r}_{pos.c}')
            self._model.add(pivot_id == self._pivot_rows.value(pos) * cols + self._pivot_cols.value(pos))

            prev_pid = self._previous_solution[pos]
            diff = self._model.new_bool_var(f'diff_{pos.r}_{pos.c}')
            
            # diff est FAUX si pivot_id == prev_pid
            self._model.add(pivot_id == prev_pid).only_enforce_if(~diff)
            # diff est VRAI si pivot_id != prev_pid
            self._model.add(pivot_id != prev_pid).only_enforce_if(diff)
            
            changes.append(diff)
        
        # Au moins une cellule doit avoir un pivot différent de la solution précédente
        self._model.add_bool_or(changes)
