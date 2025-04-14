from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Puzzles.GameSolver import GameSolver


class StarBattleSolver(GameSolver):
    def __init__(self, grid: Grid, stars_count_by_region_column_row: int, solver_engine: SolverEngine):
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
        self._solver = solver_engine
        self._grid_z3 = None

    def get_solution(self) -> Grid | None:
        self._grid_z3 = Grid([[self._solver.bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        if not self._solver.has_solution():
            return None
        model = self._solver.model()
        grid = Grid([[self._solver.is_true(model.eval(self.queen(Position(i, j)))) for j in range(self.columns_number)] for i in range(self.rows_number)])
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
            self._solver.add(self._solver.sum([self.queen(Position(r, c)) for c in range(self.columns_number)]) == self._stars_count_by_region_column_row)

    def _add_constraint_queen_by_column(self):
        for c in range(self.columns_number):
            self._solver.add(self._solver.sum([self.queen(Position(r, c)) for r in range(self.rows_number)]) == self._stars_count_by_region_column_row)

    def _add_constraint_queen_by_region(self):
        for region in self._regions.values():
            self._solver.add(self._solver.sum([self.queen(position) for position in region]) == self._stars_count_by_region_column_row)

    def _add_constraint_no_adjacent_queen(self):
        for position, _ in self._grid:
            r, c = position
            if r > 0:
                self._solver.add(self._solver.Implies(self.queen(position), self._solver.Not(self.queen(position.up))))
                if c > 0:
                    self._solver.add(self._solver.Implies(self.queen(position), self._solver.Not(self.queen(position.left))))
                    self._solver.add(self._solver.Implies(self.queen(position), self._solver.Not(self.queen(position.up_left))))
                if c < self.columns_number - 1:
                    self._solver.add(self._solver.Implies(self.queen(position), self._solver.Not(self.queen(position.right))))
                    self._solver.add(self._solver.Implies(self.queen(position), self._solver.Not(self.queen(position.up_right))))

            if r < self.rows_number - 1:
                self._solver.add(self._solver.Implies(self.queen(position), self._solver.Not(self.queen(position.down))))
                if c > 0:
                    self._solver.add(self._solver.Implies(self.queen(position), self._solver.Not(self.queen(position.left))))
                    self._solver.add(self._solver.Implies(self.queen(position), self._solver.Not(self.queen(position.down_left))))
                if c < self.columns_number - 1:
                    self._solver.add(self._solver.Implies(self.queen(position), self._solver.Not(self.queen(position.right))))
                    self._solver.add(self._solver.Implies(self.queen(position), self._solver.Not(self.queen(position.down_right))))
