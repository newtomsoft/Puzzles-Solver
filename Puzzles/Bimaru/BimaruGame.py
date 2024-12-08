from z3 import Solver, sat, Int, And, Not, If, Sum, Or, Implies

from Position import Position
from Utils.Grid import Grid


class BimaruGame:
    _watter = 0
    _ship_top = 1
    _ship_bottom = 2
    _ship_left = 3
    _ship_right = 4
    _ship_middle_vertical = 5
    _ship_middle_horizontal = 6
    _ship_single = 7

    _ship_middle_input = 8

    def __init__(self, params: (Grid, dict[str, list[int]], dict[int, int])):
        if BimaruGame._ship_single != 7:
            raise ValueError("Ship single value error")
        self._grid: Grid = params[0]
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.boat_cells: dict[str, list[int]] = params[1]
        self.boats_number_by_size: dict[int, int] = params[2]

        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 6:
            raise ValueError("The grid must be at least 6x6")
        if len(self.boat_cells['column']) != self.columns_number:
            raise ValueError("Boat cells column must have the same length as the columns number")
        if len(self.boat_cells['row']) != self.rows_number:
            raise ValueError("Boat cells row must have the same length as the rows number")
        if not self.boats_number_by_size:
            raise ValueError("At least one boat must be placed")
        if sum(self.boat_cells['column']) != sum(self.boat_cells['row']):
            raise ValueError("The sum of boat cells by row and column must be equal")
        if self.total_ships_size() != sum(self.boat_cells['column']):
            raise ValueError("The sum of the size of the ships must be equal to the sum of boats cells")
        self._solver: Solver | None = None
        self._grid_z3: Grid | None = None
        self._last_solution_grid = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._solver = Solver()
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._solver is None:
            self._init_solver()
        if self._solver.check() != sat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._grid_z3[Position(r, c)]).as_long() for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._last_solution_grid = grid
        return grid

    def get_other_solution(self):
        exclusion_constraint = Not(And([self._grid_z3[Position(r, c)] == self._last_solution_grid[Position(r, c)] for r in range(self.rows_number) for c in range(self.columns_number) if self._last_solution_grid.value(r, c)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _ship(self, position):
        return self._grid_z3[position]

    def _add_constraints(self):
        self._add_initials_constraint()
        self._add_sums_constraint()
        self._add_single_ship_constraint()
        self._add_ship_implies_constraint()

    def _add_initials_constraint(self):
        for position, value in self._grid:
            match value:
                case BimaruGame._watter:
                    self._solver.add(self._ship(position) == BimaruGame._watter)
                case BimaruGame._ship_single:
                    self._solver.add(self._ship(position) == BimaruGame._ship_single)
                case BimaruGame._ship_top:
                    self._solver.add(self._ship(position) == BimaruGame._ship_top)
                case BimaruGame._ship_bottom:
                    self._solver.add(self._ship(position) == BimaruGame._ship_bottom)
                case BimaruGame._ship_left:
                    self._solver.add(self._ship(position) == BimaruGame._ship_left)
                case BimaruGame._ship_right:
                    self._solver.add(self._ship(position) == BimaruGame._ship_right)
                case BimaruGame._ship_middle_input:
                    self._solver.add(Or(self._ship(position) == BimaruGame._ship_middle_horizontal, self._ship(position) == BimaruGame._ship_middle_vertical))
                case _:
                    self._solver.add(self._ship(position) >= BimaruGame._watter)
                    self._solver.add(self._ship(position) <= BimaruGame._ship_single)

    def _add_sums_constraint(self):
        for index, row in enumerate(self._grid_z3.matrix):
            self._solver.add(Sum([If(row[i] > 0, 1, 0) for i in range(self.columns_number)]) == self.boat_cells['row'][index])

        for index, column_tuple in enumerate(zip(*self._grid_z3.matrix)):
            column = list(column_tuple)
            self._solver.add(Sum([If(column[i] > 0, 1, 0) for i in range(self.rows_number)]) == self.boat_cells['column'][index])

    def total_ships_size(self):
        total = 0
        for size, number in self.boats_number_by_size.items():
            total += size * number
        return total

    def _add_single_ship_constraint(self):
        for position, value in self._grid_z3:
            if value == BimaruGame._ship_single:
                self._solver.add(Or([self._ship(Position(r, c)) == BimaruGame._ship_single for r in range(self.rows_number) for c in range(self.columns_number)]))

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
        self._solver.add(Implies(self._ship(position) == BimaruGame._ship_single, And([self._ship(neighbor_position) == BimaruGame._watter for neighbor_position in self._grid.neighbors_positions(position, "diagonal")])))

    def _add_ship_bottom_implies_constraint(self, position: Position):
        self._solver.add(Implies(self._ship(position) == BimaruGame._ship_bottom, And([self._ship(neighbor_position) == BimaruGame._watter for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.up])))
        if position.up.r > 0:
            self._solver.add(Implies(self._ship(position) == BimaruGame._ship_bottom, Or(self._ship(position.up) == BimaruGame._ship_top, self._ship(position.up) == BimaruGame._ship_middle_vertical)))

    def _add_ship_top_implies_constraint(self, position: Position):
        self._solver.add(Implies(self._ship(position) == BimaruGame._ship_top, And([self._ship(neighbor_position) == BimaruGame._watter for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.down])))
        if position.down.r < self.rows_number - 1:
            self._solver.add(Implies(self._ship(position) == BimaruGame._ship_top, Or(self._ship(position.down) == BimaruGame._ship_bottom, self._ship(position.down) == BimaruGame._ship_middle_vertical)))

    def _add_ship_left_implies_constraint(self, position: Position):
        self._solver.add(Implies(self._ship(position) == BimaruGame._ship_left, And([self._ship(neighbor_position) == BimaruGame._watter for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.right])))
        if position.right.c < self.columns_number - 1:
            self._solver.add(Implies(self._ship(position) == BimaruGame._ship_left, Or(self._ship(position.right) == BimaruGame._ship_right, self._ship(position.right) == BimaruGame._ship_middle_horizontal)))

    def _add_ship_right_implies_constraint(self, position: Position):
        self._solver.add(Implies(self._ship(position) == BimaruGame._ship_right, And([self._ship(neighbor_position) == BimaruGame._watter for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.left])))
        if position.left.c > 0:
            self._solver.add(Implies(self._ship(position) == BimaruGame._ship_right, Or(self._ship(position.left) == BimaruGame._ship_left, self._ship(position.left) == BimaruGame._ship_middle_horizontal)))

    def _add_ship_middle_horizontal_implies_constraint(self, position: Position):
        self._solver.add(Implies(self._ship(position) == BimaruGame._ship_middle_horizontal,
                                 And([self._ship(neighbor_position) == BimaruGame._watter for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.left and neighbor_position != position.right])))
        if position.left.c > 0:
            self._solver.add(Implies(self._ship(position) == BimaruGame._ship_middle_horizontal, Or(self._ship(position.left) == BimaruGame._ship_left, self._ship(position.left) == BimaruGame._ship_middle_horizontal)))
        if position.right.c < self.columns_number - 1:
            self._solver.add(Implies(self._ship(position) == BimaruGame._ship_middle_horizontal, Or(self._ship(position.right) == BimaruGame._ship_right, self._ship(position.right) == BimaruGame._ship_middle_horizontal)))

    def _add_ship_middle_vertical_implies_constraint(self, position: Position):
        self._solver.add(Implies(self._ship(position) == BimaruGame._ship_middle_vertical,
                                 And([self._ship(neighbor_position) == BimaruGame._watter for neighbor_position in self._grid.neighbors_positions(position, "diagonal") if neighbor_position != position.up and neighbor_position != position.down])))
        if position.up.r > 0:
            self._solver.add(Implies(self._ship(position) == BimaruGame._ship_middle_vertical, Or(self._ship(position.up) == BimaruGame._ship_top, self._ship(position.up) == BimaruGame._ship_middle_vertical)))
        if position.down.r < self.rows_number - 1:
            self._solver.add(Implies(self._ship(position) == BimaruGame._ship_middle_vertical, Or(self._ship(position.down) == BimaruGame._ship_bottom, self._ship(position.down) == BimaruGame._ship_middle_vertical)))
