from z3 import Solver, Not, And, unsat, If, Bool, is_true

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class NumberCrossSolver(GameSolver):
    black_value = False  # must stay False
    empty = None  # must stay None

    def __init__(self, input_grid: Grid, row_sums_clues: list, column_sums_clues: list):
        self._input_grid = input_grid
        if self._input_grid.rows_number != self._input_grid.columns_number:
            raise ValueError("The grid must be square")
        self.rows_number = self._input_grid.rows_number
        self.columns_number = self._input_grid.columns_number
        self._row_sums_clues = row_sums_clues
        self._column_sums_clues = column_sums_clues
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Bool(f"cell_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution if value == self.black_value])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self):
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid(
            [[self._input_grid[Position(i, j)] if is_true(model.eval(self._grid_z3[Position(i, j)])) else self.black_value for j in range(self.columns_number)]
             for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_initials_constraints()
        self._add_sums_clues_constraints()

    def _add_initials_constraints(self):
        for position, value in self._input_grid:
            if value == self.black_value:
                pass  # todo

    def _add_sums_clues_constraints(self):
        self._add_constraints_for_clues(self._row_sums_clues, self._row_positions_generator)
        self._add_constraints_for_clues(self._column_sums_clues, self._column_positions_generator)

    def _add_constraints_for_clues(self, line_sum_clues: list, position_generator):
        for index, sum_clue in enumerate(line_sum_clues):
            if sum_clue != self.empty:
                line_positions = position_generator(index)
                self._add_sum_for_line_constraint(line_positions, sum_clue)

    def _row_positions_generator(self, row_index: int) -> list:
        return [Position(row_index, c) for c in range(self.columns_number)]

    def _column_positions_generator(self, column_index: int) -> list:
        return [Position(r, column_index) for r in range(self.rows_number)]

    def _add_sum_for_line_constraint(self, line_positions: list, clue: int):
        pass  # todo
