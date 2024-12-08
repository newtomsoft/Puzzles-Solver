from z3 import Solver, sat, Int, And, Not

from Position import Position
from Utils.Grid import Grid


class BimaruGame:
    _watter = 0
    _ship_top = 1
    _ship_bottom = 2
    _ship_left = 3
    _ship_right = 4
    _ship_middle = 5
    _ship_single = 6

    def __init__(self, params: (Grid, dict[str, list[int]], dict[int, int])):
        if BimaruGame._ship_single != 6:
            raise ValueError("Ship single value error")
        self._grid: Grid = params[0]
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.boat_parts: dict[str, list[int]] = params[1]
        self.boats_number_by_size: dict[int, int] = params[2]

        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 6:
            raise ValueError("The grid must be at least 6x6")
        if len(self.boat_parts['column']) != self.columns_number:
            raise ValueError("Boat parts column must have the same length as the columns number")
        if len(self.boat_parts['row']) != self.rows_number:
            raise ValueError("Boat parts row must have the same length as the rows number")
        if not self.boats_number_by_size:
            raise ValueError("At least one boat must be placed")
        if sum(self.boats_number_by_size.values()) != sum(self.boat_parts['column']) or sum(self.boats_number_by_size.values()) != sum(self.boat_parts['row']):
            raise ValueError("The boats number by size must be equal to the sum of boats row / column ")
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

    def _add_initials_constraint(self):
        for position, value in self._grid:
            match value:
                case BimaruGame._watter:
                    self._solver.add(self._ship(position) == BimaruGame._watter)
                    break
                case BimaruGame._ship_single:
                    self._solver.add(self._ship(position) == BimaruGame._ship_single)
                    break
                case BimaruGame._ship_top:
                    self._solver.add(self._ship(position) == BimaruGame._ship_top)
                    break
                case BimaruGame._ship_bottom:
                    self._solver.add(self._ship(position) == BimaruGame._ship_bottom)
                    break
                case BimaruGame._ship_left:
                    self._solver.add(self._ship(position) == BimaruGame._ship_left)
                    break
                case BimaruGame._ship_right:
                    self._solver.add(self._ship(position) == BimaruGame._ship_right)
                    break
                case BimaruGame._ship_middle:
                    self._solver.add(self._ship(position) == BimaruGame._ship_middle)
                    break
                case _:
                    self._solver.add(self._ship(position) > BimaruGame._watter)
                    self._solver.add(self._ship(position) <= BimaruGame._ship_single)
                    break

    def _add_sums_constraint(self):
        for position, level_value in self._grid:
            self._solver.add(self._ship(position) >= 1)
            self._solver.add(self._ship(position) <= self.columns_number)
