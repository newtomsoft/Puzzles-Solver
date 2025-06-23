from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class TilePaintSolver(GameSolver):
    def __init__(self, grid: Grid, row_sums: list[int], column_sums: list[int]):
        self._grid = grid
        self.row_sums = row_sums
        self._column_sums = column_sums
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        self._tiles = self._grid.get_regions()
        if len(self._tiles) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = None
        self._previous_solution = None

    def get_solution(self) -> tuple[Grid, dict[int, frozenset[Position]]]:
        self._grid_vars = Grid([[self._model.NewBoolVar(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution, self._tiles

    def get_other_solution(self) -> tuple[Grid, dict[int, frozenset[Position]]]:
        previous_solution_literals = []
        for position, value in self._previous_solution:
            temp_var = self._model.NewBoolVar(f"prev_{position.r}_{position.c}")
            self._model.Add(self._grid_vars[position] == value).OnlyEnforceIf(temp_var)
            self._model.Add(self._grid_vars[position] != value).OnlyEnforceIf(temp_var.Not())
            previous_solution_literals.append(temp_var)

        if previous_solution_literals:
            self._model.AddBoolOr([lit.Not() for lit in previous_solution_literals])

        self._previous_solution = self._compute_solution()
        return self._previous_solution, self._tiles

    def _compute_solution(self) -> Grid :
        status = self._solver.Solve(self._model)
        if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
            return Grid.empty()

        grid = Grid([[self._solver.Value(self._grid_vars[Position(i, j)]) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_sum_constraints()
        self._add_tiles_constraints()

    def _add_sum_constraints(self):
        for i, row in enumerate(self._grid_vars.matrix):
            if self.row_sums[i] == -1:
                continue
            self._model.Add(sum(row) == self.row_sums[i])

        for i in range(self.columns_number):
            if self._column_sums[i] == -1:
                continue
            column_vars = [self._grid_vars[Position(r, i)] for r in range(self.rows_number)]
            self._model.Add(sum(column_vars) == self._column_sums[i])

    def _add_tiles_constraints(self):
        for positions in self._tiles.values():
            positions_list = list(positions)
            first_position = positions_list[0]
            for position in positions_list[1:]:
                self._model.Add(self._grid_vars[first_position] == self._grid_vars[position])
