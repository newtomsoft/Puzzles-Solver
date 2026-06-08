from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class NorinoriSolver(GameSolver):
    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number

        self._regions = self._grid.get_regions()

        if len(self._regions) == 0:
            raise ValueError("The grid must have at least one region")

        self._model = None
        self._grid_vars = None
        self._status = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._grid_vars = [[self._model.new_bool_var(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()

        self._solver.parameters.max_time_in_seconds = 10.0
        self._status = self._solver.solve(self._model)

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
                if self._solver.boolean_value(var):
                    current_vars.append(var.negated())
                else:
                    current_vars.append(var)
        self._model.add_bool_or(current_vars)

        self._status = self._solver.solve(self._model)

        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        grid = Grid([[self._solver.boolean_value(self._grid_vars[i][j]) for j in range(self.columns_number)] for i in range(self.rows_number)])
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
                self._model.add(sum(neighbor_vars) == 1).only_enforce_if(self.queen(p))

    def _add_constraint_regions(self):
        for region in self._regions.values():
            self._model.add(sum([self.queen(position) for position in region]) == 2)
