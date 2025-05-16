from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class BimaruSolver(GameSolver):
    water = 0
    ship_top = 1
    ship_bottom = 2
    ship_left = 3
    ship_right = 4
    ship_middle_vertical = 5
    ship_middle_horizontal = 6
    ship_single = 7

    ship_middle_input = 8

    def __init__(self, grid: Grid, ship_cells: dict[str, list[int]], ships_number_by_size: dict[int, int]):
        if BimaruSolver.ship_single != 7:
            raise ValueError("Ship single value error")
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.ship_cells = ship_cells
        self.ships_number_by_size = ships_number_by_size

        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 6:
            raise ValueError("The grid must be at least 6x6")
        if len(self.ship_cells['column']) != self.columns_number:
            raise ValueError("Boat cells column must have the same length as the columns number")
        if len(self.ship_cells['row']) != self.rows_number:
            raise ValueError("Boat cells row must have the same length as the rows number")
        if not self.ships_number_by_size:
            raise ValueError("At least one boat must be placed")
        if sum(self.ship_cells['column']) != sum(self.ship_cells['row']):
            raise ValueError("The sum of boat cells by row and column must be equal")
        if self._total_ships_size() != sum(self.ship_cells['column']):
            raise ValueError("The sum of the size of the ships must be equal to the sum of ships cells")
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = None
        self._previous_solution_grid = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.NewIntVar(0, BimaruSolver.ship_single, f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.Solve(self._model)
        if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
            return Grid.empty()

        grid = Grid([[self._solver.Value(self._grid_vars[Position(r, c)]) for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._previous_solution_grid = grid
        return grid

    def get_other_solution(self):
        if self._previous_solution_grid is None:
            return Grid.empty()

        previous_solution_literals = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                position = Position(r, c)
                value = self._previous_solution_grid[position]
                if value > 0:  # Only consider non-water cells
                    temp_var = self._model.NewBoolVar(f"prev_{r}_{c}")
                    self._model.Add(self._grid_vars[position] == value).OnlyEnforceIf(temp_var)
                    self._model.Add(self._grid_vars[position] != value).OnlyEnforceIf(temp_var.Not())
                    previous_solution_literals.append(temp_var)

        if previous_solution_literals:
            self._model.AddBoolOr([lit.Not() for lit in previous_solution_literals])

        return self.get_solution()

    def _total_ships_size(self):
        total = 0
        for size, number in self.ships_number_by_size.items():
            total += size * number
        return total

    def _ship(self, position):
        return self._grid_vars[position]

    def _add_constraints(self):
        self._add_initials_constraint()
        self._add_sums_constraint()
        self._add_ship_implies_constraint()
        self._add_ships_size_constraint()

    def _add_initials_constraint(self):
        for position, value in self._grid:
            match value:
                case BimaruSolver.water:
                    self._model.Add(self._ship(position) == BimaruSolver.water)
                case BimaruSolver.ship_single:
                    self._model.Add(self._ship(position) == BimaruSolver.ship_single)
                case BimaruSolver.ship_top:
                    self._model.Add(self._ship(position) == BimaruSolver.ship_top)
                case BimaruSolver.ship_bottom:
                    self._model.Add(self._ship(position) == BimaruSolver.ship_bottom)
                case BimaruSolver.ship_left:
                    self._model.Add(self._ship(position) == BimaruSolver.ship_left)
                case BimaruSolver.ship_right:
                    self._model.Add(self._ship(position) == BimaruSolver.ship_right)
                case BimaruSolver.ship_middle_input:
                    middle_h = self._model.NewBoolVar(f"middle_h_{position.r}_{position.c}")
                    middle_v = self._model.NewBoolVar(f"middle_v_{position.r}_{position.c}")
                    self._model.Add(self._ship(position) == BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(middle_h)
                    self._model.Add(self._ship(position) == BimaruSolver.ship_middle_vertical).OnlyEnforceIf(middle_v)
                    self._model.AddBoolOr([middle_h, middle_v])
                case _:
                    self._model.Add(self._ship(position) >= BimaruSolver.water)
                    self._model.Add(self._ship(position) <= BimaruSolver.ship_single)

    def _add_sums_constraint(self):
        for index in range(self.rows_number):
            row_vars = []
            for c in range(self.columns_number):
                is_ship = self._model.NewBoolVar(f"is_ship_r{index}_c{c}")
                self._model.Add(self._grid_vars[Position(index, c)] != BimaruSolver.water).OnlyEnforceIf(is_ship)
                self._model.Add(self._grid_vars[Position(index, c)] == BimaruSolver.water).OnlyEnforceIf(is_ship.Not())
                row_vars.append(is_ship)
            self._model.Add(sum(row_vars) == self.ship_cells['row'][index])

        for index in range(self.columns_number):
            col_vars = []
            for r in range(self.rows_number):
                is_ship = self._model.NewBoolVar(f"is_ship_r{r}_c{index}")
                self._model.Add(self._grid_vars[Position(r, index)] != BimaruSolver.water).OnlyEnforceIf(is_ship)
                self._model.Add(self._grid_vars[Position(r, index)] == BimaruSolver.water).OnlyEnforceIf(is_ship.Not())
                col_vars.append(is_ship)
            self._model.Add(sum(col_vars) == self.ship_cells['column'][index])

    def _add_ship_implies_constraint(self):
        for position, _ in self._grid_vars:
            self._add_ship_single_implies_constraint(position)
            self._add_ship_bottom_implies_constraint(position)
            self._add_ship_top_implies_constraint(position)
            self._add_ship_left_implies_constraint(position)
            self._add_ship_right_implies_constraint(position)
            self._add_ship_middle_horizontal_implies_constraint(position)
            self._add_ship_middle_vertical_implies_constraint(position)

    def _add_ship_single_implies_constraint(self, position: Position):
        is_single = self._model.NewBoolVar(f"is_single_{position.r}_{position.c}")
        self._model.Add(self._ship(position) == BimaruSolver.ship_single).OnlyEnforceIf(is_single)
        self._model.Add(self._ship(position) != BimaruSolver.ship_single).OnlyEnforceIf(is_single.Not())

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            self._model.Add(self._ship(neighbor_position) == BimaruSolver.water).OnlyEnforceIf(is_single)

    def _add_ship_bottom_implies_constraint(self, position: Position):
        is_bottom = self._model.NewBoolVar(f"is_bottom_{position.r}_{position.c}")
        self._model.Add(self._ship(position) == BimaruSolver.ship_bottom).OnlyEnforceIf(is_bottom)
        self._model.Add(self._ship(position) != BimaruSolver.ship_bottom).OnlyEnforceIf(is_bottom.Not())

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.up:
                self._model.Add(self._ship(neighbor_position) == BimaruSolver.water).OnlyEnforceIf(is_bottom)

        if position.r > 0:
            is_top_above = self._model.NewBoolVar(f"is_top_above_{position.r}_{position.c}")
            is_middle_v_above = self._model.NewBoolVar(f"is_middle_v_above_{position.r}_{position.c}")

            self._model.Add(self._ship(position.up) == BimaruSolver.ship_top).OnlyEnforceIf(is_top_above)
            self._model.Add(self._ship(position.up) != BimaruSolver.ship_top).OnlyEnforceIf(is_top_above.Not())

            self._model.Add(self._ship(position.up) == BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v_above)
            self._model.Add(self._ship(position.up) != BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v_above.Not())

            self._model.AddBoolOr([is_top_above, is_middle_v_above]).OnlyEnforceIf(is_bottom)
        else:
            self._model.Add(self._ship(position) != BimaruSolver.ship_bottom)

    def _add_ship_top_implies_constraint(self, position: Position):
        is_top = self._model.NewBoolVar(f"is_top_{position.r}_{position.c}")
        self._model.Add(self._ship(position) == BimaruSolver.ship_top).OnlyEnforceIf(is_top)
        self._model.Add(self._ship(position) != BimaruSolver.ship_top).OnlyEnforceIf(is_top.Not())

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.down:
                self._model.Add(self._ship(neighbor_position) == BimaruSolver.water).OnlyEnforceIf(is_top)

        if position.r < self.rows_number - 1:
            is_bottom_below = self._model.NewBoolVar(f"is_bottom_below_{position.r}_{position.c}")
            is_middle_v_below = self._model.NewBoolVar(f"is_middle_v_below_{position.r}_{position.c}")

            self._model.Add(self._ship(position.down) == BimaruSolver.ship_bottom).OnlyEnforceIf(is_bottom_below)
            self._model.Add(self._ship(position.down) != BimaruSolver.ship_bottom).OnlyEnforceIf(is_bottom_below.Not())

            self._model.Add(self._ship(position.down) == BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v_below)
            self._model.Add(self._ship(position.down) != BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v_below.Not())

            self._model.AddBoolOr([is_bottom_below, is_middle_v_below]).OnlyEnforceIf(is_top)
        else:
            self._model.Add(self._ship(position) != BimaruSolver.ship_top)

    def _add_ship_left_implies_constraint(self, position: Position):
        is_left = self._model.NewBoolVar(f"is_left_{position.r}_{position.c}")
        self._model.Add(self._ship(position) == BimaruSolver.ship_left).OnlyEnforceIf(is_left)
        self._model.Add(self._ship(position) != BimaruSolver.ship_left).OnlyEnforceIf(is_left.Not())

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.right:
                self._model.Add(self._ship(neighbor_position) == BimaruSolver.water).OnlyEnforceIf(is_left)

        if position.c < self.columns_number - 1:
            is_right_right = self._model.NewBoolVar(f"is_right_right_{position.r}_{position.c}")
            is_middle_h_right = self._model.NewBoolVar(f"is_middle_h_right_{position.r}_{position.c}")

            self._model.Add(self._ship(position.right) == BimaruSolver.ship_right).OnlyEnforceIf(is_right_right)
            self._model.Add(self._ship(position.right) != BimaruSolver.ship_right).OnlyEnforceIf(is_right_right.Not())

            self._model.Add(self._ship(position.right) == BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h_right)
            self._model.Add(self._ship(position.right) != BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h_right.Not())

            self._model.AddBoolOr([is_right_right, is_middle_h_right]).OnlyEnforceIf(is_left)
        else:
            self._model.Add(self._ship(position) != BimaruSolver.ship_left)

    def _add_ship_right_implies_constraint(self, position: Position):
        is_right = self._model.NewBoolVar(f"is_right_{position.r}_{position.c}")
        self._model.Add(self._ship(position) == BimaruSolver.ship_right).OnlyEnforceIf(is_right)
        self._model.Add(self._ship(position) != BimaruSolver.ship_right).OnlyEnforceIf(is_right.Not())

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.left:
                self._model.Add(self._ship(neighbor_position) == BimaruSolver.water).OnlyEnforceIf(is_right)

        if position.c > 0:
            is_left_left = self._model.NewBoolVar(f"is_left_left_{position.r}_{position.c}")
            is_middle_h_left = self._model.NewBoolVar(f"is_middle_h_left_{position.r}_{position.c}")

            self._model.Add(self._ship(position.left) == BimaruSolver.ship_left).OnlyEnforceIf(is_left_left)
            self._model.Add(self._ship(position.left) != BimaruSolver.ship_left).OnlyEnforceIf(is_left_left.Not())

            self._model.Add(self._ship(position.left) == BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h_left)
            self._model.Add(self._ship(position.left) != BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h_left.Not())

            self._model.AddBoolOr([is_left_left, is_middle_h_left]).OnlyEnforceIf(is_right)
        else:
            self._model.Add(self._ship(position) != BimaruSolver.ship_right)

    def _add_ship_middle_horizontal_implies_constraint(self, position: Position):
        is_middle_h = self._model.NewBoolVar(f"is_middle_h_{position.r}_{position.c}")
        self._model.Add(self._ship(position) == BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h)
        self._model.Add(self._ship(position) != BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h.Not())

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.left and neighbor_position != position.right:
                self._model.Add(self._ship(neighbor_position) == BimaruSolver.water).OnlyEnforceIf(is_middle_h)

        if position.c > 0:
            is_left_left = self._model.NewBoolVar(f"is_left_left_mh_{position.r}_{position.c}")
            is_middle_h_left = self._model.NewBoolVar(f"is_middle_h_left_mh_{position.r}_{position.c}")

            self._model.Add(self._ship(position.left) == BimaruSolver.ship_left).OnlyEnforceIf(is_left_left)
            self._model.Add(self._ship(position.left) != BimaruSolver.ship_left).OnlyEnforceIf(is_left_left.Not())

            self._model.Add(self._ship(position.left) == BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h_left)
            self._model.Add(self._ship(position.left) != BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h_left.Not())

            self._model.AddBoolOr([is_left_left, is_middle_h_left]).OnlyEnforceIf(is_middle_h)
        else:
            self._model.Add(self._ship(position) != BimaruSolver.ship_middle_horizontal)

        if position.c < self.columns_number - 1:
            is_right_right = self._model.NewBoolVar(f"is_right_right_mh_{position.r}_{position.c}")
            is_middle_h_right = self._model.NewBoolVar(f"is_middle_h_right_mh_{position.r}_{position.c}")

            self._model.Add(self._ship(position.right) == BimaruSolver.ship_right).OnlyEnforceIf(is_right_right)
            self._model.Add(self._ship(position.right) != BimaruSolver.ship_right).OnlyEnforceIf(is_right_right.Not())

            self._model.Add(self._ship(position.right) == BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h_right)
            self._model.Add(self._ship(position.right) != BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h_right.Not())

            self._model.AddBoolOr([is_right_right, is_middle_h_right]).OnlyEnforceIf(is_middle_h)
        else:
            self._model.Add(self._ship(position) != BimaruSolver.ship_middle_horizontal)

    def _add_ship_middle_vertical_implies_constraint(self, position: Position):
        is_middle_v = self._model.NewBoolVar(f"is_middle_v_{position.r}_{position.c}")
        self._model.Add(self._ship(position) == BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v)
        self._model.Add(self._ship(position) != BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v.Not())

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.up and neighbor_position != position.down:
                self._model.Add(self._ship(neighbor_position) == BimaruSolver.water).OnlyEnforceIf(is_middle_v)

        if position.r > 0:
            is_top_above = self._model.NewBoolVar(f"is_top_above_mv_{position.r}_{position.c}")
            is_middle_v_above = self._model.NewBoolVar(f"is_middle_v_above_mv_{position.r}_{position.c}")

            self._model.Add(self._ship(position.up) == BimaruSolver.ship_top).OnlyEnforceIf(is_top_above)
            self._model.Add(self._ship(position.up) != BimaruSolver.ship_top).OnlyEnforceIf(is_top_above.Not())

            self._model.Add(self._ship(position.up) == BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v_above)
            self._model.Add(self._ship(position.up) != BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v_above.Not())

            self._model.AddBoolOr([is_top_above, is_middle_v_above]).OnlyEnforceIf(is_middle_v)
        else:
            self._model.Add(self._ship(position) != BimaruSolver.ship_middle_vertical)

        if position.r < self.rows_number - 1:
            is_bottom_below = self._model.NewBoolVar(f"is_bottom_below_mv_{position.r}_{position.c}")
            is_middle_v_below = self._model.NewBoolVar(f"is_middle_v_below_mv_{position.r}_{position.c}")

            self._model.Add(self._ship(position.down) == BimaruSolver.ship_bottom).OnlyEnforceIf(is_bottom_below)
            self._model.Add(self._ship(position.down) != BimaruSolver.ship_bottom).OnlyEnforceIf(is_bottom_below.Not())

            self._model.Add(self._ship(position.down) == BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v_below)
            self._model.Add(self._ship(position.down) != BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v_below.Not())

            self._model.AddBoolOr([is_bottom_below, is_middle_v_below]).OnlyEnforceIf(is_middle_v)
        else:
            self._model.Add(self._ship(position) != BimaruSolver.ship_middle_vertical)

    def _add_ships_size_constraint(self):
        single_number = self.ships_number_by_size.get(1) if self.ships_number_by_size.get(1) is not None else 0
        if single_number > 0:
            single_ship_vars = []
            for position, _ in self._grid_vars:
                is_single = self._model.NewBoolVar(f"is_single_count_{position.r}_{position.c}")
                self._model.Add(self._ship(position) == BimaruSolver.ship_single).OnlyEnforceIf(is_single)
                self._model.Add(self._ship(position) != BimaruSolver.ship_single).OnlyEnforceIf(is_single.Not())
                single_ship_vars.append(is_single)
            self._model.Add(sum(single_ship_vars) == single_number)

        for number in range(2, max(self.ships_number_by_size.keys()) + 1):
            if self.ships_number_by_size.get(number) is None:
                continue

            ship_count_vars = []

            for position, _ in self._grid_vars:
                horizontal_positions_n = [position + Position(0, i) for i in range(number) if (position + Position(0, i)).c < self.columns_number]
                if len(horizontal_positions_n) == number:
                    is_horizontal_ship = self._model.NewBoolVar(f"is_h_ship_{number}_{position.r}_{position.c}")

                    ship_part_conditions = []

                    # Start (left) condition
                    is_left_start = self._model.NewBoolVar(f"is_left_start_{number}_{position.r}_{position.c}")
                    self._model.Add(self._ship(horizontal_positions_n[0]) == BimaruSolver.ship_left).OnlyEnforceIf(is_left_start)
                    self._model.Add(self._ship(horizontal_positions_n[0]) != BimaruSolver.ship_left).OnlyEnforceIf(is_left_start.Not())
                    ship_part_conditions.append(is_left_start)

                    # Middle conditions
                    for i, middle_pos in enumerate(horizontal_positions_n[1:-1]):
                        is_middle_h = self._model.NewBoolVar(f"is_middle_h_{number}_{position.r}_{position.c}_{i}")
                        self._model.Add(self._ship(middle_pos) == BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h)
                        self._model.Add(self._ship(middle_pos) != BimaruSolver.ship_middle_horizontal).OnlyEnforceIf(is_middle_h.Not())
                        ship_part_conditions.append(is_middle_h)

                    # End (right) condition
                    is_right_end = self._model.NewBoolVar(f"is_right_end_{number}_{position.r}_{position.c}")
                    self._model.Add(self._ship(horizontal_positions_n[-1]) == BimaruSolver.ship_right).OnlyEnforceIf(is_right_end)
                    self._model.Add(self._ship(horizontal_positions_n[-1]) != BimaruSolver.ship_right).OnlyEnforceIf(is_right_end.Not())
                    ship_part_conditions.append(is_right_end)

                    # All conditions must be true for this to be a valid horizontal ship
                    self._model.AddBoolAnd(ship_part_conditions).OnlyEnforceIf(is_horizontal_ship)
                    self._model.AddBoolOr([condition.Not() for condition in ship_part_conditions]).OnlyEnforceIf(is_horizontal_ship.Not())

                    ship_count_vars.append(is_horizontal_ship)

            for position, _ in self._grid_vars:
                vertical_positions_n = [position + Position(i, 0) for i in range(number) if (position + Position(i, 0)).r < self.rows_number]
                if len(vertical_positions_n) == number:
                    is_vertical_ship = self._model.NewBoolVar(f"is_v_ship_{number}_{position.r}_{position.c}")

                    ship_part_conditions = []

                    # Start (top) condition
                    is_top_start = self._model.NewBoolVar(f"is_top_start_{number}_{position.r}_{position.c}")
                    self._model.Add(self._ship(vertical_positions_n[0]) == BimaruSolver.ship_top).OnlyEnforceIf(is_top_start)
                    self._model.Add(self._ship(vertical_positions_n[0]) != BimaruSolver.ship_top).OnlyEnforceIf(is_top_start.Not())
                    ship_part_conditions.append(is_top_start)

                    # Middle conditions
                    for i, middle_pos in enumerate(vertical_positions_n[1:-1]):
                        is_middle_v = self._model.NewBoolVar(f"is_middle_v_{number}_{position.r}_{position.c}_{i}")
                        self._model.Add(self._ship(middle_pos) == BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v)
                        self._model.Add(self._ship(middle_pos) != BimaruSolver.ship_middle_vertical).OnlyEnforceIf(is_middle_v.Not())
                        ship_part_conditions.append(is_middle_v)

                    # End (bottom) condition
                    is_bottom_end = self._model.NewBoolVar(f"is_bottom_end_{number}_{position.r}_{position.c}")
                    self._model.Add(self._ship(vertical_positions_n[-1]) == BimaruSolver.ship_bottom).OnlyEnforceIf(is_bottom_end)
                    self._model.Add(self._ship(vertical_positions_n[-1]) != BimaruSolver.ship_bottom).OnlyEnforceIf(is_bottom_end.Not())
                    ship_part_conditions.append(is_bottom_end)

                    # All conditions must be true for this to be a valid vertical ship
                    self._model.AddBoolAnd(ship_part_conditions).OnlyEnforceIf(is_vertical_ship)
                    self._model.AddBoolOr([condition.Not() for condition in ship_part_conditions]).OnlyEnforceIf(is_vertical_ship.Not())

                    ship_count_vars.append(is_vertical_ship)

            self._model.Add(sum(ship_count_vars) == self.ships_number_by_size[number])
