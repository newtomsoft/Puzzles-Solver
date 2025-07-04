from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class VectorsSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars = None
        self._previous_solution: Grid | None = None
        self._black_positions_with_region_number: dict[Position, int] = {}

    def get_solution(self) -> Grid:
        black_cell_count = [1 for position, value in self._grid if type(value) is int and value >= 0].count(1)
        self._grid_vars = [[self._model.NewIntVar(1, black_cell_count, f"grid_{r}_{c}") 
                           for c in range(self.columns_number)] 
                           for r in range(self.rows_number)]
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None or self._previous_solution.is_empty():
            return Grid.empty()

        literals = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                prev_val = self._previous_solution.value(r, c)
                not_same_val = self._model.NewBoolVar(f"cell_{r}_{c}_not_same_as_prev")
                self._model.Add(self._grid_vars[r][c] != prev_val).OnlyEnforceIf(not_same_val)
                self._model.Add(self._grid_vars[r][c] == prev_val).OnlyEnforceIf(not_same_val.Not())
                literals.append(not_same_val)
        self._model.AddBoolOr(literals)

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)

        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        return Grid([[solver.Value(self._grid_vars[r][c]) for c in range(self.columns_number)] for r in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_regions_constraints()
        self._add_regions_size_constraints()
        self._add_regions_in_1_block_constraints()

    def _add_initial_constraints(self):
        black_cell_count = [1 for position, value in self._grid if type(value) is int and value >= 0].count(1)
        region_number = 0
        for position, value in self._grid:
            if type(value) is int and value >= 0:
                region_number += 1
                self._black_positions_with_region_number[position] = region_number
                self._model.Add(self._grid_vars[position.r][position.c] == region_number)
            else:
                self._model.Add(self._grid_vars[position.r][position.c] >= 1)
                self._model.Add(self._grid_vars[position.r][position.c] <= black_cell_count)

    def _add_regions_constraints(self):
        positions_possible_region_values: dict[Position, list] = {}
        for current_position, region_number in self._black_positions_with_region_number.items():
            for position in [pos for pos in self._grid.all_orthogonal_positions(current_position) if pos not in self._black_positions_with_region_number and current_position.distance_to(pos) <= self._grid[current_position]]:
                if position not in positions_possible_region_values:
                    positions_possible_region_values[position] = []
                bool_var = self._model.NewBoolVar(f"pos_{position.r}_{position.c}_is_region_{region_number}")
                self._model.Add(self._grid_vars[position.r][position.c] == region_number).OnlyEnforceIf(bool_var)
                self._model.Add(self._grid_vars[position.r][position.c] != region_number).OnlyEnforceIf(bool_var.Not())
                positions_possible_region_values[position].append(bool_var)
        for position, possible_region_values in positions_possible_region_values.items():
            self._model.AddBoolOr(possible_region_values)

    def _add_regions_size_constraints(self):
        for position, region_number in self._black_positions_with_region_number.items():
            count_for_this_region = self._grid[position] + 1
            count_vars = []
            for r in range(self.rows_number):
                for c in range(self.columns_number):
                    is_region = self._model.NewBoolVar(f"cell_{r}_{c}_is_region_{region_number}")
                    self._model.Add(self._grid_vars[r][c] == region_number).OnlyEnforceIf(is_region)
                    self._model.Add(self._grid_vars[r][c] != region_number).OnlyEnforceIf(is_region.Not())
                    count_vars.append(is_region)
            self._model.Add(sum(count_vars) == count_for_this_region)

    def _add_regions_in_1_block_constraints(self):
        for position, region_number in self._black_positions_with_region_number.items():
            for up_position in self._grid.all_positions_up(position)[-1:0:-1]:
                up_is_region = self._model.NewBoolVar(f"up_{up_position.r}_{up_position.c}_is_region_{region_number}")
                down_is_region = self._model.NewBoolVar(f"down_{up_position.down.r}_{up_position.down.c}_is_region_{region_number}")

                self._model.Add(self._grid_vars[up_position.r][up_position.c] == region_number).OnlyEnforceIf(up_is_region)
                self._model.Add(self._grid_vars[up_position.r][up_position.c] != region_number).OnlyEnforceIf(up_is_region.Not())
                self._model.Add(self._grid_vars[up_position.down.r][up_position.down.c] == region_number).OnlyEnforceIf(down_is_region)
                self._model.Add(self._grid_vars[up_position.down.r][up_position.down.c] != region_number).OnlyEnforceIf(down_is_region.Not())

                self._model.AddBoolOr([up_is_region.Not(), down_is_region])

            for down_position in self._grid.all_positions_down(position)[-1:0:-1]:
                down_is_region = self._model.NewBoolVar(f"down_{down_position.r}_{down_position.c}_is_region_{region_number}")
                up_is_region = self._model.NewBoolVar(f"up_{down_position.up.r}_{down_position.up.c}_is_region_{region_number}")

                self._model.Add(self._grid_vars[down_position.r][down_position.c] == region_number).OnlyEnforceIf(down_is_region)
                self._model.Add(self._grid_vars[down_position.r][down_position.c] != region_number).OnlyEnforceIf(down_is_region.Not())
                self._model.Add(self._grid_vars[down_position.up.r][down_position.up.c] == region_number).OnlyEnforceIf(up_is_region)
                self._model.Add(self._grid_vars[down_position.up.r][down_position.up.c] != region_number).OnlyEnforceIf(up_is_region.Not())

                self._model.AddBoolOr([down_is_region.Not(), up_is_region])

            for left_position in self._grid.all_positions_left(position)[-1:0:-1]:
                left_is_region = self._model.NewBoolVar(f"left_{left_position.r}_{left_position.c}_is_region_{region_number}")
                right_is_region = self._model.NewBoolVar(f"right_{left_position.right.r}_{left_position.right.c}_is_region_{region_number}")

                self._model.Add(self._grid_vars[left_position.r][left_position.c] == region_number).OnlyEnforceIf(left_is_region)
                self._model.Add(self._grid_vars[left_position.r][left_position.c] != region_number).OnlyEnforceIf(left_is_region.Not())
                self._model.Add(self._grid_vars[left_position.right.r][left_position.right.c] == region_number).OnlyEnforceIf(right_is_region)
                self._model.Add(self._grid_vars[left_position.right.r][left_position.right.c] != region_number).OnlyEnforceIf(right_is_region.Not())

                self._model.AddBoolOr([left_is_region.Not(), right_is_region])

            for right_position in self._grid.all_positions_right(position)[-1:0:-1]:
                right_is_region = self._model.NewBoolVar(f"right_{right_position.r}_{right_position.c}_is_region_{region_number}")
                left_is_region = self._model.NewBoolVar(f"left_{right_position.left.r}_{right_position.left.c}_is_region_{region_number}")

                self._model.Add(self._grid_vars[right_position.r][right_position.c] == region_number).OnlyEnforceIf(right_is_region)
                self._model.Add(self._grid_vars[right_position.r][right_position.c] != region_number).OnlyEnforceIf(right_is_region.Not())
                self._model.Add(self._grid_vars[right_position.left.r][right_position.left.c] == region_number).OnlyEnforceIf(left_is_region)
                self._model.Add(self._grid_vars[right_position.left.r][right_position.left.c] != region_number).OnlyEnforceIf(left_is_region.Not())

                self._model.AddBoolOr([right_is_region.Not(), left_is_region])
