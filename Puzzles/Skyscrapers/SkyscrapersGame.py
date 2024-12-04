from z3 import Solver, sat, Int, Distinct, Implies, And, Not, Or

from Utils.Grid import Grid


class SkyscrapersGame:
    _no_value = 0

    def __init__(self, params: (Grid, dict[str, list[int]])):
        self._grid: Grid = params[0]
        self.viewable_skyscrapers: dict[str, list[int]] = params[1]
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.biggest_skyscraper_levels = self.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        self.by_east_viewable_skyscrapers = self.viewable_skyscrapers['by_east']
        if len(self.by_east_viewable_skyscrapers) != self.columns_number:
            raise ValueError("The 'by_east' viewable skyscrapers list must have the same length as the rows number")
        self.by_west_viewable_skyscrapers = self.viewable_skyscrapers['by_west']
        if len(self.by_west_viewable_skyscrapers) != self.columns_number:
            raise ValueError("The 'by_west' viewable skyscrapers list must have the same length as the rows number")
        self.by_north_viewable_skyscrapers = self.viewable_skyscrapers['by_north']
        if len(self.by_north_viewable_skyscrapers) != self.rows_number:
            raise ValueError("The 'by_north' viewable skyscrapers list must have the same length as the columns number")
        self.by_south_viewable_skyscrapers = self.viewable_skyscrapers['by_south']
        if len(self.by_south_viewable_skyscrapers) != self.rows_number:
            raise ValueError("The 'by_south' viewable skyscrapers list must have the same length as the columns number")
        self._solver = None
        self._grid_z3: Grid = Grid.empty()
        self._last_solution_grid = None

    def _init_solver(self):
        self._matrix_z3 = [[Int(f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._grid_z3 = Grid(self._matrix_z3)
        self._solver = Solver()
        self._add_constraints()

    def get_solution(self) -> Grid | None:
        if self._solver is None:
            self._init_solver()
        if self._solver.check() != sat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._matrix_z3[i][j]).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)])
        self._last_solution_grid = grid
        return grid

    def get_other_solution(self):
        self._exclude_solution(self._last_solution_grid)
        solution = self.get_solution()
        return solution

    def _exclude_solution(self, solution_grid: Grid):
        exclude_constraint = Not(And([self._matrix_z3[r][c] == solution_grid.value(r, c) for r in range(self.rows_number) for c in range(self.columns_number) if solution_grid.value(r, c)]))
        self._solver.add(exclude_constraint)

    def _add_constraints(self):
        self._add_initials_levels_constraint()
        self._add_range_levels_constraint()
        self._add_distinct_level_constraint()
        self._add_viewable_skyscrapers_constraint()

    def level(self, position):
        return self._grid_z3[position]

    def _add_initials_levels_constraint(self):
        for position, level_value in self._grid:
            if level_value != self._no_value:
                self._solver.add(self.level(position) == level_value)

    def _add_range_levels_constraint(self):
        for position, level_value in self._grid:
            self._solver.add(self.level(position) >= 1)
            self._solver.add(self.level(position) <= self.columns_number)

    def _add_distinct_level_constraint(self):
        constraints = []
        for row in self._grid_z3.matrix:
            constraints.append(Distinct([row[j] for j in range(self.columns_number)]))
        for column in zip(*self._grid_z3.matrix):
            constraints.append(Distinct([column[j] for j in range(self.rows_number)]))
        self._solver.add(constraints)

    def _add_viewable_skyscrapers_constraint(self):
        for r, row in enumerate(self._grid_z3.matrix):
            self._add_viewable_skyscrapers_constraint_for_this_view(row[::-1], self.by_east_viewable_skyscrapers[r])
            self._add_viewable_skyscrapers_constraint_for_this_view(row, self.by_west_viewable_skyscrapers[r])
            pass

        for c, column in enumerate(zip(*self._grid_z3.matrix)):
            self._add_viewable_skyscrapers_constraint_for_this_view(column, self.by_north_viewable_skyscrapers[c])
            self._add_viewable_skyscrapers_constraint_for_this_view(column[::-1], self.by_south_viewable_skyscrapers[c])

    def _add_viewable_skyscrapers_constraint_for_this_view(self, line, viewable_skyscrapers: int):
        if viewable_skyscrapers == 0:
            return

        if viewable_skyscrapers == 1:
            self._solver.add(line[0] == self.biggest_skyscraper_levels)
            return

        if viewable_skyscrapers == self.biggest_skyscraper_levels:
            self._solver.add([line[i] == i + 1 for i in range(self.columns_number)])
            return

        if viewable_skyscrapers == 2:
            self._solver.add(line[0] != self.biggest_skyscraper_levels)
            constraints = set()
            first_to_or = line[1] == self.biggest_skyscraper_levels
            for i in range(2, self.columns_number):
                constraints.add(And([line[i] == self.biggest_skyscraper_levels, And([line[0] > line[j] for j in range(1, i)])]))
            constraints.add(first_to_or)
            self._solver.add(Or(constraints))
            return

        if viewable_skyscrapers == self.biggest_skyscraper_levels - 1:
            self._solver.add([line[i] != self.biggest_skyscraper_levels for i in range(2)])
            self._solver.add(Implies(line[-2] == self.biggest_skyscraper_levels, And([line[i + 1] > line[i] for i in range(self.columns_number - 2)])))
            self._solver.add(Implies(line[-1] == self.biggest_skyscraper_levels, self._all_increase_except_one(line[:-1])))
            return

    def _all_increase_except_one(self, line):
        constraints = set()
        for i_less in range(len(line) - 1):
            constraint_to_and = [line[i] < line[i + 1] for i in range(self.columns_number - 2) if i != i_less]
            constraint_to_and.append(line[i_less] > line[i_less + 1])
            constraints.add(And(constraint_to_and))
        return Or(constraints)
