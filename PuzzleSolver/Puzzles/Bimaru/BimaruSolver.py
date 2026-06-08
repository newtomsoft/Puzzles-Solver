from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


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
        super().__init__()
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
        self._grid_vars = None
        self._type_bools = {}
        self._previous_solution_grid = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.new_int_var(0, BimaruSolver.ship_single, f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_type_bool_constraints()
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
            return Grid.empty()

        grid = Grid([[self._solver.value(self._grid_vars[Position(r, c)]) for c in range(self.columns_number)] for r in range(self.rows_number)])
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
                    temp_var = self._model.new_bool_var(f"prev_{r}_{c}")
                    self._model.add(self._grid_vars[position] == value).only_enforce_if(temp_var)
                    self._model.add(self._grid_vars[position] != value).only_enforce_if(temp_var.negated())
                    previous_solution_literals.append(temp_var)

        if previous_solution_literals:
            self._model.add_bool_or([lit.negated() for lit in previous_solution_literals])

        return self.get_solution()

    def _total_ships_size(self):
        total = 0
        for size, number in self.ships_number_by_size.items():
            total += size * number
        return total

    def _ship(self, position):
        return self._grid_vars[position]

    def _add_constraints(self):
        self._add_sums_constraint()
        self._add_ship_implies_constraint()
        self._add_ships_size_constraint()

    def _add_type_bool_constraints(self):
        for position, _ in self._grid_vars:
            value = self._grid[position]
            if value == BimaruSolver.ship_middle_input:
                middle_h = self._model.new_bool_var(f"middle_h_{position.r}_{position.c}")
                middle_v = self._model.new_bool_var(f"middle_v_{position.r}_{position.c}")
                self._model.add(self._ship(position) == BimaruSolver.ship_middle_horizontal).only_enforce_if(middle_h)
                self._model.add(self._ship(position) != BimaruSolver.ship_middle_horizontal).only_enforce_if(middle_h.Not())
                self._model.add(self._ship(position) == BimaruSolver.ship_middle_vertical).only_enforce_if(middle_v)
                self._model.add(self._ship(position) != BimaruSolver.ship_middle_vertical).only_enforce_if(middle_v.Not())
                self._model.add_bool_or([middle_h, middle_v])
                self._type_bools[(position, BimaruSolver.ship_middle_horizontal)] = middle_h
                self._type_bools[(position, BimaruSolver.ship_middle_vertical)] = middle_v
                for t in (BimaruSolver.ship_single, BimaruSolver.ship_top, BimaruSolver.ship_bottom, BimaruSolver.ship_left, BimaruSolver.ship_right):
                    b = self._model.new_bool_var(f"type_{t}_{position.r}_{position.c}")
                    self._model.add(self._ship(position) == t).only_enforce_if(b)
                    self._model.add(self._ship(position) != t).only_enforce_if(b.Not())
                    self._type_bools[(position, t)] = b
            elif value >= 0:
                self._model.add(self._ship(position) == value)
                for t in range(BimaruSolver.water, BimaruSolver.ship_single + 1):
                    b = self._model.new_bool_var(f"type_{t}_{position.r}_{position.c}")
                    self._model.add(self._ship(position) == t).only_enforce_if(b)
                    self._model.add(self._ship(position) != t).only_enforce_if(b.Not())
                    self._type_bools[(position, t)] = b
            else:
                for t in range(BimaruSolver.water, BimaruSolver.ship_single + 1):
                    b = self._model.new_bool_var(f"type_{t}_{position.r}_{position.c}")
                    self._model.add(self._ship(position) == t).only_enforce_if(b)
                    self._model.add(self._ship(position) != t).only_enforce_if(b.Not())
                    self._type_bools[(position, t)] = b

    def _add_sums_constraint(self):
        for index in range(self.rows_number):
            row_vars = []
            for c in range(self.columns_number):
                is_ship = self._model.new_bool_var(f"is_ship_r{index}_c{c}")
                self._model.add(self._grid_vars[Position(index, c)] != BimaruSolver.water).only_enforce_if(is_ship)
                self._model.add(self._grid_vars[Position(index, c)] == BimaruSolver.water).only_enforce_if(is_ship.Not())
                row_vars.append(is_ship)
            self._model.add(sum(row_vars) == self.ship_cells['row'][index])

        for index in range(self.columns_number):
            col_vars = []
            for r in range(self.rows_number):
                is_ship = self._model.new_bool_var(f"is_ship_r{r}_c{index}")
                self._model.add(self._grid_vars[Position(r, index)] != BimaruSolver.water).only_enforce_if(is_ship)
                self._model.add(self._grid_vars[Position(r, index)] == BimaruSolver.water).only_enforce_if(is_ship.Not())
                col_vars.append(is_ship)
            self._model.add(sum(col_vars) == self.ship_cells['column'][index])

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
        is_single = self._type_bools[(position, BimaruSolver.ship_single)]
        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            self._model.add(self._ship(neighbor_position) == BimaruSolver.water).only_enforce_if(is_single)

    def _add_ship_bottom_implies_constraint(self, position: Position):
        is_bottom = self._type_bools[(position, BimaruSolver.ship_bottom)]

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.up:
                self._model.add(self._ship(neighbor_position) == BimaruSolver.water).only_enforce_if(is_bottom)

        if position.r > 0:
            self._model.add_bool_or([
                self._type_bools[(position.up, BimaruSolver.ship_top)],
                self._type_bools[(position.up, BimaruSolver.ship_middle_vertical)]
            ]).only_enforce_if(is_bottom)
        else:
            self._model.add(self._ship(position) != BimaruSolver.ship_bottom)

    def _add_ship_top_implies_constraint(self, position: Position):
        is_top = self._type_bools[(position, BimaruSolver.ship_top)]

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.down:
                self._model.add(self._ship(neighbor_position) == BimaruSolver.water).only_enforce_if(is_top)

        if position.r < self.rows_number - 1:
            self._model.add_bool_or([
                self._type_bools[(position.down, BimaruSolver.ship_bottom)],
                self._type_bools[(position.down, BimaruSolver.ship_middle_vertical)]
            ]).only_enforce_if(is_top)
        else:
            self._model.add(self._ship(position) != BimaruSolver.ship_top)

    def _add_ship_left_implies_constraint(self, position: Position):
        is_left = self._type_bools[(position, BimaruSolver.ship_left)]

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.right:
                self._model.add(self._ship(neighbor_position) == BimaruSolver.water).only_enforce_if(is_left)

        if position.c < self.columns_number - 1:
            self._model.add_bool_or([
                self._type_bools[(position.right, BimaruSolver.ship_right)],
                self._type_bools[(position.right, BimaruSolver.ship_middle_horizontal)]
            ]).only_enforce_if(is_left)
        else:
            self._model.add(self._ship(position) != BimaruSolver.ship_left)

    def _add_ship_right_implies_constraint(self, position: Position):
        is_right = self._type_bools[(position, BimaruSolver.ship_right)]

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.left:
                self._model.add(self._ship(neighbor_position) == BimaruSolver.water).only_enforce_if(is_right)

        if position.c > 0:
            self._model.add_bool_or([
                self._type_bools[(position.left, BimaruSolver.ship_left)],
                self._type_bools[(position.left, BimaruSolver.ship_middle_horizontal)]
            ]).only_enforce_if(is_right)
        else:
            self._model.add(self._ship(position) != BimaruSolver.ship_right)

    def _add_ship_middle_horizontal_implies_constraint(self, position: Position):
        is_middle_h = self._type_bools[(position, BimaruSolver.ship_middle_horizontal)]

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.left and neighbor_position != position.right:
                self._model.add(self._ship(neighbor_position) == BimaruSolver.water).only_enforce_if(is_middle_h)

        if position.c > 0:
            self._model.add_bool_or([
                self._type_bools[(position.left, BimaruSolver.ship_left)],
                self._type_bools[(position.left, BimaruSolver.ship_middle_horizontal)]
            ]).only_enforce_if(is_middle_h)
        else:
            self._model.add(self._ship(position) != BimaruSolver.ship_middle_horizontal)

        if position.c < self.columns_number - 1:
            self._model.add_bool_or([
                self._type_bools[(position.right, BimaruSolver.ship_right)],
                self._type_bools[(position.right, BimaruSolver.ship_middle_horizontal)]
            ]).only_enforce_if(is_middle_h)
        else:
            self._model.add(self._ship(position) != BimaruSolver.ship_middle_horizontal)

    def _add_ship_middle_vertical_implies_constraint(self, position: Position):
        is_middle_v = self._type_bools[(position, BimaruSolver.ship_middle_vertical)]

        for neighbor_position in self._grid.neighbors_positions(position, "diagonal"):
            if neighbor_position != position.up and neighbor_position != position.down:
                self._model.add(self._ship(neighbor_position) == BimaruSolver.water).only_enforce_if(is_middle_v)

        if position.r > 0:
            self._model.add_bool_or([
                self._type_bools[(position.up, BimaruSolver.ship_top)],
                self._type_bools[(position.up, BimaruSolver.ship_middle_vertical)]
            ]).only_enforce_if(is_middle_v)
        else:
            self._model.add(self._ship(position) != BimaruSolver.ship_middle_vertical)

        if position.r < self.rows_number - 1:
            self._model.add_bool_or([
                self._type_bools[(position.down, BimaruSolver.ship_bottom)],
                self._type_bools[(position.down, BimaruSolver.ship_middle_vertical)]
            ]).only_enforce_if(is_middle_v)
        else:
            self._model.add(self._ship(position) != BimaruSolver.ship_middle_vertical)

    def _is_cell_compatible(self, position: Position, required_type: int) -> bool:
        value = self._grid[position]
        if value == -1:
            return True
        if value == BimaruSolver.ship_middle_input:
            return required_type in (BimaruSolver.ship_middle_horizontal, BimaruSolver.ship_middle_vertical)
        return value == required_type

    def _add_ships_size_constraint(self):
        single_number = self.ships_number_by_size.get(1) if self.ships_number_by_size.get(1) is not None else 0
        if single_number > 0:
            single_ship_vars = []
            for position, _ in self._grid_vars:
                if not self._is_cell_compatible(position, BimaruSolver.ship_single):
                    continue
                is_single = self._type_bools[(position, BimaruSolver.ship_single)]
                single_ship_vars.append(is_single)
            self._model.add(sum(single_ship_vars) == single_number)

        for number in range(2, max(self.ships_number_by_size.keys()) + 1):
            if self.ships_number_by_size.get(number) is None:
                continue

            ship_count_vars = []

            for position, _ in self._grid_vars:
                horizontal_positions_n = [position + Position(0, i) for i in range(number) if (position + Position(0, i)).c < self.columns_number]
                if len(horizontal_positions_n) == number:
                    required_types = [BimaruSolver.ship_left] + [BimaruSolver.ship_middle_horizontal] * (number - 2) + [BimaruSolver.ship_right]
                    if all(self._is_cell_compatible(pos, req) for pos, req in zip(horizontal_positions_n, required_types)):
                        is_horizontal_ship = self._model.new_bool_var(f"is_h_ship_{number}_{position.r}_{position.c}")

                        self._model.add_bool_and([
                            self._type_bools[(horizontal_positions_n[0], BimaruSolver.ship_left)],
                            *[self._type_bools[(horizontal_positions_n[i], BimaruSolver.ship_middle_horizontal)] for i in range(1, number - 1)],
                            self._type_bools[(horizontal_positions_n[-1], BimaruSolver.ship_right)]
                        ]).only_enforce_if(is_horizontal_ship)

                        neg_conditions = [
                            self._type_bools[(horizontal_positions_n[0], BimaruSolver.ship_left)].Not(),
                            *[self._type_bools[(horizontal_positions_n[i], BimaruSolver.ship_middle_horizontal)].Not() for i in range(1, number - 1)],
                            self._type_bools[(horizontal_positions_n[-1], BimaruSolver.ship_right)].Not()
                        ]
                        self._model.add_bool_or(neg_conditions).only_enforce_if(is_horizontal_ship.Not())

                        ship_count_vars.append(is_horizontal_ship)

            for position, _ in self._grid_vars:
                vertical_positions_n = [position + Position(i, 0) for i in range(number) if (position + Position(i, 0)).r < self.rows_number]
                if len(vertical_positions_n) == number:
                    required_types = [BimaruSolver.ship_top] + [BimaruSolver.ship_middle_vertical] * (number - 2) + [BimaruSolver.ship_bottom]
                    if all(self._is_cell_compatible(pos, req) for pos, req in zip(vertical_positions_n, required_types)):
                        is_vertical_ship = self._model.new_bool_var(f"is_v_ship_{number}_{position.r}_{position.c}")

                        self._model.add_bool_and([
                            self._type_bools[(vertical_positions_n[0], BimaruSolver.ship_top)],
                            *[self._type_bools[(vertical_positions_n[i], BimaruSolver.ship_middle_vertical)] for i in range(1, number - 1)],
                            self._type_bools[(vertical_positions_n[-1], BimaruSolver.ship_bottom)]
                        ]).only_enforce_if(is_vertical_ship)

                        neg_conditions = [
                            self._type_bools[(vertical_positions_n[0], BimaruSolver.ship_top)].Not(),
                            *[self._type_bools[(vertical_positions_n[i], BimaruSolver.ship_middle_vertical)].Not() for i in range(1, number - 1)],
                            self._type_bools[(vertical_positions_n[-1], BimaruSolver.ship_bottom)].Not()
                        ]
                        self._model.add_bool_or(neg_conditions).only_enforce_if(is_vertical_ship.Not())

                        ship_count_vars.append(is_vertical_ship)

            self._model.add(sum(ship_count_vars) == self.ships_number_by_size[number])
