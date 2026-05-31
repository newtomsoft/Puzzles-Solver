from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class MinesweeperMosaicSolver(GameSolver):
    cell_empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_z3 = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        if self._grid_z3 is None:
            self._init_solver()

        if self._solver.Solve(self._model) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        self._model.AddBoolOr([self._grid_z3.value(r, c).Not() if self._previous_solution.value(r, c) is True else self._grid_z3.value(r, c) for r in range(self.rows_number) for c in range(self.columns_number)])

        if self._solver.Solve(self._model) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        return self._compute_solution()

    def _compute_solution(self):
        self._previous_solution = Grid([[bool(self._solver.Value(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return self._previous_solution

    def _init_solver(self):
        self._grid_z3 = Grid([[self._model.NewBoolVar(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def _add_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == self.empty:
                    continue
                cells_in_cell_zone = []
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if 0 <= r + dr < self.rows_number and 0 <= c + dc < self.columns_number:
                            cells_in_cell_zone.append(self._grid_z3.value(r + dr, c + dc))
                self._model.Add(sum(cells_in_cell_zone) == self._grid.value(r, c))
