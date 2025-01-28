from z3 import Bool, Solver, Implies, Not, And, Or, sat, is_true, Sum

from Utils.Grid import Grid


class HitoriGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self._solver = None
        self._grid_z3 = None
        self._is_print_dot = False
        self._last_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._solver = Solver()
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._solver is None:
            self._init_solver()

        solution, _ = self._ensure_all_white_connected()
        self._last_solution = solution
        return solution

    def _ensure_all_white_connected(self):
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self._grid.columns_number)] for i in range(self._grid.rows_number)])
            wrong_blacks_sets = current_grid.find_all_min_2_connected_cells_touch_border(False, 'diagonal')

            if len(wrong_blacks_sets) == 0:
                return self.get_solution_grid(current_grid), proposition_count

            if self._is_print_dot:
                self.print_dot(proposition_count)

            for wrong_blacks in wrong_blacks_sets:
                proposition_constraints = [Not(self._grid_z3.value(r, c)) for r, c in wrong_blacks]
                self._solver.add(Not(And(proposition_constraints)))

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for position, _ in [(position, value) for (position, value) in self._last_solution if not value]:
            previous_solution_constraints.append(Not(self._grid_z3[position]))
        self._solver.add(Not(And(previous_solution_constraints)))

        return self.get_solution()

    def _add_constraints(self):
        self._if_unique_in_row_and_column_then_white()
        self._if_n_same_number_in_row_or_column_then_black_for_n_minus_1()
        self._white_for_same_number_in_row_and_column_implies_black()
        self._black_implies_von_neumann_withe()
        self._if_sandwiched_by_2_same_number_then_white()
        self._if_2_same_number_contigus_then_others_black()
        self._if_3_same_number_in_corner_then_black_corner()
        self._black_x_black_on_border_implies_white_white()
        self._if_4_same_number_in_square_then_black_in_diagonal()
        self._3_black_in_von_neumann_implies_last_white()
        self._diagonal_black_implies_1_white()
        self._pyramid_black_on_border_implies_top_white()
        self._if_2_same_number_near_corner_then_white()

    def _black_implies_von_neumann_withe(self):
        constraints = []
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                if r > 0:
                    constraints.append(Implies(Not(self._grid_z3.value(r, c)), self._grid_z3.value(r - 1, c)))
                if r < self._grid.rows_number - 1:
                    constraints.append(Implies(Not(self._grid_z3.value(r, c)), self._grid_z3.value(r + 1, c)))
                if c > 0:
                    constraints.append(Implies(Not(self._grid_z3.value(r, c)), self._grid_z3.value(r, c - 1)))
                if c < self._grid.columns_number - 1:
                    constraints.append(Implies(Not(self._grid_z3.value(r, c)), self._grid_z3.value(r, c + 1)))
                self._solver.add(constraints)

    def _if_n_same_number_in_row_or_column_then_black_for_n_minus_1(self):
        constraints = []
        for r0 in range(self._grid.rows_number):
            for c0 in range(self._grid.columns_number):
                r1selected = []
                for r1 in range(self._grid.rows_number):
                    if self._grid.value(r0, c0) == self._grid.value(r1, c0) and r1 != r0:
                        r1selected.append(r1)
                constraints.append(Sum([Not(self._grid_z3.value(r, c0)) for r in r1selected]) >= len(r1selected) - 1)
                c1selected = []
                for c1 in range(self._grid.columns_number):
                    if self._grid.value(r0, c0) == self._grid.value(r0, c1) and c1 != c0:
                        c1selected.append(c1)
                constraints.append(Sum([Not(self._grid_z3.value(r0, c)) for c in c1selected]) >= len(c1selected) - 1)
        self._solver.add(constraints)

    def _if_unique_in_row_and_column_then_white(self):
        constraints = []
        for r0 in range(self._grid.rows_number):
            for c0 in range(self._grid.columns_number):
                unique_in_row = all(self._grid.value(r0, c0) != self._grid.value(r0, c1) for c1 in range(self._grid.columns_number) if c1 != c0)
                unique_in_column = all(self._grid.value(r0, c0) != self._grid.value(r1, c0) for r1 in range(self._grid.rows_number) if r1 != r0)
                if unique_in_row and unique_in_column:
                    constraints.append(self._grid_z3.value(r0, c0))
        self._solver.add(constraints)

    def _white_for_same_number_in_row_and_column_implies_black(self):
        constraints = []
        for r0 in range(self._grid.rows_number):
            for c0 in range(self._grid.columns_number):
                for r1 in range(self._grid.rows_number):
                    if self._grid.value(r0, c0) == self._grid.value(r1, c0) and r1 != r0:
                        constraints.append(Implies(self._grid_z3.value(r0, c0), Not(self._grid_z3.value(r1, c0))))
                for c1 in range(self._grid.columns_number):
                    if self._grid.value(r0, c0) == self._grid.value(r0, c1) and c1 != c0:
                        constraints.append(Implies(self._grid_z3.value(r0, c0), Not(self._grid_z3.value(r0, c1))))
        self._solver.add(constraints)

    def _if_2_same_number_contigus_then_others_black(self):
        constraints = []
        for r in range(self._grid.rows_number - 1):
            for c in range(self._grid.columns_number):
                current_number = self._grid.value(r, c)
                if self._grid.value(r + 1, c) == current_number:
                    for r1 in range(self._grid.rows_number):
                        if r1 != r and r1 != r + 1 and self._grid.value(r1, c) == current_number:
                            constraints.append(Not(self._grid_z3.value(r1, c)))
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number - 1):
                current_number = self._grid.value(r, c)
                if self._grid.value(r, c + 1) == current_number:
                    for c1 in range(self._grid.rows_number):
                        if c1 != c and c1 != c + 1 and self._grid.value(r, c1) == current_number:
                            constraints.append(Not(self._grid_z3.value(r, c1)))
        self._solver.add(constraints)

    def _if_sandwiched_by_2_same_number_then_white(self):
        constraints = []
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                if 0 < r < self._grid.rows_number - 1 and self._grid.value(r - 1, c) == self._grid.value(r + 1, c):
                    constraints.append(self._grid_z3.value(r, c))
                if 0 < c < self._grid.columns_number - 1 and self._grid.value(r, c - 1) == self._grid.value(r, c + 1):
                    constraints.append(self._grid_z3.value(r, c))
        self._solver.add(constraints)

    def _if_3_same_number_in_corner_then_black_corner(self):
        constraints = [
            Not(self._grid_z3.value(0, 0)) if self._grid.value(0, 0) == self._grid.value(0, 1) == self._grid.value(1, 0) else True,
            Not(self._grid_z3.value(0, self._grid.columns_number - 1)) if self._grid.value(0, self._grid.columns_number - 1) == self._grid.value(0, self._grid.columns_number - 2) == self._grid.value(
                1, self._grid.columns_number - 1) else True,
            Not(self._grid_z3.value(self._grid.rows_number - 1, 0)) if self._grid.value(self._grid.rows_number - 1, 0) == self._grid.value(self._grid.rows_number - 1, 1) == self._grid.value(
                self._grid.rows_number - 2, 0) else True,
            Not(self._grid_z3.value(self._grid.rows_number - 1, self._grid.columns_number - 1)) if self._grid.value(self._grid.rows_number - 1, self._grid.columns_number - 1) == self._grid.value(
                self._grid.rows_number - 2,
                self._grid.columns_number - 1) == self._grid.value(
                self._grid.rows_number - 1, self._grid.columns_number - 2) else True
        ]
        self._solver.add(constraints)

    def _if_4_same_number_in_square_then_black_in_diagonal(self):
        square_same_number = []
        for r in range(self._grid.rows_number - 1):
            for c in range(self._grid.columns_number - 1):
                if self._grid.value(r, c) == self._grid.value(r + 1, c) == self._grid.value(r, c + 1) == self._grid.value(r + 1, c + 1):
                    Or(
                        And(Not(self._grid_z3.value(r, c)), self._grid_z3.value(r + 1, c), self._grid_z3.value(r, c + 1), Not(self._grid_z3.value(r + 1, c + 1))),
                        And(self._grid_z3.value(r, c), Not(self._grid_z3.value(r + 1, c)), Not(self._grid_z3.value(r, c + 1)), self._grid_z3.value(r + 1, c + 1)),
                    )
        self._solver.add(square_same_number)

    def _black_x_black_on_border_implies_white_white(self):
        constraints = []
        last_row = self._grid.rows_number - 1
        last_column = self._grid.columns_number - 1
        for c in range(self._grid.columns_number - 2):
            constraints.append(Implies(And(Not(self._grid_z3.value(0, c)), Not(self._grid_z3.value(0, c + 2))), self._grid_z3.value(0, c + 1)))
            constraints.append(Implies(And(Not(self._grid_z3.value(last_row, c)), Not(self._grid_z3.value(last_row, c + 2))), self._grid_z3.value(last_row, c + 1)))
        for r in range(self._grid.rows_number - 2):
            constraints.append(Implies(And(Not(self._grid_z3.value(r, 0)), Not(self._grid_z3.value(r + 2, 0))), self._grid_z3.value(r + 1, 0)))
            constraints.append(Implies(And(Not(self._grid_z3.value(r, last_column)), Not(self._grid_z3.value(r + 2, last_column))), self._grid_z3.value(r + 1, last_column)))
        self._solver.add(constraints)

    def _3_black_in_von_neumann_implies_last_white(self):
        constraints = []
        for r in range(1, self._grid.rows_number - 1):
            for c in range(1, self._grid.columns_number - 1):
                constraints.append(Implies(And(Not(self._grid_z3.value(r, c - 1)), Not(self._grid_z3.value(r - 1, c)), Not(self._grid_z3.value(r, c + 1))), self._grid_z3.value(r + 1, c)))
                constraints.append(Implies(And(Not(self._grid_z3.value(r - 1, c)), Not(self._grid_z3.value(r, c + 1)), Not(self._grid_z3.value(r + 1, c))), self._grid_z3.value(r, c - 1)))
                constraints.append(Implies(And(Not(self._grid_z3.value(r, c + 1)), Not(self._grid_z3.value(r + 1, c)), Not(self._grid_z3.value(r, c - 1))), self._grid_z3.value(r - 1, c)))
                constraints.append(Implies(And(Not(self._grid_z3.value(r + 1, c)), Not(self._grid_z3.value(r, c - 1)), Not(self._grid_z3.value(r - 1, c))), self._grid_z3.value(r, c + 1)))
        self._solver.add(constraints)

    def _diagonal_black_implies_1_white(self):
        constraints = []
        min_rows_column_number = min(self._grid.rows_number, self._grid.columns_number)
        for diagonal_len in range(2, min_rows_column_number - 1):
            if self._grid.rows_number == self._grid.columns_number >= diagonal_len:
                constraints.append(Sum([self._grid_z3.value(diagonal_len - 1 - x, x) for x in range(diagonal_len - 1)]) < diagonal_len)
                constraints.append(Sum([self._grid_z3.value(diagonal_len - 1 - x, self._grid.columns_number - 1 - x) for x in range(diagonal_len - 1)]) < diagonal_len)
                constraints.append(Sum([self._grid_z3.value(self._grid.rows_number - diagonal_len + x, x) for x in range(diagonal_len - 1)]) < diagonal_len)
                constraints.append(Sum([self._grid_z3.value(self._grid.rows_number - diagonal_len + x, self._grid.columns_number - 1 - x) for x in range(diagonal_len - 1)]) < diagonal_len)

        self._solver.add(constraints)

    def _if_2_same_number_near_corner_then_white(self):
        self._if_2_same_number_near_corner_touch_border_then_white()
        self._if_2_same_number_near_corner_near_border_then_white()

    def _if_2_same_number_near_corner_touch_border_then_white(self):
        constraints = []
        if self._grid.value(0, 0) == self._grid.value(0, 1):
            constraints.append(self._grid_z3.value(1, 0))
        if self._grid.value(0, 0) == self._grid.value(1, 0):
            constraints.append(self._grid_z3.value(0, 1))
        if self._grid.value(0, self._grid.columns_number - 1) == self._grid.value(0, self._grid.columns_number - 2):
            constraints.append(self._grid_z3.value(1, self._grid.columns_number - 1))
        if self._grid.value(0, self._grid.columns_number - 1) == self._grid.value(1, self._grid.columns_number - 1):
            constraints.append(self._grid_z3.value(0, self._grid.columns_number - 2))
        if self._grid.value(self._grid.rows_number - 1, 0) == self._grid.value(self._grid.rows_number - 1, 1):
            constraints.append(self._grid_z3.value(self._grid.rows_number - 2, 0))
        if self._grid.value(self._grid.rows_number - 1, 0) == self._grid.value(self._grid.rows_number - 2, 0):
            constraints.append(self._grid_z3.value(self._grid.rows_number - 1, 1))
        if self._grid.value(self._grid.rows_number - 1, self._grid.columns_number - 1) == self._grid.value(self._grid.rows_number - 1, self._grid.columns_number - 2):
            constraints.append(self._grid_z3.value(self._grid.rows_number - 2, self._grid.columns_number - 1))
        if self._grid.value(self._grid.rows_number - 1, self._grid.columns_number - 1) == self._grid.value(self._grid.rows_number - 2, self._grid.columns_number - 1):
            constraints.append(self._grid_z3.value(self._grid.rows_number - 1, self._grid.columns_number - 2))
        self._solver.add(constraints)

    def _if_2_same_number_near_corner_near_border_then_white(self):
        constraints = []
        if self._grid.value(1, 0) == self._grid.value(1, 1):
            constraints.append(self._grid_z3.value(0, 1))
        if self._grid.value(0, 1) == self._grid.value(1, 1):
            constraints.append(self._grid_z3.value(1, 0))
        if self._grid.value(1, self._grid.columns_number - 1) == self._grid.value(1, self._grid.columns_number - 2):
            constraints.append(self._grid_z3.value(0, self._grid.columns_number - 2))
        if self._grid.value(0, self._grid.columns_number - 2) == self._grid.value(1, self._grid.columns_number - 2):
            constraints.append(self._grid_z3.value(1, self._grid.columns_number - 1))
        if self._grid.value(self._grid.rows_number - 2, 0) == self._grid.value(self._grid.rows_number - 2, 1):
            constraints.append(self._grid_z3.value(self._grid.rows_number - 1, 1))
        if self._grid.value(self._grid.rows_number - 1, 1) == self._grid.value(self._grid.rows_number - 2, 1):
            constraints.append(self._grid_z3.value(self._grid.rows_number - 2, 0))
        if self._grid.value(self._grid.rows_number - 2, self._grid.columns_number - 1) == self._grid.value(self._grid.rows_number - 2, self._grid.columns_number - 2):
            constraints.append(self._grid_z3.value(self._grid.rows_number - 1, self._grid.columns_number - 2))
        if self._grid.value(self._grid.rows_number - 1, self._grid.columns_number - 2) == self._grid.value(self._grid.rows_number - 2, self._grid.columns_number - 2):
            constraints.append(self._grid_z3.value(self._grid.rows_number - 2, self._grid.columns_number - 1))
        self._solver.add(constraints)

    def _pyramid_black_on_border_implies_top_white(self):
        self._2_levels_pyramid_black_on_border_implies_top_white()
        self._3_levels_pyramid_black_on_border_implies_top_white()

    def _2_levels_pyramid_black_on_border_implies_top_white(self):
        constraints = []
        for r in range(1, self._grid.rows_number - 3):
            for c, dc in {(0, 1), (self._grid.columns_number - 1, -1)}:
                constraints.append(Implies(And(Not(self._grid_z3.value(r, c)), Not(self._grid_z3.value(r + 2, c))), self._grid_z3.value(r + 1, c + dc)))
        for c in range(1, self._grid.columns_number - 3):
            for r, dr in {(0, 1), (self._grid.rows_number - 1, -1)}:
                constraints.append(Implies(And(Not(self._grid_z3.value(r, c)), Not(self._grid_z3.value(r, c + 2))), self._grid_z3.value(r + dr, c + 1)))
        self._solver.add(constraints)

    def _3_levels_pyramid_black_on_border_implies_top_white(self):
        constraints = []
        for r in range(1, self._grid.rows_number - 4):
            for c, dc in {(0, 1), (self._grid.columns_number - 1, -1)}:
                constraints.append(Implies(And(Not(self._grid_z3.value(r, c)), Not(self._grid_z3.value(r + 4, c)), Not(self._grid_z3.value(r + 1, c + dc)), Not(self._grid_z3.value(r + 3, c + dc))),
                                           self._grid_z3.value(r + 2, c + 2 * dc)))
        for c in range(1, self._grid.columns_number - 4):
            for r, dr in {(0, 1), (self._grid.rows_number - 1, -1)}:
                constraints.append(Implies(And(Not(self._grid_z3.value(r, c)), Not(self._grid_z3.value(r, c + 4)), Not(self._grid_z3.value(r + dr, c + 1)), Not(self._grid_z3.value(r + dr, c + 3))),
                                           self._grid_z3.value(r + 2 * dr, c + 2)))
        self._solver.add(constraints)

    def print_proposition(self, proposition_grid: Grid):
        print("\n".join(" ".join(f'{self._grid.value(r, c)}' if proposition_grid.value(r, c) else "■" for c in range(self._grid.columns_number)) for r in range(self._grid.rows_number)))

    def get_solution_grid(self, proposition_grid: Grid):
        return Grid([[self._grid.value(r, c) if proposition_grid.value(r, c) else False for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])

    @staticmethod
    def print_dot(proposition_count):
        print('.', end='')
        if proposition_count % 100 == 0:
            print()
