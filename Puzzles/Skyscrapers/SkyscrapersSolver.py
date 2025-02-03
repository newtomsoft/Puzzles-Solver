from z3 import Distinct, ArithRef

from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Grid import Grid
from Utils.Position import Position


class SkyscrapersSolver(GameSolver):
    _no_value = 0

    def __init__(self, grid: Grid, visible_skyscrapers: dict[str, list[int]], solver_engine: SolverEngine):
        self._grid: Grid = grid
        self.visible_skyscrapers: dict[str, list[int]] = visible_skyscrapers
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.highest_skyscraper_levels = self.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        if len(self.visible_skyscrapers['by_east']) != self.columns_number:
            raise ValueError("The 'by_east' viewable skyscrapers list must have the same length as the rows number")
        if len(self.visible_skyscrapers['by_west']) != self.columns_number:
            raise ValueError("The 'by_west' viewable skyscrapers list must have the same length as the rows number")
        if len(self.visible_skyscrapers['by_north']) != self.rows_number:
            raise ValueError("The 'by_north' viewable skyscrapers list must have the same length as the columns number")
        if len(self.visible_skyscrapers['by_south']) != self.rows_number:
            raise ValueError("The 'by_south' viewable skyscrapers list must have the same length as the columns number")
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._last_solution_grid = None

    def _init_solver(self):
        self._grid_z3 = Grid([[self._solver.int(f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.has_constraints():
            self._init_solver()
        if not self._solver.has_solution():
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._level_at(Position(r, c))).as_long() for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._last_solution_grid = grid
        return grid

    def get_other_solution(self):
        exclusion_constraint = self._solver.Not(self._solver.And([self._level_at(Position(r, c)) == self._last_solution_grid[Position(r, c)] for r in range(self.rows_number) for c in range(self.columns_number) if self._last_solution_grid.value(r, c)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _level_at(self, position):
        return self._grid_z3[position]

    def _add_constraints(self):
        self._add_initials_levels_constraint()
        self._add_range_levels_constraint()
        self._add_distinct_level_constraint()
        self._add_visible_skyscrapers_constraint()

    def _add_initials_levels_constraint(self):
        for position, level_value in self._grid:
            if level_value != self._no_value:
                self._solver.add(self._level_at(position) == level_value)

    def _add_range_levels_constraint(self):
        for position, level_value in self._grid:
            self._solver.add(self._level_at(position) >= 1)
            self._solver.add(self._level_at(position) <= self.columns_number)

    def _add_distinct_level_constraint(self):
        constraints = []
        for row in self._grid_z3.matrix:
            constraints.append(Distinct([row[j] for j in range(self.columns_number)]))
        for column in zip(*self._grid_z3.matrix):
            constraints.append(Distinct([column[j] for j in range(self.rows_number)]))
        self._solver.add(constraints)

    def _add_visible_skyscrapers_constraint(self):
        for index, row in enumerate(self._grid_z3.matrix):
            self._solver.add(self._visible_skyscrapers_constraint(self.visible_skyscrapers['by_west'][index], row))
            self._solver.add(self._visible_skyscrapers_constraint(self.visible_skyscrapers['by_east'][index], self._reversed(row)))

        for index, column_tuple in enumerate(zip(*self._grid_z3.matrix)):
            column = list(column_tuple)
            self._solver.add(self._visible_skyscrapers_constraint(self.visible_skyscrapers['by_north'][index], column))
            self._solver.add(self._visible_skyscrapers_constraint(self.visible_skyscrapers['by_south'][index], self._reversed(column)))

    def _visible_skyscrapers_constraint(self, visible_skyscrapers: int, line: list[ArithRef], height_base=None):
        if visible_skyscrapers == 0:
            return True

        if height_base is None:
            height_base = line[0]

        if visible_skyscrapers == 1:
            return self._one_visible_skyscraper_constraint(line, height_base)

        if len(line) == 1:
            return False

        sub_line = line[1:]
        line1_sup_line0_constraint = self._solver.And(line[1] > height_base, self._visible_skyscrapers_constraint(visible_skyscrapers - 1, sub_line, line[1]))
        line1_inf_line0_constraint = self._solver.And(line[1] < height_base, self._visible_skyscrapers_constraint(visible_skyscrapers, sub_line, height_base))

        return self._solver.Or(line1_sup_line0_constraint, line1_inf_line0_constraint)

    @staticmethod
    def _reversed(line: list) -> list:
        return line[::-1]

    def _one_visible_skyscraper_constraint(self, line, highest_skyscraper_levels):
        index0_constraint = line[0] == highest_skyscraper_levels
        others_indexes_constraint = self._solver.And([line[i] < line[0] for i in range(1, len(line))])
        return self._solver.And(index0_constraint, others_indexes_constraint)
