from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class NumberLinkSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars = None
        self._previous_solution = None

    def get_solution(self) -> (Grid, int):
        self._grid_vars = Grid([[self._model.NewIntVar(0, max(self.rows_number * self.columns_number - 1, 0), f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()
        if self._previous_solution.is_empty():
            return Grid.empty()

        bool_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                prev_val = self._previous_solution.value(r, c)
                diff_var = self._model.NewBoolVar(f"diff_r{r}_c{c}")
                self._model.Add(self._grid_vars[Position(r, c)] != prev_val).OnlyEnforceIf(diff_var)
                self._model.Add(self._grid_vars[Position(r, c)] == prev_val).OnlyEnforceIf(diff_var.Not())
                bool_vars.append(diff_var)

        self._model.AddBoolOr(bool_vars)

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        return Grid([[solver.Value(self._grid_vars.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_neighbors_count_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid:
            if value >= 0:
                self._model.Add(self._grid_vars[position] == value)
            else:
                self._model.Add(self._grid_vars[position] >= 0)

    def _add_neighbors_count_constraints(self):
        for position, position_value in self._grid:
            same_value_neighbors = []
            for neighbor_position in self._grid.neighbors_positions(position):
                same_value = self._model.NewBoolVar(f"same_value_{position.r}_{position.c}_{neighbor_position.r}_{neighbor_position.c}")
                self._model.Add(self._grid_vars[position] == self._grid_vars[neighbor_position]).OnlyEnforceIf(same_value)
                self._model.Add(self._grid_vars[position] != self._grid_vars[neighbor_position]).OnlyEnforceIf(same_value.Not())
                same_value_neighbors.append(same_value)

            if position_value >= 0:
                self._model.Add(sum(same_value_neighbors) == 1)
            else:
                self._model.Add(sum(same_value_neighbors) == 2)
