from Domain.Grid.Grid import Grid
from Domain.Position import Position
from GameSolver import GameSolver
from Ports.SolverEngine import SolverEngine


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

    def __init__(self, grid: Grid, ship_cells: dict[str, list[int]], ships_number_by_size: dict[int, int], solver_engine: SolverEngine):
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
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution_grid = None

    def _init_solver(self):
        self._grid_z3 = Grid([[self._solver.int(f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.has_constraints():
            self._init_solver()
        if not self._solver.has_solution():
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._grid_z3[Position(r, c)])() for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._previous_solution_grid = grid
        return grid

    def get_other_solution(self):
        exclusion_constraint = self._solver.Not(self._solver.And([self._grid_z3[Position(r, c)] == self._previous_solution_grid[Position(r, c)] for r in range(self.rows_number) for c in range(self.columns_number) if self._previous_solution_grid.value(r, c)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _total_ships_size(self):
        total = 0
        for size, number in self.ships_number_by_size.items():
            total += size * number
        return total

    def _ship(self, position):
        return self._grid_z3[position]

    def _add_constraints(self):
        self._add_initials_constraint()
        self._add_sums_constraint()
        self._add_ship_implies_constraint()
        self._add_ships_size_constraint()

    def _add_initials_constraint(self):
        for position, value in self._grid:
            match value:
                case BimaruSolver.water:
                    self._solver.add(self._ship(position) == BimaruSolver.water)
                case BimaruSolver.ship_single:
                    self._solver.add(self._ship(position) == BimaruSolver.ship_single)
                case BimaruSolver.ship_top:
                    self._solver.add(self._ship(position) == BimaruSolver.ship_top)
                case BimaruSolver.ship_bottom:
                    self._solver.add(self._ship(position) == BimaruSolver.ship_bottom)
                case BimaruSolver.ship_left:
                    self._solver.add(self._ship(position) == BimaruSolver.ship_left)
                case BimaruSolver.ship_right:
                    self._solver.add(self._ship(position) == BimaruSolver.ship_right)
                case BimaruSolver.ship_middle_input:
                    self._solver.add(self._solver.Or(self._ship(position) == BimaruSolver.ship_middle_horizontal, self._ship(position) == BimaruSolver.ship_middle_vertical))
                case _:
                    self._solver.add(self._ship(position) >= BimaruSolver.water)
                    self._solver.add(self._ship(position) <= BimaruSolver.ship_single)

    def _add_sums_constraint(self):
        for index, row in enumerate(self._grid_z3.matrix):
            self._solver.add(self._solver.sum([self._solver.If(row[i] != BimaruSolver.water, 1, 0) for i in range(self.columns_number)]) == self.ship_cells['row'][index])

        for index, column_tuple in enumerate(zip(*self._grid_z3.matrix)):
            column = list(column_tuple)
            self._solver.add(self._solver.sum([self._solver.If(column[i] != BimaruSolver.water, 1, 0) for i in range(self.rows_number)]) == self.ship_cells['column'][index])

    def _add_ship_implies_constraint(self):
        for position, _ in self._grid_z3:
            self._add_ship_single_implies_constraint(position)
            self._add_ship_bottom_implies_constraint(position)
            self._add_ship_top_implies_constraint(position)
            self._add_ship_left_implies_constraint(position)
            self._add_ship_right_implies_constraint(position)
            self._add_ship_middle_horizontal_implies_constraint(position)
            self._add_ship_middle_vertical_implies_constraint(position)

    def _add_ship_single_implies_constraint(self, position: Position):
        self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_single, self._solver.And([self._ship(neighbor_position) == BimaruSolver.water for neighbor_position in self._grid.neighbors_positions(position, "diagonal")])))

    def _add_ship_bottom_implies_constraint(self, position: Position):
        self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_bottom, self._solver.And([self._ship(neighbor_position) == BimaruSolver.water for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.up])))
        if position.r > 0:
            self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_bottom, self._solver.Or(self._ship(position.up) == BimaruSolver.ship_top, self._ship(position.up) == BimaruSolver.ship_middle_vertical)))
        else:
            self._solver.add(self._ship(position) != BimaruSolver.ship_bottom)

    def _add_ship_top_implies_constraint(self, position: Position):
        self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_top, self._solver.And([self._ship(neighbor_position) == BimaruSolver.water for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.down])))
        if position.r < self.rows_number - 1:
            self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_top, self._solver.Or(self._ship(position.down) == BimaruSolver.ship_bottom, self._ship(position.down) == BimaruSolver.ship_middle_vertical)))
        else:
            self._solver.add(self._ship(position) != BimaruSolver.ship_top)

    def _add_ship_left_implies_constraint(self, position: Position):
        self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_left, self._solver.And([self._ship(neighbor_position) == BimaruSolver.water for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.right])))
        if position.c < self.columns_number - 1:
            self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_left, self._solver.Or(self._ship(position.right) == BimaruSolver.ship_right, self._ship(position.right) == BimaruSolver.ship_middle_horizontal)))
        else:
            self._solver.add(self._ship(position) != BimaruSolver.ship_left)

    def _add_ship_right_implies_constraint(self, position: Position):
        self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_right, self._solver.And([self._ship(neighbor_position) == BimaruSolver.water for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.left])))
        if position.c > 0:
            self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_right, self._solver.Or(self._ship(position.left) == BimaruSolver.ship_left, self._ship(position.left) == BimaruSolver.ship_middle_horizontal)))
        else:
            self._solver.add(self._ship(position) != BimaruSolver.ship_right)

    def _add_ship_middle_horizontal_implies_constraint(self, position: Position):
        self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_middle_horizontal,
                                              self._solver.And([self._ship(neighbor_position) == BimaruSolver.water for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.left and neighbor_position != position.right])))
        if position.c > 0:
            self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_middle_horizontal, self._solver.Or(self._ship(position.left) == BimaruSolver.ship_left, self._ship(position.left) == BimaruSolver.ship_middle_horizontal)))
        else:
            self._solver.add(self._ship(position) != BimaruSolver.ship_middle_horizontal)
        if position.c < self.columns_number - 1:
            self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_middle_horizontal, self._solver.Or(self._ship(position.right) == BimaruSolver.ship_right, self._ship(position.right) == BimaruSolver.ship_middle_horizontal)))
        else:
            self._solver.add(self._ship(position) != BimaruSolver.ship_middle_horizontal)

    def _add_ship_middle_vertical_implies_constraint(self, position: Position):
        self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_middle_vertical,
                                              self._solver.And([self._ship(neighbor_position) == BimaruSolver.water for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.up and neighbor_position != position.down])))
        if position.r > 0:
            self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_middle_vertical, self._solver.Or(self._ship(position.up) == BimaruSolver.ship_top, self._ship(position.up) == BimaruSolver.ship_middle_vertical)))
        else:
            self._solver.add(self._ship(position) != BimaruSolver.ship_middle_vertical)
        if position.r < self.rows_number - 1:
            self._solver.add(self._solver.Implies(self._ship(position) == BimaruSolver.ship_middle_vertical, self._solver.Or(self._ship(position.down) == BimaruSolver.ship_bottom, self._ship(position.down) == BimaruSolver.ship_middle_vertical)))
        else:
            self._solver.add(self._ship(position) != BimaruSolver.ship_middle_vertical)

    def _add_ships_size_constraint(self):
        single_number = self.ships_number_by_size.get(1) if self.ships_number_by_size.get(1) is not None else 0
        self._solver.add(self._solver.sum([self._solver.If(self._ship(position) == BimaruSolver.ship_single, 1, 0) for position, _ in self._grid_z3]) == single_number)

        for number in range(2, max(self.ships_number_by_size.keys()) + 1):
            if self.ships_number_by_size.get(number) is None:
                continue
            constraint = []
            for position, _ in self._grid_z3:
                horizontal_positions_n = [position + Position(0, i) for i in range(number) if (position + Position(0, i)).c < self.columns_number]
                if len(horizontal_positions_n) == number:
                    start_horizontal_condition = self._solver.And(self._ship(horizontal_positions_n[0]) == BimaruSolver.ship_left)
                    between_horizontal_condition = self._solver.And([self._ship(current_position) == BimaruSolver.ship_middle_horizontal for current_position in horizontal_positions_n[1:-1]])
                    end_horizontal_condition = self._solver.And(self._ship(horizontal_positions_n[-1]) == BimaruSolver.ship_right)
                    constraint.append(self._solver.If(self._solver.And(start_horizontal_condition,  between_horizontal_condition, end_horizontal_condition), 1, 0))
                vertical_positions_n = [position + Position(i, 0) for i in range(number) if (position + Position(i, 0)).r < self.rows_number]
                if len(vertical_positions_n) == number:
                    start_vertical_condition = self._solver.And(self._ship(vertical_positions_n[0]) == BimaruSolver.ship_top)
                    between_vertical_condition = self._solver.And([self._ship(current_position) == BimaruSolver.ship_middle_vertical for current_position in vertical_positions_n[1:-1]])
                    end_vertical_condition = self._solver.And(self._ship(vertical_positions_n[-1]) == BimaruSolver.ship_bottom)
                    constraint.append(self._solver.If(self._solver.And(start_vertical_condition, between_vertical_condition, end_vertical_condition), 1, 0))
            self._solver.add(self._solver.sum(constraint) == self.ships_number_by_size[number])
