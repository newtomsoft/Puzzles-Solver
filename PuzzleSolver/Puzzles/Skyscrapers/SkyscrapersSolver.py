from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class SkyscrapersSolver(GameSolver):
    _no_value = 0

    def __init__(self, grid: Grid, visible_skyscrapers: dict[str, list[int]]):
        super().__init__()
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
        self._model = cp_model.CpModel()
        self._grid_vars: Grid | None = None
        self._previous_solution_grid = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.new_int_var(1, self.columns_number, f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._model.Proto().constraints:
            self._init_solver()

        status = self._solver.solve(self._model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            grid = Grid([[self._solver.value(self._level_at(Position(r, c))) for c in range(self.columns_number)] for r in range(self.rows_number)])
            self._previous_solution_grid = grid
            return grid
        else:
            return Grid.empty()

    def get_other_solution(self):
        if self._previous_solution_grid is None:
            return Grid.empty()

        previous_solution_bools = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._previous_solution_grid.value(r, c) != self._no_value:
                    is_same = self._model.new_bool_var(f"is_same_{r}_{c}")
                    self._model.add(self._level_at(Position(r, c)) == self._previous_solution_grid.value(r, c)).only_enforce_if(is_same)
                    self._model.add(self._level_at(Position(r, c)) != self._previous_solution_grid.value(r, c)).only_enforce_if(is_same.negated())
                    previous_solution_bools.append(is_same)

        if previous_solution_bools:
            all_same = self._model.new_bool_var("all_same")
            self._model.add_bool_and(previous_solution_bools).only_enforce_if(all_same)
            self._model.add_bool_or([b.negated() for b in previous_solution_bools]).only_enforce_if(all_same.negated())
            self._model.add(all_same == 0)

        return self.get_solution()

    def _level_at(self, position):
        return self._grid_vars[position]

    def _add_constraints(self):
        self._add_initials_levels_constraint()
        self._add_distinct_level_constraint()
        self._add_visible_skyscrapers_constraint()

    def _add_initials_levels_constraint(self):
        for position, level_value in self._grid:
            if level_value != self._no_value:
                self._model.add(self._level_at(position) == level_value)

    def _add_distinct_level_constraint(self):
        for r in range(self.rows_number):
            row_vars = [self._level_at(Position(r, c)) for c in range(self.columns_number)]
            self._model.add_all_different(row_vars)

        for c in range(self.columns_number):
            col_vars = [self._level_at(Position(r, c)) for r in range(self.rows_number)]
            self._model.add_all_different(col_vars)

    def _add_visible_skyscrapers_constraint(self):
        for index in range(self.rows_number):
            row = [self._level_at(Position(index, c)) for c in range(self.columns_number)]
            self._add_visible_count_constraint(self.visible_skyscrapers['by_west'][index], row)
            self._add_visible_count_constraint(self.visible_skyscrapers['by_east'][index], self._reversed(row))

        for index in range(self.columns_number):
            column = [self._level_at(Position(r, index)) for r in range(self.rows_number)]
            self._add_visible_count_constraint(self.visible_skyscrapers['by_north'][index], column)
            self._add_visible_count_constraint(self.visible_skyscrapers['by_south'][index], self._reversed(column))

    def _add_visible_count_constraint(self, visible_count: int, line: list):
        if visible_count == 0:
            return  # No constraint needed

        is_visible = []
        for i in range(len(line)):
            is_visible.append(self._model.new_bool_var(f"is_visible_{i}"))

        self._model.add(is_visible[0] == 1)

        for i in range(1, len(line)):
            is_taller = []
            for j in range(i):
                is_taller_than_j = self._model.new_bool_var(f"is_taller_{i}_{j}")
                self._model.add(line[i] > line[j]).only_enforce_if(is_taller_than_j)
                self._model.add(line[i] <= line[j]).only_enforce_if(is_taller_than_j.negated())
                is_taller.append(is_taller_than_j)

            all_taller = self._model.new_bool_var(f"all_taller_{i}")
            self._model.add_bool_and(is_taller).only_enforce_if(all_taller)
            self._model.add_bool_or([b.negated() for b in is_taller]).only_enforce_if(all_taller.negated())

            self._model.add(is_visible[i] == all_taller)

        self._model.add(sum(is_visible) == visible_count)

    @staticmethod
    def _reversed(line: list) -> list:
        return line[::-1]
