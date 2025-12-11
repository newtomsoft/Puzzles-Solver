from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class ShakashakaSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = []

    def _init_solver(self):
        # 0: Empty (White)
        # 1: TL Triangle (White is BR)
        # 2: TR Triangle (White is BL)
        # 3: BR Triangle (White is TL)
        # 4: BL Triangle (White is TR)
        # 5: Black (Full Black)
        self._grid_vars = [[self._model.NewIntVar(0, 5, f'cell_{r}_{c}') for c in range(self._columns_number)] for r in range(self._rows_number)]
        self._add_constraints()

    def get_solution(self) -> Grid:
        self._init_solver()
        status = self._solver.Solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return self._build_solution_grid()
        # Return a grid with dimensions but empty values, or None, depending on contract.
        # But Grid([]) fails.
        return Grid([[0] * self._columns_number for _ in range(self._rows_number)])

    def get_other_solution(self) -> Grid:
        # Not strictly required for initial scaffold unless needed for uniqueness checks
        return Grid([])

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
        self._add_black_cell_number_constraints()
        self._add_rectangularity_constraints()
        self._add_triangle_connectivity_constraints()

    def _add_triangle_connectivity_constraints(self):
        # Triangles must form Rotated Rectangles, so they cannot have Grid Line boundaries.
        # This implies that every "White Face" of a Triangle must connect to a "White Face" of a neighbor Triangle.
        # It cannot connect to Empty(0), Black(5), or Border.

        # White Faces per type:
        # 1(TL): Right, Bottom
        # 2(TR): Left, Bottom
        # 3(BR): Left, Top
        # 4(BL): Right, Top

        # Neighbor Requirements (must have matching white face):
        # If Cell needs Right Neighbor (East): Neighbor must have Left White Face (TR(2), BR(3)).
        # If Cell needs Left Neighbor (West): Neighbor must have Right White Face (TL(1), BL(4)).
        # If Cell needs Bottom Neighbor (South): Neighbor must have Top White Face (BR(3), BL(4)).
        # If Cell needs Top Neighbor (North): Neighbor must have Bottom White Face (TL(1), TR(2)).

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                # We can implement this using implications on the variable values.
                cell = self._grid_vars[r][c]

                # Check Right (East) Constraint
                # Applies if cell in {1, 4} (TL, BL have Right White Face)
                # But wait: TL(1) White is Right/Bottom. BL(4) White is Right/Top.
                # Yes.

                # If cell has Right White Face:
                # Neighbor (r, c+1) MUST exist and be in {2, 3} (TR, BR).

                # If (r, c+1) does not exist (Border):
                # Cell cannot be {1, 4}.
                if c + 1 >= self._columns_number:
                    self._model.Add(cell != 1)
                    self._model.Add(cell != 4)
                else:
                    neighbor = self._grid_vars[r][c+1]
                    # Allowed neighbors for {1, 4} are {2, 3}.
                    # Logic: (cell in {1, 4}) => (neighbor in {2, 3})

                    b_needs_right = self._new_bool_var_domain_check(cell, [1, 4], f'needs_right_{r}_{c}')
                    b_valid_right = self._new_bool_var_domain_check(neighbor, [2, 3], f'valid_right_{r}_{c}')
                    self._model.AddImplication(b_needs_right, b_valid_right)

                # Check Left (West) Constraint
                # Applies if cell in {2, 3} (TR, BR have Left White Face)
                # Neighbor (r, c-1) MUST exist and be in {1, 4} (TL, BL).
                if c - 1 < 0:
                    self._model.Add(cell != 2)
                    self._model.Add(cell != 3)
                else:
                    neighbor = self._grid_vars[r][c-1]
                    b_needs_left = self._new_bool_var_domain_check(cell, [2, 3], f'needs_left_{r}_{c}')
                    b_valid_left = self._new_bool_var_domain_check(neighbor, [1, 4], f'valid_left_{r}_{c}')
                    self._model.AddImplication(b_needs_left, b_valid_left)

                # Check Bottom (South) Constraint
                # Applies if cell in {1, 2} (TL, TR have Bottom White Face)
                # Neighbor (r+1, c) MUST exist and be in {3, 4} (BR, BL).
                if r + 1 >= self._rows_number:
                    self._model.Add(cell != 1)
                    self._model.Add(cell != 2)
                else:
                    neighbor = self._grid_vars[r+1][c]
                    b_needs_bottom = self._new_bool_var_domain_check(cell, [1, 2], f'needs_bottom_{r}_{c}')
                    b_valid_bottom = self._new_bool_var_domain_check(neighbor, [3, 4], f'valid_bottom_{r}_{c}')
                    self._model.AddImplication(b_needs_bottom, b_valid_bottom)

                # Check Top (North) Constraint
                # Applies if cell in {3, 4} (BR, BL have Top White Face)
                # Neighbor (r-1, c) MUST exist and be in {1, 2} (TL, TR).
                if r - 1 < 0:
                    self._model.Add(cell != 3)
                    self._model.Add(cell != 4)
                else:
                    neighbor = self._grid_vars[r-1][c]
                    b_needs_top = self._new_bool_var_domain_check(cell, [3, 4], f'needs_top_{r}_{c}')
                    b_valid_top = self._new_bool_var_domain_check(neighbor, [1, 2], f'valid_top_{r}_{c}')
                    self._model.AddImplication(b_needs_top, b_valid_top)

    def _add_fixed_cell_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = self._grid[r][c]
                # Input grid convention:
                # -1: Empty White (Constraint: Must be 0-4)
                # -2: Empty Black (Constraint: Must be 5)
                # 0-4: Numbered Black (Constraint: Must be 5)
                if val == -2:
                    self._model.Add(self._grid_vars[r][c] == 5)
                elif val >= 0:
                    self._model.Add(self._grid_vars[r][c] == 5)
                else: # val == -1 (White)
                    self._model.Add(self._grid_vars[r][c] != 5)

    def _add_black_cell_number_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = self._grid[r][c]
                if val >= 0:
                    neighbors = []
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self._rows_number and 0 <= nc < self._columns_number:
                            # Count if neighbor is a triangle (1-4)
                            is_1 = self._model.NewBoolVar(f'is_1_{nr}_{nc}')
                            is_2 = self._model.NewBoolVar(f'is_2_{nr}_{nc}')
                            is_3 = self._model.NewBoolVar(f'is_3_{nr}_{nc}')
                            is_4 = self._model.NewBoolVar(f'is_4_{nr}_{nc}')

                            self._model.Add(self._grid_vars[nr][nc] == 1).OnlyEnforceIf(is_1)
                            self._model.Add(self._grid_vars[nr][nc] != 1).OnlyEnforceIf(is_1.Not())
                            self._model.Add(self._grid_vars[nr][nc] == 2).OnlyEnforceIf(is_2)
                            self._model.Add(self._grid_vars[nr][nc] != 2).OnlyEnforceIf(is_2.Not())
                            self._model.Add(self._grid_vars[nr][nc] == 3).OnlyEnforceIf(is_3)
                            self._model.Add(self._grid_vars[nr][nc] != 3).OnlyEnforceIf(is_3.Not())
                            self._model.Add(self._grid_vars[nr][nc] == 4).OnlyEnforceIf(is_4)
                            self._model.Add(self._grid_vars[nr][nc] != 4).OnlyEnforceIf(is_4.Not())

                            neighbors.append(sum([is_1, is_2, is_3, is_4]))

                    self._model.Add(sum(neighbors) == val)

    def _add_rectangularity_constraints(self):
        # Iterate over all internal vertices
        # Vertex (r, c) is the intersection of row r and col c
        # (Where r in 1..R, c in 1..C relative to grid lines? No, 0..R, 0..C)
        # There are (R+1)*(C+1) vertices.
        # But we only care about vertices where 4 cells meet (Interior vertices).
        # These are r in 1..R-1, c in 1..C-1.

        for r in range(1, self._rows_number):
            for c in range(1, self._columns_number):
                self._add_vertex_constraint(r, c)

    def _add_vertex_constraint(self, r, c):
        # Cells around vertex (r,c):
        # UL: (r-1, c-1) -> BR corner
        # UR: (r-1, c)   -> BL corner
        # DL: (r, c-1)   -> TR corner
        # DR: (r, c)     -> TL corner

        ul = self._grid_vars[r-1][c-1]
        ur = self._grid_vars[r-1][c]
        dl = self._grid_vars[r][c-1]
        dr = self._grid_vars[r][c]

        # 1. Diagonal Parity Check
        # Does a diagonal touch the vertex?
        # UL (BR corner): Diag if UL in {TR(2), BL(4)}
        # UR (BL corner): Diag if UR in {TL(1), BR(3)}
        # DL (TR corner): Diag if DL in {TL(1), BR(3)}
        # DR (TL corner): Diag if DR in {TR(2), BL(4)}

        d_ul = self._new_bool_var_domain_check(ul, [2, 4], f'd_ul_{r}_{c}')
        d_ur = self._new_bool_var_domain_check(ur, [1, 3], f'd_ur_{r}_{c}')
        d_dl = self._new_bool_var_domain_check(dl, [1, 3], f'd_dl_{r}_{c}')
        d_dr = self._new_bool_var_domain_check(dr, [2, 4], f'd_dr_{r}_{c}')

        diag_sum_var = self._model.NewIntVar(0, 4, f'diag_sum_{r}_{c}')
        self._model.Add(diag_sum_var == sum([d_ul, d_ur, d_dl, d_dr]))
        self._model.AddAllowedAssignments([diag_sum_var], [(0,), (2,), (4,)])

        # 2. No 270-degree White Check (Exactly 3 White Quadrants Forbidden)
        # White Quadrant = Open space (0) or White part of Triangle
        # Note: If diagonal touches vertex, we treat it as "Blocked" (Not White) for this count check
        # because the diagonal acts as a wall.
        # So "White" means the corner is purely white space.

        # UL (BR corner): White if UL in {0, 1, 3}?
        #   TL(1): Diag / (BL-TR). BR is White. Yes.
        #   BR(3): Diag / (BL-TR). BR is Black? No.
        #     BR Triangle: In BR corner. Diagonal BL-TR.
        #     So BR corner is occupied by Triangle (Black).
        #     Wait. If Triangle is IN BR corner, then BR corner is Black.
        #     So BR(3) corner is NOT White.
        #   Let's re-verify Corner Colors.
        #   0(E): All White.
        #   5(B): All Black.
        #   1(TL): Triangle in TL. BR is White. (TR, BL blocked by diag). TL Black.
        #   2(TR): Triangle in TR. BL is White. (TL, BR blocked by diag). TR Black.
        #   3(BR): Triangle in BR. TL is White. (TR, BL blocked by diag). BR Black.
        #   4(BL): Triangle in BL. TR is White. (TL, BR blocked by diag). BL Black.

        # Mapping for White Corner at Vertex:
        # UL (BR corner): White if UL in {0, 1}. (3 is Black, 2,4 are Diag/Blocked).
        # UR (BL corner): White if UR in {0, 2}. (1,3 Diag, 4 Black).
        # DL (TR corner): White if DL in {0, 4}. (1,3 Diag, 2 Black).
        # DR (TL corner): White if DR in {0, 3}. (2,4 Diag, 1 Black).

        w_ul = self._new_bool_var_domain_check(ul, [0, 1], f'w_ul_{r}_{c}')
        w_ur = self._new_bool_var_domain_check(ur, [0, 2], f'w_ur_{r}_{c}')
        w_dl = self._new_bool_var_domain_check(dl, [0, 4], f'w_dl_{r}_{c}')
        w_dr = self._new_bool_var_domain_check(dr, [0, 3], f'w_dr_{r}_{c}')

        white_sum = sum([w_ul, w_ur, w_dl, w_dr])
        self._model.Add(white_sum != 3)

    def _new_bool_var_domain_check(self, var, allowed_values, name):
        b = self._model.NewBoolVar(name)
        # domain = cp_model.Domain.FromValues(allowed_values)
        # self._model.AddLinearExpressionInDomain(var, domain).OnlyEnforceIf(b)
        # complement = cp_model.Domain.FromValues([v for v in range(6) if v not in allowed_values])
        # self._model.AddLinearExpressionInDomain(var, complement).OnlyEnforceIf(b.Not())

        # Alternative implementation using AddAllowedAssignments on (var, b)
        table = []
        for val in range(6):
            if val in allowed_values:
                table.append((val, 1))
            else:
                table.append((val, 0))
        self._model.AddAllowedAssignments([var, b], table)
        return b
