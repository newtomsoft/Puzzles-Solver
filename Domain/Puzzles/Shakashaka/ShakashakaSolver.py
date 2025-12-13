from enum import IntEnum

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class ShakashakaCellType(IntEnum):
    WHITE_FULL = 0
    WHITE_BR = 1
    WHITE_BL = 2
    WHITE_TL = 3
    WHITE_TR = 4
    BLACK_FULL = 5


class ShakashakaSolver(GameSolver):
    # don't change these values
    input_white = -1
    input_black = -2

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
        self._grid_vars = Grid([[self._model.NewIntVar(ShakashakaCellType.WHITE_FULL, ShakashakaCellType.BLACK_FULL, f'cell_{r}_{c}') for c in range(self._columns_number)] for r in
                                range(self._rows_number)])
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
                row.append(ShakashakaCellType(int(val)))
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
                self._model.Add(self._grid_vars[position] == ShakashakaCellType.BLACK_FULL)
                continue
            self._model.Add(self._grid_vars[position] != ShakashakaCellType.BLACK_FULL)

    def _add_triangle_connectivity_constraints(self):
        allowed_horizontal = []
        for left in range(6):
            for right in range(6):
                valid = True
                if left == ShakashakaCellType.WHITE_BR and right not in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_BL]:
                    valid = False
                if left == ShakashakaCellType.WHITE_TR and right not in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_TL]:
                    valid = False
                if right == ShakashakaCellType.WHITE_BL and left not in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_BR]:
                    valid = False
                if right == ShakashakaCellType.WHITE_TL and left not in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_TR]:
                    valid = False

                if valid:
                    allowed_horizontal.append((left, right))

        for r in range(self._rows_number):
            for c in range(self._columns_number - 1):
                self._model.AddAllowedAssignments([self._grid_vars[r][c], self._grid_vars[r][c + 1]], allowed_horizontal)

        for r in range(self._rows_number):
            # Specific constraints for the cell on the right side
            self._model.Add(self._grid_vars[r][self._columns_number - 1] != ShakashakaCellType.WHITE_BR)
            self._model.Add(self._grid_vars[r][self._columns_number - 1] != ShakashakaCellType.WHITE_TR)
            self._model.Add(self._grid_vars[r][0] != ShakashakaCellType.WHITE_BL)
            self._model.Add(self._grid_vars[r][0] != ShakashakaCellType.WHITE_TL)

        allowed_vertical = []
        for top in range(6):
            for bottom in range(6):
                valid = True
                if top == ShakashakaCellType.WHITE_BR and bottom not in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_TR]:
                    valid = False
                if top == ShakashakaCellType.WHITE_BL and bottom not in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_TL]:
                    valid = False
                if bottom == ShakashakaCellType.WHITE_TR and top not in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_BR, ShakashakaCellType.WHITE_BL]:
                    valid = False
                if bottom == ShakashakaCellType.WHITE_TL and top not in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_BR, ShakashakaCellType.WHITE_BL]:
                    valid = False

                if valid:
                    allowed_vertical.append((top, bottom))

        for r in range(self._rows_number - 1):
            for c in range(self._columns_number):
                self._model.AddAllowedAssignments([self._grid_vars[r][c], self._grid_vars[r + 1][c]], allowed_vertical)

        for c in range(self._columns_number):
            self._model.Add(self._grid_vars[self._rows_number - 1][c] != ShakashakaCellType.WHITE_BR)
            self._model.Add(self._grid_vars[self._rows_number - 1][c] != ShakashakaCellType.WHITE_BL)
            self._model.Add(self._grid_vars[0][c] != ShakashakaCellType.WHITE_TL)
            self._model.Add(self._grid_vars[0][c] != ShakashakaCellType.WHITE_TR)

        # Interdire le motif suivant (horizontal) sur deux lignes consécutives:
        # Ligne r   :    [0]...[0][2] (au moins un 0 entre les deux colonnes)
        # Ligne r+1 : [1][0]...[0][3]
        # (Adapted logic for table constraints below)

        # Pattern 1: (Above=2, Cell=0) => Right=2
        allowed_p1 = []
        for t in range(6):
            for ce in range(6):
                for ri in range(6):
                    if t == ShakashakaCellType.WHITE_BL and ce == ShakashakaCellType.WHITE_FULL and ri != ShakashakaCellType.WHITE_BL:
                        continue
                    allowed_p1.append((t, ce, ri))

        for r in range(1, self._rows_number):
            for c in range(self._columns_number - 1):
                self._model.AddAllowedAssignments([self._grid_vars[r-1][c], self._grid_vars[r][c], self._grid_vars[r][c+1]], allowed_p1)

        allowed_p1_edge = []
        for t in range(6):
            for ce in range(6):
                if t == ShakashakaCellType.WHITE_BL and ce == ShakashakaCellType.WHITE_FULL:
                    continue
                allowed_p1_edge.append((t, ce))
        for r in range(1, self._rows_number):
             self._model.AddAllowedAssignments([self._grid_vars[r-1][self._columns_number-1], self._grid_vars[r][self._columns_number-1]], allowed_p1_edge)

        # Pattern 2: (Above=1, Cell=0) => Left=1
        allowed_p2 = []
        for t in range(6):
            for ce in range(6):
                for le in range(6):
                    if t == ShakashakaCellType.WHITE_BR and ce == ShakashakaCellType.WHITE_FULL and le != ShakashakaCellType.WHITE_BR:
                        continue
                    allowed_p2.append((t, ce, le))

        for r in range(1, self._rows_number):
            for c in range(1, self._columns_number):
                self._model.AddAllowedAssignments([self._grid_vars[r-1][c], self._grid_vars[r][c], self._grid_vars[r][c-1]], allowed_p2)

        allowed_p2_edge = []
        for t in range(6):
            for ce in range(6):
                if t == ShakashakaCellType.WHITE_BR and ce == ShakashakaCellType.WHITE_FULL:
                    continue
                allowed_p2_edge.append((t, ce))
        for r in range(1, self._rows_number):
            self._model.AddAllowedAssignments([self._grid_vars[r-1][0], self._grid_vars[r][0]], allowed_p2_edge)

        # Pattern 3: (Below=4, Cell=0) => Left=4
        allowed_p3 = []
        for b in range(6):
            for ce in range(6):
                for le in range(6):
                    if b == ShakashakaCellType.WHITE_TR and ce == ShakashakaCellType.WHITE_FULL and le != ShakashakaCellType.WHITE_TR:
                        continue
                    allowed_p3.append((b, ce, le))

        for r in range(self._rows_number - 1):
            for c in range(1, self._columns_number):
                self._model.AddAllowedAssignments([self._grid_vars[r+1][c], self._grid_vars[r][c], self._grid_vars[r][c-1]], allowed_p3)

        allowed_p3_edge = []
        for b in range(6):
            for ce in range(6):
                if b == ShakashakaCellType.WHITE_TR and ce == ShakashakaCellType.WHITE_FULL:
                    continue
                allowed_p3_edge.append((b, ce))
        for r in range(self._rows_number - 1):
            self._model.AddAllowedAssignments([self._grid_vars[r+1][0], self._grid_vars[r][0]], allowed_p3_edge)

        # Pattern 4: (Below=3, Cell=0) => Right=3
        allowed_p4 = []
        for b in range(6):
            for ce in range(6):
                for ri in range(6):
                    if b == ShakashakaCellType.WHITE_TL and ce == ShakashakaCellType.WHITE_FULL and ri != ShakashakaCellType.WHITE_TL:
                        continue
                    allowed_p4.append((b, ce, ri))

        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                self._model.AddAllowedAssignments([self._grid_vars[r+1][c], self._grid_vars[r][c], self._grid_vars[r][c+1]], allowed_p4)

        allowed_p4_edge = []
        for b in range(6):
            for ce in range(6):
                if b == ShakashakaCellType.WHITE_TL and ce == ShakashakaCellType.WHITE_FULL:
                    continue
                allowed_p4_edge.append((b, ce))
        for r in range(self._rows_number - 1):
            self._model.AddAllowedAssignments([self._grid_vars[r+1][self._columns_number-1], self._grid_vars[r][self._columns_number-1]], allowed_p4_edge)


    def _add_number_constraints(self):
        for position, val in [(pos, val) for pos, val in self._grid if val >= 0]:
            neighbors_var = []
            for neighbor_position in self._grid.neighbors_positions(position):
                is_1 = self._model.NewBoolVar(f'is_1_{neighbor_position}')
                is_2 = self._model.NewBoolVar(f'is_2_{neighbor_position}')
                is_3 = self._model.NewBoolVar(f'is_3_{neighbor_position}')
                is_4 = self._model.NewBoolVar(f'is_4_{neighbor_position}')
                neighbor_var = self._grid_vars[neighbor_position]
                self._model.Add(neighbor_var == ShakashakaCellType.WHITE_BR).OnlyEnforceIf(is_1)
                self._model.Add(neighbor_var != ShakashakaCellType.WHITE_BR).OnlyEnforceIf(is_1.Not())
                self._model.Add(neighbor_var == ShakashakaCellType.WHITE_BL).OnlyEnforceIf(is_2)
                self._model.Add(neighbor_var != ShakashakaCellType.WHITE_BL).OnlyEnforceIf(is_2.Not())
                self._model.Add(neighbor_var == ShakashakaCellType.WHITE_TL).OnlyEnforceIf(is_3)
                self._model.Add(neighbor_var != ShakashakaCellType.WHITE_TL).OnlyEnforceIf(is_3.Not())
                self._model.Add(neighbor_var == ShakashakaCellType.WHITE_TR).OnlyEnforceIf(is_4)
                self._model.Add(neighbor_var != ShakashakaCellType.WHITE_TR).OnlyEnforceIf(is_4.Not())
                neighbors_var.append(sum([is_1, is_2, is_3, is_4]))

            self._model.Add(sum(neighbors_var) == val)

    def _add_vertex_constraints(self):
        allowed_vertex = []
        for ul in range(6):
            for ur in range(6):
                for dl in range(6):
                    for dr in range(6):
                        d_ul = 1 if ul in [ShakashakaCellType.WHITE_BL, ShakashakaCellType.WHITE_TR] else 0
                        d_ur = 1 if ur in [ShakashakaCellType.WHITE_BR, ShakashakaCellType.WHITE_TL] else 0
                        d_dl = 1 if dl in [ShakashakaCellType.WHITE_BR, ShakashakaCellType.WHITE_TL] else 0
                        d_dr = 1 if dr in [ShakashakaCellType.WHITE_BL, ShakashakaCellType.WHITE_TR] else 0

                        diag_sum = d_ul + d_ur + d_dl + d_dr
                        if diag_sum not in [0, 2, 4]:
                            continue

                        w_ul = 1 if ul in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_BR] else 0
                        w_ur = 1 if ur in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_BL] else 0
                        w_dl = 1 if dl in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_TR] else 0
                        w_dr = 1 if dr in [ShakashakaCellType.WHITE_FULL, ShakashakaCellType.WHITE_TL] else 0

                        white_sum = w_ul + w_ur + w_dl + w_dr
                        if white_sum == 3:
                            continue

                        allowed_vertex.append((ul, ur, dl, dr))

        black_const = self._model.NewConstant(5)

        def get_var(r, c):
            if 0 <= r < self._rows_number and 0 <= c < self._columns_number:
                return self._grid_vars[r][c]
            return black_const

        for r in range(self._rows_number + 1):
            for c in range(self._columns_number + 1):
                vars_list = [
                    get_var(r - 1, c - 1),
                    get_var(r - 1, c),
                    get_var(r, c - 1),
                    get_var(r, c)
                ]
                self._model.AddAllowedAssignments(vars_list, allowed_vertex)

    def _new_bool_var_domain_check(self, var, allowed_values, name):
        b = self._model.NewBoolVar(name)
        table = []
        for val in range(6):
            table.append((val, 1 if val in allowed_values else 0))
        self._model.AddAllowedAssignments([var, b], table)
        return b

    def _add_rectangularity_constraints(self):
        # Interdire le motif suivant (horizontal) sur deux lignes consécutives:
        # Ligne r   : [1][0]...[0]   (au moins un 0 entre les deux colonnes)
        # Ligne r+1 : [4][0]...[0][2]
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                for e in range(c + 2, self._columns_number):
                    mid = e - 1
                    if self._grid[r][mid] != self.input_white or self._grid[r + 1][mid] != self.input_white:
                        break

                    if self._grid[r][e] != self.input_white or self._grid[r + 1][e] != self.input_white:
                        break

                    top_c = self._grid_vars[r][c]
                    bot_c = self._grid_vars[r + 1][c]
                    top_e = self._grid_vars[r][e]
                    bot_e = self._grid_vars[r + 1][e]

                    # Pattern 1
                    b_top_is_1 = self._new_bool_var_domain_check(top_c, [ShakashakaCellType.WHITE_BR], f'p1t1_{r}_{c}_{e}')
                    b_bot_is_4 = self._new_bool_var_domain_check(bot_c, [ShakashakaCellType.WHITE_TR], f'p1b4_{r}_{c}_{e}')
                    b_bote_is_2 = self._new_bool_var_domain_check(bot_e, [ShakashakaCellType.WHITE_BL], f'p1be2_{r}_{c}_{e}')
                    b_tope_is_3 = self._new_bool_var_domain_check(top_e, [ShakashakaCellType.WHITE_TL], f'p1te3_{r}_{c}_{e}')
                    clause1 = [b_top_is_1.Not(), b_bot_is_4.Not(), b_bote_is_2.Not(), b_tope_is_3.Not()]

                    # Interdire le motif suivant (horizontal) sur deux lignes consécutives:
                    # Ligne r   : [1][0]...[0][3] (au moins un 0 entre les deux colonnes)
                    # Ligne r+1 : [4][0]...[0]
                    # Pattern 2
                    b_p2_top1 = self._new_bool_var_domain_check(top_c, [ShakashakaCellType.WHITE_BR], f'p2t1_{r}_{c}_{e}')
                    b_p2_bot4 = self._new_bool_var_domain_check(bot_c, [ShakashakaCellType.WHITE_TR], f'p2b4_{r}_{c}_{e}')
                    b_p2_te3 = self._new_bool_var_domain_check(top_e, [ShakashakaCellType.WHITE_TL], f'p2te3_{r}_{c}_{e}')
                    clause2 = [b_p2_top1.Not(), b_p2_bot4.Not(), b_p2_te3.Not()]

                    # Interdire le motif suivant (horizontal) sur deux lignes consécutives:
                    # Ligne r   :    [0]...[0][2] (au moins un 0 entre les deux colonnes)
                    # Ligne r+1 : [1][0]...[0][3]
                    # Pattern 3
                    b_p3_top0 = self._new_bool_var_domain_check(top_c, [ShakashakaCellType.WHITE_FULL], f'p3t0_{r}_{c}_{e}')
                    b_p3_bot1 = self._new_bool_var_domain_check(bot_c, [ShakashakaCellType.WHITE_BR], f'p3b1_{r}_{c}_{e}')
                    b_p3_te2 = self._new_bool_var_domain_check(top_e, [ShakashakaCellType.WHITE_BL], f'p3te2_{r}_{c}_{e}')
                    b_p3_be3 = self._new_bool_var_domain_check(bot_e, [ShakashakaCellType.WHITE_TL], f'p3be3_{r}_{c}_{e}')
                    clause3 = [b_p3_top0.Not(), b_p3_bot1.Not(), b_p3_te2.Not(), b_p3_be3.Not()]

                    # Interdire le motif suivant (horizontal) sur deux lignes consécutives:
                    # Ligne r   : [4][0]...[0][2] (au moins un 0 entre les deux colonnes)
                    # Ligne r+1 :    [0]...[0][3]
                    # Pattern 4
                    b_p4_top4 = self._new_bool_var_domain_check(top_c, [ShakashakaCellType.WHITE_TR], f'p4t4_{r}_{c}_{e}')
                    b_p4_bot0 = self._new_bool_var_domain_check(bot_c, [ShakashakaCellType.WHITE_FULL], f'p4b0_{r}_{c}_{e}')
                    b_p4_te2 = self._new_bool_var_domain_check(top_e, [ShakashakaCellType.WHITE_BL], f'p4te2_{r}_{c}_{e}')
                    b_p4_be3 = self._new_bool_var_domain_check(bot_e, [ShakashakaCellType.WHITE_TL], f'p4be3_{r}_{c}_{e}')
                    clause4 = [b_p4_top4.Not(), b_p4_bot0.Not(), b_p4_te2.Not(), b_p4_be3.Not()]

                    for k in range(c + 1, e):
                        top_k = self._grid_vars[r][k]
                        bot_k = self._grid_vars[r + 1][k]
                        b_topk_0 = self._new_bool_var_domain_check(top_k, [ShakashakaCellType.WHITE_FULL], f'mid_t0_{r}_{k}')
                        b_botk_0 = self._new_bool_var_domain_check(bot_k, [ShakashakaCellType.WHITE_FULL], f'mid_b0_{r}_{k}')

                        not_mid = [b_topk_0.Not(), b_botk_0.Not()]
                        clause1.extend(not_mid)
                        clause2.extend(not_mid)
                        clause3.extend(not_mid)
                        clause4.extend(not_mid)

                    self._model.AddBoolOr(clause1)
                    self._model.AddBoolOr(clause2)
                    self._model.AddBoolOr(clause3)
                    self._model.AddBoolOr(clause4)

        # [4;1] ⇒ à droite [3;2]
        allowed_vpair1 = []
        for t in range(6):
            for b in range(6):
                for rt in range(6):
                    for rb in range(6):
                        if t == ShakashakaCellType.WHITE_TR and b == ShakashakaCellType.WHITE_BR:
                            if rt != ShakashakaCellType.WHITE_TL or rb != ShakashakaCellType.WHITE_BL:
                                continue
                        allowed_vpair1.append((t, b, rt, rb))

        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                self._model.AddAllowedAssignments([self._grid_vars[r][c], self._grid_vars[r+1][c], self._grid_vars[r][c+1], self._grid_vars[r+1][c+1]], allowed_vpair1)

        # [3;2] ⇒ à gauche [4;1]
        allowed_vpair2 = []
        for t in range(6):
            for b in range(6):
                for lt in range(6):
                    for lb in range(6):
                        if t == ShakashakaCellType.WHITE_TL and b == ShakashakaCellType.WHITE_BL:
                            if lt != ShakashakaCellType.WHITE_TR or lb != ShakashakaCellType.WHITE_BR:
                                continue
                        allowed_vpair2.append((t, b, lt, lb))

        for r in range(self._rows_number - 1):
            for c in range(1, self._columns_number):
                self._model.AddAllowedAssignments([self._grid_vars[r][c], self._grid_vars[r+1][c], self._grid_vars[r][c-1], self._grid_vars[r+1][c-1]], allowed_vpair2)
