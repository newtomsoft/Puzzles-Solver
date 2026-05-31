from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class DosunFuwariSolver(GameSolver):
    cell_empty = 0
    black = 1
    white = 2
    wall = empty

    def __init__(self, region_grid: Grid):
        self._region_grid = region_grid
        self._positions_by_region = region_grid.get_regions()
        self.rows_number = self._region_grid.rows_number
        self.columns_number = self._region_grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[self._model.new_int_var(0, 2, f"cell_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        eq_vars = []
        for position, value in self._previous_solution:
            b = self._model.new_bool_var(f"block_{position.r}_{position.c}")
            self._model.Add(self._grid_z3[position] == value).OnlyEnforceIf(b)
            self._model.Add(self._grid_z3[position] != value).OnlyEnforceIf(b.Not())
            eq_vars.append(b)
        self._model.Add(sum(eq_vars) <= len(eq_vars) - 1)
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self):
        status = self._solver.Solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()
        grid = Grid([[self._solver.Value(self._grid_z3[Position(i, j)]) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_initials_constraints()
        self._add_count_constraints()
        self._add_gravity_constraints()

    def _add_initials_constraints(self):
        for position, value in self._region_grid:
            if value == self.wall:
                self._model.Add(self._grid_z3[position] == self.empty)
                continue
            self._model.Add(self._grid_z3[position] >= self.empty)
            self._model.Add(self._grid_z3[position] <= self.white)

    def _add_count_constraints(self):
        for positions in [positions for region_id, positions in self._positions_by_region.items() if region_id != self.wall]:
            black_bools = []
            for position in positions:
                b = self._model.new_bool_var(f"black_{position.r}_{position.c}")
                self._model.Add(self._grid_z3[position] == self.black).OnlyEnforceIf(b)
                self._model.Add(self._grid_z3[position] != self.black).OnlyEnforceIf(b.Not())
                black_bools.append(b)
            self._model.Add(sum(black_bools) == 1)

            white_bools = []
            for position in positions:
                b = self._model.new_bool_var(f"white_{position.r}_{position.c}")
                self._model.Add(self._grid_z3[position] == self.white).OnlyEnforceIf(b)
                self._model.Add(self._grid_z3[position] != self.white).OnlyEnforceIf(b.Not())
                white_bools.append(b)
            self._model.Add(sum(white_bools) == 1)

    def _add_gravity_constraints(self):
        for position in [position for position, value in self._region_grid if value != self.wall]:
            is_black = self._model.new_bool_var(f"is_black_{position.r}_{position.c}")
            self._model.Add(self._grid_z3[position] == self.black).OnlyEnforceIf(is_black)
            self._model.Add(self._grid_z3[position] != self.black).OnlyEnforceIf(is_black.Not())

            no_down = self._grid_z3.is_position_in_edge_down(position)
            down_wall = not no_down and self._region_grid[position.down] == self.wall
            if not no_down and not down_wall:
                is_down_black = self._model.new_bool_var(f"is_down_black_{position.r}_{position.c}")
                self._model.Add(self._grid_z3[position.down] == self.black).OnlyEnforceIf(is_down_black)
                self._model.Add(self._grid_z3[position.down] != self.black).OnlyEnforceIf(is_down_black.Not())
                self._model.AddImplication(is_black, is_down_black)

            is_white = self._model.new_bool_var(f"is_white_{position.r}_{position.c}")
            self._model.Add(self._grid_z3[position] == self.white).OnlyEnforceIf(is_white)
            self._model.Add(self._grid_z3[position] != self.white).OnlyEnforceIf(is_white.Not())

            no_up = self._grid_z3.is_position_in_edge_up(position)
            up_wall = not no_up and self._region_grid[position.up] == self.wall
            if not no_up and not up_wall:
                is_up_white = self._model.new_bool_var(f"is_up_white_{position.r}_{position.c}")
                self._model.Add(self._grid_z3[position.up] == self.white).OnlyEnforceIf(is_up_white)
                self._model.Add(self._grid_z3[position.up] != self.white).OnlyEnforceIf(is_up_white.Not())
                self._model.AddImplication(is_white, is_up_white)

            if not self._grid_z3.is_position_in_edge_down(position):
                is_down_white = self._model.new_bool_var(f"is_down_white_{position.r}_{position.c}")
                self._model.Add(self._grid_z3[position.down] == self.white).OnlyEnforceIf(is_down_white)
                self._model.Add(self._grid_z3[position.down] != self.white).OnlyEnforceIf(is_down_white.Not())
                self._model.AddBoolOr([is_black.Not(), is_down_white.Not()])
