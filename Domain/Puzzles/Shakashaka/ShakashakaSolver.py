from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class ShakashakaSolver(GameSolver):
    # don't change these values
    input_white = -1
    input_black = -2
    full_white = 0
    full_black = 5

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._previous_solution = Grid.empty()
        self._grid_vars = Grid.empty()
        self._init_solver()

    def _init_solver(self):
        # 1: White is BR
        # 2: White is BL
        # 3: White is TL
        # 4: White is TR
        self._grid_vars = Grid([[self._model.NewIntVar(self.full_white, self.full_black, f'cell_{r}_{c}') for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        status = self._solver.Solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            self._previous_solution = self._build_solution_grid()
            return self._previous_solution

        self._previous_solution = Grid.empty()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        previous_values = []
        all_vars = []
        for position, value in self._previous_solution:
            previous_values.append(value)
            all_vars.append(self._grid_vars[position])

        self._model.AddForbiddenAssignments(all_vars, [previous_values])

        return self.get_solution()

    def _build_solution_grid(self) -> Grid:
        solution_matrix = []
        for r in range(self._rows_number):
            row = []
            for c in range(self._columns_number):
                val = self._solver.Value(self._grid_vars[r][c])
                row.append(int(val))
            solution_matrix.append(row)
        return Grid(solution_matrix)

    def _add_constraints(self):
        self._add_fixed_cell_constraints()
        self._add_number_constraints()
        self._add_triangle_connectivity_constraints()
        self._add_vertex_constraints()
        self._add_rectangularity_constraints()

    def _add_fixed_cell_constraints(self):
        for position, val in self._grid:
            if val != self.input_white:
                self._model.Add(self._grid_vars[position] == self.full_black)
                continue
            self._model.Add(self._grid_vars[position] != self.full_black)

    def _add_triangle_connectivity_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                cell = self._grid_vars[r][c]

                if c + 1 >= self._columns_number:
                    self._model.Add(cell != 1)
                    self._model.Add(cell != 4)
                else:
                    neighbor = self._grid_vars[r][c + 1]
                    # Specific constraints for the cell on the right side
                    # If current cell is 1 (BR), the right neighbor can only be 0 (white) or 2 (BL)
                    b_is_1 = self._new_bool_var_domain_check(cell, [1], f'is_1_{r}_{c}')
                    b_valid_right_for_1 = self._new_bool_var_domain_check(neighbor, [0, 2], f'valid_right_for_1_{r}_{c}')
                    self._model.AddImplication(b_is_1, b_valid_right_for_1)

                    # If current cell is 4 (TR), keep previous allowance: right neighbor in [0, 3]
                    b_is_4 = self._new_bool_var_domain_check(cell, [4], f'is_4_{r}_{c}')
                    b_valid_right_for_4 = self._new_bool_var_domain_check(neighbor, [0, 3], f'valid_right_for_4_{r}_{c}')
                    self._model.AddImplication(b_is_4, b_valid_right_for_4)

                if c - 1 < 0:
                    self._model.Add(cell != 2)
                    self._model.Add(cell != 3)
                else:
                    neighbor = self._grid_vars[r][c - 1]
                    b_is_2 = self._new_bool_var_domain_check(cell, [2], f'is_2_{r}_{c}')
                    b_valid_left_for_2 = self._new_bool_var_domain_check(neighbor, [0, 1], f'valid_left_for_2_{r}_{c}')
                    self._model.AddImplication(b_is_2, b_valid_left_for_2)

                    b_is_3 = self._new_bool_var_domain_check(cell, [3], f'is_3_{r}_{c}')
                    b_valid_left_for_3 = self._new_bool_var_domain_check(neighbor, [0, 4], f'valid_left_for_3_{r}_{c}')
                    self._model.AddImplication(b_is_3, b_valid_left_for_3)

                if r + 1 >= self._rows_number:
                    self._model.Add(cell != 1)
                    self._model.Add(cell != 2)
                else:
                    neighbor = self._grid_vars[r + 1][c]
                    b_is_1_bottom = self._new_bool_var_domain_check(cell, [1], f'is_1_bottom_{r}_{c}')
                    b_valid_below_for_1 = self._new_bool_var_domain_check(neighbor, [0, 4], f'valid_below_for_1_{r}_{c}')
                    self._model.AddImplication(b_is_1_bottom, b_valid_below_for_1)

                    b_is_2_bottom = self._new_bool_var_domain_check(cell, [2], f'is_2_bottom_{r}_{c}')
                    b_valid_below_for_2 = self._new_bool_var_domain_check(neighbor, [0, 3], f'valid_below_for_2_{r}_{c}')
                    self._model.AddImplication(b_is_2_bottom, b_valid_below_for_2)

                if r - 1 < 0:
                    self._model.Add(cell != 3)
                    self._model.Add(cell != 4)
                else:
                    neighbor = self._grid_vars[r - 1][c]
                    b_needs_top = self._new_bool_var_domain_check(cell, [3, 4], f'needs_top_{r}_{c}')
                    b_valid_top = self._new_bool_var_domain_check(neighbor, [0, 1, 2], f'valid_top_{r}_{c}')
                    self._model.AddImplication(b_needs_top, b_valid_top)

                if r - 1 >= 0:
                    above = self._grid_vars[r - 1][c]
                    b_above_is_2 = self._new_bool_var_domain_check(above, [2], f'above_is_2_{r}_{c}')
                    b_above_is_1 = self._new_bool_var_domain_check(above, [1], f'above_is_1_{r}_{c}')
                    b_cell_is_0 = self._new_bool_var_domain_check(cell, [0], f'cell_is_0_{r}_{c}')

                    if c + 1 < self._columns_number:
                        right = self._grid_vars[r][c + 1]
                        b_right_is_2 = self._new_bool_var_domain_check(right, [2], f'right_is_2_{r}_{c}')
                        self._model.AddBoolOr([b_above_is_2.Not(), b_cell_is_0.Not(), b_right_is_2])
                    else:
                        self._model.AddBoolOr([b_above_is_2.Not(), b_cell_is_0.Not()])

                    if c - 1 >= 0:
                        left = self._grid_vars[r][c - 1]
                        b_left_is_1 = self._new_bool_var_domain_check(left, [1], f'left_is_1_{r}_{c}')
                        self._model.AddBoolOr([b_above_is_1.Not(), b_cell_is_0.Not(), b_left_is_1])
                    else:
                        self._model.AddBoolOr([b_above_is_1.Not(), b_cell_is_0.Not()])

                if r + 1 < self._rows_number:
                    below = self._grid_vars[r + 1][c]
                    b_below_is_4 = self._new_bool_var_domain_check(below, [4], f'below_is_4_{r}_{c}')
                    b_below_is_3 = self._new_bool_var_domain_check(below, [3], f'below_is_3_{r}_{c}')
                    b_cell_is_0_b = self._new_bool_var_domain_check(cell, [0], f'cell_is_0_b_{r}_{c}')

                    if c - 1 >= 0:
                        left2 = self._grid_vars[r][c - 1]
                        b_left_is_4 = self._new_bool_var_domain_check(left2, [4], f'left_is_4_{r}_{c}')
                        self._model.AddBoolOr([b_below_is_4.Not(), b_cell_is_0_b.Not(), b_left_is_4])
                    else:
                        self._model.AddBoolOr([b_below_is_4.Not(), b_cell_is_0_b.Not()])

                    if c + 1 < self._columns_number:
                        right2 = self._grid_vars[r][c + 1]
                        b_right_is_3 = self._new_bool_var_domain_check(right2, [3], f'right_is_3_{r}_{c}')
                        self._model.AddBoolOr([b_below_is_3.Not(), b_cell_is_0_b.Not(), b_right_is_3])
                    else:
                        self._model.AddBoolOr([b_below_is_3.Not(), b_cell_is_0_b.Not()])

    def _add_number_constraints(self):
        for position, val in [(pos, val) for pos, val in self._grid if val >= 0]:
            neighbors_var = []
            for neighbor_position in self._grid.neighbors_positions(position):
                is_1 = self._model.NewBoolVar(f'is_1_{neighbor_position}')
                is_2 = self._model.NewBoolVar(f'is_2_{neighbor_position}')
                is_3 = self._model.NewBoolVar(f'is_3_{neighbor_position}')
                is_4 = self._model.NewBoolVar(f'is_4_{neighbor_position}')
                neighbor_var = self._grid_vars[neighbor_position]
                self._model.Add(neighbor_var == 1).OnlyEnforceIf(is_1)
                self._model.Add(neighbor_var != 1).OnlyEnforceIf(is_1.Not())
                self._model.Add(neighbor_var == 2).OnlyEnforceIf(is_2)
                self._model.Add(neighbor_var != 2).OnlyEnforceIf(is_2.Not())
                self._model.Add(neighbor_var == 3).OnlyEnforceIf(is_3)
                self._model.Add(neighbor_var != 3).OnlyEnforceIf(is_3.Not())
                self._model.Add(neighbor_var == 4).OnlyEnforceIf(is_4)
                self._model.Add(neighbor_var != 4).OnlyEnforceIf(is_4.Not())
                neighbors_var.append(sum([is_1, is_2, is_3, is_4]))

            self._model.Add(sum(neighbors_var) == val)

    def _add_vertex_constraints(self):
        for r in range(self._rows_number + 1):
            for c in range(self._columns_number + 1):
                self._add_vertex_constraint(r, c)

    def _get_cell_var(self, r, c):
        if 0 <= r < self._rows_number and 0 <= c < self._columns_number:
            return self._grid_vars[r][c]
        return 5

    def _add_vertex_constraint(self, r, c):
        ul = self._get_cell_var(r - 1, c - 1)
        ur = self._get_cell_var(r - 1, c)
        dl = self._get_cell_var(r, c - 1)
        dr = self._get_cell_var(r, c)

        d_ul = self._new_bool_var_domain_check(ul, [2, 4], f'd_ul_{r}_{c}')
        d_ur = self._new_bool_var_domain_check(ur, [1, 3], f'd_ur_{r}_{c}')
        d_dl = self._new_bool_var_domain_check(dl, [1, 3], f'd_dl_{r}_{c}')
        d_dr = self._new_bool_var_domain_check(dr, [2, 4], f'd_dr_{r}_{c}')

        diag_sum_var = self._model.NewIntVar(0, 4, f'diag_sum_{r}_{c}')
        self._model.Add(diag_sum_var == sum([d_ul, d_ur, d_dl, d_dr]))
        self._model.AddAllowedAssignments([diag_sum_var], [(0,), (2,), (4,)])

        w_ul = self._new_bool_var_domain_check(ul, [0, 1], f'w_ul_{r}_{c}')
        w_ur = self._new_bool_var_domain_check(ur, [0, 2], f'w_ur_{r}_{c}')
        w_dl = self._new_bool_var_domain_check(dl, [0, 4], f'w_dl_{r}_{c}')
        w_dr = self._new_bool_var_domain_check(dr, [0, 3], f'w_dr_{r}_{c}')

        white_sum = sum([w_ul, w_ur, w_dl, w_dr])
        self._model.Add(white_sum != 3)

        white_sum_var = self._model.NewIntVar(0, 4, f'white_sum_{r}_{c}')
        self._model.Add(white_sum_var == white_sum)

        b_ws2 = self._model.NewBoolVar(f'ws2_{r}_{c}')
        self._model.Add(white_sum_var >= 2).OnlyEnforceIf(b_ws2)
        self._model.Add(white_sum_var <= 2).OnlyEnforceIf(b_ws2)

        def both_true_bool(a, b, name_suffix):
            b_and = self._model.NewBoolVar(f'both_{name_suffix}_{r}_{c}')
            self._model.Add(a + b >= 2).OnlyEnforceIf(b_and)
            self._model.Add(a + b <= 2).OnlyEnforceIf(b_and)
            self._model.Add(a + b <= 1).OnlyEnforceIf(b_and.Not())
            return b_and

        adj_ul_ur = both_true_bool(w_ul, w_ur, 'ul_ur')
        adj_ur_dr = both_true_bool(w_ur, w_dr, 'ur_dr')
        adj_dr_dl = both_true_bool(w_dr, w_dl, 'dr_dl')
        adj_dl_ul = both_true_bool(w_dl, w_ul, 'dl_ul')

        for idx, adj in enumerate([adj_ul_ur, adj_ur_dr, adj_dr_dl, adj_dl_ul]):
            forbid = self._model.NewBoolVar(f'forbid_adjL_{idx}_{r}_{c}')
            self._model.AddImplication(forbid, adj)
            self._model.AddImplication(forbid, b_ws2)
            self._model.Add(forbid == 0)

    def _new_bool_var_domain_check(self, var, allowed_values, name):
        b = self._model.NewBoolVar(name)

        table = []
        for val in range(6):
            if val in allowed_values:
                table.append((val, 1))
            else:
                table.append((val, 0))
        self._model.AddAllowedAssignments([var, b], table)
        return b

    def _add_rectangularity_constraints(self):
        # Interdire le motif suivant (horizontal) sur deux lignes consécutives:
        # Ligne r   : [1][0]...[0]   (au moins un 0 entre les deux colonnes)
        # Ligne r+1 : [4][0]...[0][2]
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):  # besoin d'au moins une colonne à droite
                for e in range(c + 2, self._columns_number):
                    top_c = self._grid_vars[r][c]
                    bot_c = self._grid_vars[r + 1][c]
                    bot_e = self._grid_vars[r + 1][e]
                    top_e = self._grid_vars[r][e]

                    b_top_is_1 = self._new_bool_var_domain_check(top_c, [1], f'pat_top1_{r}_{c}_e{e}')
                    b_bot_is_4 = self._new_bool_var_domain_check(bot_c, [4], f'pat_bot4_{r}_{c}_e{e}')
                    b_bote_is_2 = self._new_bool_var_domain_check(bot_e, [2], f'pat_bote2_{r}_{c}_e{e}')
                    b_tope_is_3 = self._new_bool_var_domain_check(top_e, [3], f'pat_tope3_{r}_{c}_e{e}')

                    clause = [b_top_is_1.Not(), b_bot_is_4.Not(), b_bote_is_2.Not(), b_tope_is_3.Not()]

                    for k in range(c + 1, e):
                        top_k = self._grid_vars[r][k]
                        bot_k = self._grid_vars[r + 1][k]
                        b_topk_is_0 = self._new_bool_var_domain_check(top_k, [0], f'pat_top0_{r}_{k}_from{c}_to{e}')
                        b_botk_is_0 = self._new_bool_var_domain_check(bot_k, [0], f'pat_bot0_{r + 1}_{k}_from{c}_to{e}')
                        clause.append(b_topk_is_0.Not())
                        clause.append(b_botk_is_0.Not())

                    self._model.AddBoolOr(clause)

        # Interdire le motif suivant (horizontal) sur deux lignes consécutives:
        # Ligne r   : [1][0]...[0][3] (au moins un 0 entre les deux colonnes)
        # Ligne r+1 : [4][0]...[0]
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                for e in range(c + 2, self._columns_number):
                    top_c = self._grid_vars[r][c]
                    bot_c = self._grid_vars[r + 1][c]
                    top_e = self._grid_vars[r][e]

                    b_top_is_1 = self._new_bool_var_domain_check(top_c, [1], f'patA_top1_{r}_{c}_e{e}')
                    b_bot_is_4 = self._new_bool_var_domain_check(bot_c, [4], f'patA_bot4_{r}_{c}_e{e}')
                    b_tope_is_3 = self._new_bool_var_domain_check(top_e, [3], f'patA_tope3_{r}_{c}_e{e}')

                    clause = [b_top_is_1.Not(), b_bot_is_4.Not(), b_tope_is_3.Not()]
                    for k in range(c + 1, e):
                        b_topk_is_0 = self._new_bool_var_domain_check(self._grid_vars[r][k], [0], f'patA_top0_{r}_{k}_from{c}_to{e}')
                        b_botk_is_0 = self._new_bool_var_domain_check(self._grid_vars[r + 1][k], [0], f'patA_bot0_{r + 1}_{k}_from{c}_to{e}')
                        clause.append(b_topk_is_0.Not())
                        clause.append(b_botk_is_0.Not())
                    self._model.AddBoolOr(clause)

        # Interdire le motif suivant (horizontal) sur deux lignes consécutives:
        # Ligne r   :    [0]...[0][2] (au moins un 0 entre les deux colonnes)
        # Ligne r+1 : [1][0]...[0][3]
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                for e in range(c + 2, self._columns_number):
                    top_c = self._grid_vars[r][c]
                    bot_c = self._grid_vars[r + 1][c]
                    top_e = self._grid_vars[r][e]
                    bot_e = self._grid_vars[r + 1][e]

                    b_topc_is_0 = self._new_bool_var_domain_check(top_c, [0], f'patB_topc0_{r}_{c}_e{e}')
                    b_botc_is_1 = self._new_bool_var_domain_check(bot_c, [1], f'patB_botc1_{r}_{c}_e{e}')
                    b_tope_is_2 = self._new_bool_var_domain_check(top_e, [2], f'patB_tope2_{r}_{c}_e{e}')
                    b_bote_is_3 = self._new_bool_var_domain_check(bot_e, [3], f'patB_bote3_{r}_{c}_e{e}')

                    clause = [b_topc_is_0.Not(), b_botc_is_1.Not(), b_tope_is_2.Not(), b_bote_is_3.Not()]
                    for k in range(c + 1, e):
                        b_topk_is_0 = self._new_bool_var_domain_check(self._grid_vars[r][k], [0], f'patB_top0_{r}_{k}_from{c}_to{e}')
                        b_botk_is_0 = self._new_bool_var_domain_check(self._grid_vars[r + 1][k], [0], f'patB_bot0_{r + 1}_{k}_from{c}_to{e}')
                        clause.append(b_topk_is_0.Not())
                        clause.append(b_botk_is_0.Not())
                    self._model.AddBoolOr(clause)

        # Interdire le motif suivant (horizontal) sur deux lignes consécutives:
        # Ligne r   : [4][0]...[0][2] (au moins un 0 entre les deux colonnes)
        # Ligne r+1 :    [0]...[0][3]
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                for e in range(c + 2, self._columns_number):
                    top_c = self._grid_vars[r][c]
                    bot_c = self._grid_vars[r + 1][c]
                    top_e = self._grid_vars[r][e]
                    bot_e = self._grid_vars[r + 1][e]

                    b_topc_is_4 = self._new_bool_var_domain_check(top_c, [4], f'patC_topc4_{r}_{c}_e{e}')
                    b_botc_is_0 = self._new_bool_var_domain_check(bot_c, [0], f'patC_botc0_{r}_{c}_e{e}')
                    b_tope_is_2 = self._new_bool_var_domain_check(top_e, [2], f'patC_tope2_{r}_{c}_e{e}')
                    b_bote_is_3 = self._new_bool_var_domain_check(bot_e, [3], f'patC_bote3_{r}_{c}_e{e}')

                    clause = [b_topc_is_4.Not(), b_botc_is_0.Not(), b_tope_is_2.Not(), b_bote_is_3.Not()]
                    for k in range(c + 1, e):
                        b_topk_is_0 = self._new_bool_var_domain_check(self._grid_vars[r][k], [0], f'patC_top0_{r}_{k}_from{c}_to{e}')
                        b_botk_is_0 = self._new_bool_var_domain_check(self._grid_vars[r + 1][k], [0], f'patC_bot0_{r + 1}_{k}_from{c}_to{e}')
                        clause.append(b_topk_is_0.Not())
                        clause.append(b_botk_is_0.Not())
                    self._model.AddBoolOr(clause)

        # [4;1] ⇒ à droite [3;2]
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                top = self._grid_vars[r][c]
                bottom = self._grid_vars[r + 1][c]
                right = self._grid_vars[r][c + 1]
                right_bottom = self._grid_vars[r + 1][c + 1]

                b_top_is_4 = self._new_bool_var_domain_check(top, [4], f'vpair_top4_{r}_{c}')
                b_bot_is_1 = self._new_bool_var_domain_check(bottom, [1], f'vpair_bot1_{r}_{c}')

                b_pair_41 = self._model.NewBoolVar(f'pair41_{r}_{c}')
                self._model.Add(b_top_is_4 + b_bot_is_1 >= 2).OnlyEnforceIf(b_pair_41)
                self._model.Add(b_top_is_4 + b_bot_is_1 <= 2).OnlyEnforceIf(b_pair_41)
                self._model.Add(b_top_is_4 + b_bot_is_1 <= 1).OnlyEnforceIf(b_pair_41.Not())

                b_right_is_3 = self._new_bool_var_domain_check(right, [3], f'vpair_right3_{r}_{c}')
                b_rb_is_2 = self._new_bool_var_domain_check(right_bottom, [2], f'vpair_rb2_{r}_{c}')

                self._model.AddImplication(b_pair_41, b_right_is_3)
                self._model.AddImplication(b_pair_41, b_rb_is_2)

        # [3;2] ⇒ à gauche [4;1]
        for r in range(self._rows_number - 1):
            for c in range(1, self._columns_number):
                top = self._grid_vars[r][c]
                bottom = self._grid_vars[r + 1][c]
                left = self._grid_vars[r][c - 1]
                left_bottom = self._grid_vars[r + 1][c - 1]

                b_top_is_3 = self._new_bool_var_domain_check(top, [3], f'vpair_top3_{r}_{c}')
                b_bot_is_2 = self._new_bool_var_domain_check(bottom, [2], f'vpair_bot2_{r}_{c}')

                b_pair_32 = self._model.NewBoolVar(f'pair32_{r}_{c}')
                self._model.Add(b_top_is_3 + b_bot_is_2 >= 2).OnlyEnforceIf(b_pair_32)
                self._model.Add(b_top_is_3 + b_bot_is_2 <= 2).OnlyEnforceIf(b_pair_32)
                self._model.Add(b_top_is_3 + b_bot_is_2 <= 1).OnlyEnforceIf(b_pair_32.Not())

                b_left_is_4 = self._new_bool_var_domain_check(left, [4], f'vpair_left4_{r}_{c}')
                b_lb_is_1 = self._new_bool_var_domain_check(left_bottom, [1], f'vpair_lb1_{r}_{c}')

                self._model.AddImplication(b_pair_32, b_left_is_4)
                self._model.AddImplication(b_pair_32, b_lb_is_1)
