from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class ArukoneNo2x2Solver(GameSolver):
    cell_empty = -1

    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars = None
        self._previous_solution = None

    def get_solution(self) -> Grid:
        self._grid_vars = Grid(
            [[self._model.new_int_var(0, max(self.rows_number * self.columns_number - 1, 0), f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
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
                diff_var = self._model.new_bool_var(f"diff_r{r}_c{c}")
                self._model.add(self._grid_vars[Position(r, c)] != prev_val).only_enforce_if(diff_var)
                self._model.add(self._grid_vars[Position(r, c)] == prev_val).only_enforce_if(diff_var.negated())
                bool_vars.append(diff_var)

        self._model.add_bool_or(bool_vars)

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        status = solver.solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        return Grid([[solver.value(self._grid_vars.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_neighbors_count_constraints()
        self._add_no_2x2_same_value_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid:
            if value >= 0:
                self._model.add(self._grid_vars[position] == value)
            else:
                self._model.add(self._grid_vars[position] >= 0)

    def _add_neighbors_count_constraints(self):
        for position, position_value in self._grid:
            same_value_neighbors = []
            for neighbor_position in self._grid.neighbors_positions(position):
                same_value = self._model.new_bool_var(f"same_value_{position.r}_{position.c}_{neighbor_position.r}_{neighbor_position.c}")
                self._model.add(self._grid_vars[position] == self._grid_vars[neighbor_position]).only_enforce_if(same_value)
                self._model.add(self._grid_vars[position] != self._grid_vars[neighbor_position]).only_enforce_if(same_value.negated())
                same_value_neighbors.append(same_value)

            if any(v >= 0 for v in self._grid.neighbors_values(position)):
                if position_value >= 0:
                    self._model.add(sum(same_value_neighbors) >= 1)
                    self._model.add(sum(same_value_neighbors) <= 2)
                else:
                    self._model.add(sum(same_value_neighbors) >= 2)
                    self._model.add(sum(same_value_neighbors) <= 3)
            else:
                if position_value >= 0:
                    self._model.add(sum(same_value_neighbors) == 1)
                else:
                    self._model.add(sum(same_value_neighbors) == 2)

    def _add_no_2x2_same_value_constraints(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                vars_2x2 = [
                    self._grid_vars[Position(r, c)],
                    self._grid_vars[Position(r + 1, c)],
                    self._grid_vars[Position(r, c + 1)],
                    self._grid_vars[Position(r + 1, c + 1)]
                ]

                is_same_01 = self._model.new_bool_var(f"same_2x2_{r}_{c}_01")
                is_same_12 = self._model.new_bool_var(f"same_2x2_{r}_{c}_12")
                is_same_23 = self._model.new_bool_var(f"same_2x2_{r}_{c}_23")
                
                self._model.add(vars_2x2[0] == vars_2x2[1]).only_enforce_if(is_same_01)
                self._model.add(vars_2x2[0] != vars_2x2[1]).only_enforce_if(is_same_01.negated())
                
                self._model.add(vars_2x2[1] == vars_2x2[2]).only_enforce_if(is_same_12)
                self._model.add(vars_2x2[1] != vars_2x2[2]).only_enforce_if(is_same_12.negated())
                
                self._model.add(vars_2x2[2] == vars_2x2[3]).only_enforce_if(is_same_23)
                self._model.add(vars_2x2[2] != vars_2x2[3]).only_enforce_if(is_same_23.negated())
                
                self._model.add_bool_or([is_same_01.negated(), is_same_12.negated(), is_same_23.negated()])