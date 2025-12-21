from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class NorinoriSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number

        # Match test expectations
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")

        if self.rows_number < 6:
            raise ValueError("The grid must be at least 6x6")

        self._regions = self._grid.get_regions()

        if len(self._regions) < 2:
            raise ValueError("The grid must have at least 2 regions")

        self._model = None
        self._solver = cp_model.CpSolver()
        self._grid_vars = None
        self._status = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._grid_vars = [[self._model.NewBoolVar(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()

        self._status = self._solver.Solve(self._model)

        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        return self._compute_solution()

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

    def _compute_solution(self) -> Grid:
        grid = Grid([[1 if self._solver.Value(self._grid_vars[i][j]) else 0 for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def queen(self, position):
        return self._grid_vars[position.r][position.c]

    def _add_constraints(self):
        self._add_constraint_dominoes()
        self._add_constraint_regions()

    def _add_constraint_dominoes(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                p = Position(r, c)
                neighbors = self._grid.neighbors_positions(p)
                neighbor_vars = [self.queen(n) for n in neighbors]
                self._model.Add(sum(neighbor_vars) == 1).OnlyEnforceIf(self.queen(p))

    def _add_constraint_regions(self):
        for region in self._regions.values():
            self._model.Add(sum([self.queen(position) for position in region]) == 2)
