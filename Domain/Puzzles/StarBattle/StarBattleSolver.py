from ortools.sat.python import cp_model

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
        self._model = None
        self._solver = cp_model.CpSolver()
        self._grid_vars = None
        self._status = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._grid_vars = [[self._model.NewBoolVar(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()

    def get_solution(self) -> Grid | None:
        if self._model is None:
            self._init_model()

        self._status = self._solver.Solve(self._model)

        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return None

        grid = Grid([[self._solver.Value(self._grid_vars[i][j]) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def get_other_solution(self) -> Grid:
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return self.get_solution()

        current_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                var = self._grid_vars[r][c]
                if self._solver.BooleanValue(var):
                    current_vars.append(var.Not())
                else:
                    current_vars.append(var)
        self._model.AddBoolOr(current_vars)

        self._status = self._solver.Solve(self._model)

        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        return self._compute_solution()

    def _compute_solution(self):
         return Grid([[self._solver.Value(self._grid_vars[i][j]) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def queen(self, position):
        return self._grid_vars[position.r][position.c]

    def _add_constraints(self):
        self._add_constraint_queen_by_row()
        self._add_constraint_queen_by_column()
        self._add_constraint_queen_by_region()
        self._add_constraint_no_adjacent_queen()

    def _add_constraint_queen_by_row(self):
        for r in range(self.rows_number):
            self._model.Add(sum([self.queen(Position(r, c)) for c in range(self.columns_number)]) == self._stars_count_by_region_column_row)

    def _add_constraint_queen_by_column(self):
        for c in range(self.columns_number):
            self._model.Add(sum([self.queen(Position(r, c)) for r in range(self.rows_number)]) == self._stars_count_by_region_column_row)

    def _add_constraint_queen_by_region(self):
        for region in self._regions.values():
            self._model.Add(sum([self.queen(position) for position in region]) == self._stars_count_by_region_column_row)

    def _add_constraint_no_adjacent_queen(self):
        for position, _ in self._grid:
            neighbors = self._grid.neighbors_positions(position, "diagonal")
            for neighbor in neighbors:
                self._model.AddBoolOr([self.queen(position).Not(), self.queen(neighbor).Not()])
