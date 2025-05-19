from z3 import Solver, Bool, Not, unsat, Implies, is_true, And

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class StarBattleSolver(GameSolver):
    def __init__(self, grid: Grid, stars_count_by_region_column_row: int):
        self._grid = grid
        self._stars_count_by_region_column_row = stars_count_by_region_column_row
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        self._regions = self._grid.get_regions()
        if self.rows_number != len(self._regions):
            raise ValueError("The grid must have the same number of regions as rows/column")
        if self._stars_count_by_region_column_row < 1:
            raise ValueError("The stars count by region/column/row must be at least 1")
        self._solver = Solver()
        self._grid_z3 = None

    def get_solution(self) -> Grid | None:
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        if self._solver.check() == unsat:
            return None
        model = self._solver.model()
        grid = Grid([[is_true(model.eval(self.queen(Position(i, j)))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def get_other_solution(self) -> Grid:
        raise NotImplemented("This method is not yet implemented")

    def queen(self, position):
        return self._grid_z3[position]

    def _add_constraints(self):
        self._add_constraint_queen_by_row()
        self._add_constraint_queen_by_column()
        self._add_constraint_queen_by_region()
        self._add_constraint_no_adjacent_queen()

    def _add_constraint_queen_by_row(self):
        for r in range(self.rows_number):
            self._solver.add(sum([self.queen(Position(r, c)) for c in range(self.columns_number)]) == self._stars_count_by_region_column_row)

    def _add_constraint_queen_by_column(self):
        for c in range(self.columns_number):
            self._solver.add(sum([self.queen(Position(r, c)) for r in range(self.rows_number)]) == self._stars_count_by_region_column_row)

    def _add_constraint_queen_by_region(self):
        for region in self._regions.values():
            self._solver.add(sum([self.queen(position) for position in region]) == self._stars_count_by_region_column_row)

    def _add_constraint_no_adjacent_queen(self):
        for position, _ in self._grid:
            not_neighbors_queen = And([Not(self.queen(position)) for position in self._grid.neighbors_positions(position, "diagonal")])
            self._solver.add(Implies(self.queen(position), not_neighbors_queen))
