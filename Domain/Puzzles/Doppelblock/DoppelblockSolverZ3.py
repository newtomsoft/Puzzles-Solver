from z3 import Solver, Not, And, unsat, Int, If, Distinct

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class DoppelblockSolver(GameSolver):
    empty = None
    black_value = 0 # must stay 0

    def __init__(self, grid: Grid, row_sums_clues: list, column_sums_clues: list):
        self._grid = grid
        if self._grid.rows_number != self._grid.columns_number:
            raise ValueError("The grid must be square")
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._row_sums_clues = row_sums_clues
        self._column_sums_clues = column_sums_clues
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"cell_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self):
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._grid_z3[Position(i, j)]).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_initials_constraints()
        self._add_two_black_cells_and_distincts_numbers_constraints()
        self._add_sums_clues_constraints()

    def _add_initials_constraints(self):
        for position, value in self._grid:
            if value != self.empty:
                self._solver.add(self._grid_z3[position] == value)
            else:
                self._solver.add(self._grid_z3[position] >= 0, self._grid_z3[position] <= self.rows_number - 2)

    def _add_two_black_cells_and_distincts_numbers_constraints(self):
        for r in range(self.rows_number):
            row_vars = [self._grid_z3[Position(r, c)] for c in range(self.columns_number)]
            self._solver.add(sum((cell == self.black_value for cell in row_vars)) == 2)

            non_zero_vars = []
            for c in range(self.columns_number):
                non_zero_var = If(row_vars[c] != self.black_value, row_vars[c], -c - 1)
                non_zero_vars.append(non_zero_var)
            self._solver.add(Distinct(non_zero_vars))

        for c in range(self.columns_number):
            col_vars = [self._grid_z3[Position(r, c)] for r in range(self.rows_number)]
            self._solver.add(sum((cell == self.black_value for cell in col_vars)) == 2)

            non_zero_vars = []
            for r in range(self.rows_number):
                non_zero_var = If(col_vars[r] != 0, col_vars[r], -r - 1)
                non_zero_vars.append(non_zero_var)
            self._solver.add(Distinct(non_zero_vars))

    def _add_sums_clues_constraints(self):
        for r, clue in enumerate(self._row_sums_clues):
            if clue != self.empty:
                row_vars = [self._grid_z3[Position(r, c)] for c in range(self.columns_number)]
                self._add_sum_for_line_constraint(row_vars, clue)

        for c, clue in enumerate(self._column_sums_clues):
            if clue != self.empty:
                col_vars = [self._grid_z3[Position(r, c)] for r in range(self.rows_number)]
                self._add_sum_for_line_constraint(col_vars, clue)

    def _add_sum_for_line_constraint(self, line_vars: list, clue: int):
        sum_terms = self._calculate_between_pairs_sums(line_vars)
        self._solver.add(sum(sum_terms) == clue)

    def _calculate_between_pairs_sums(self, line_vars: list) -> list:
        sum_terms = []
        line_length = len(line_vars)

        for i in range(line_length):
            for j in range(i + 1, line_length):
                is_pair_black = And(line_vars[i] == self.black_value, line_vars[j] == self.black_value)
                between_pair_sum = sum(line_vars[k] for k in range(i + 1, j))
                sum_terms.append(If(is_pair_black, between_pair_sum, 0))

        return sum_terms
