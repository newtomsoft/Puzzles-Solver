from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class PutteriaSolver(GameSolver):
    cell_empty = 0
    cross = -1

    def __init__(self, regions_grid: Grid, clues_grid: Grid):
        self._regions_grid = regions_grid
        self._clues_grid = clues_grid
        self.rows_number = self._regions_grid.rows_number
        self.columns_number = self._regions_grid.columns_number
        self._regions = self._regions_grid.get_regions()
        self._region_sizes = {region_id: len(cells) for region_id, cells in self._regions.items()}
        self._cell_region = {}
        for region_id, cells in self._regions.items():
            for pos in cells:
                self._cell_region[pos] = region_id
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = Grid.empty()
        self._status = None

    def get_solution(self) -> Grid:
        self._grid_vars = [[self._model.new_bool_var(f"has_number_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()
        self._status = self._solver.solve(self._model)
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()
        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        current_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                var = self._grid_vars[r][c]
                if self._solver.boolean_value(var):
                    current_vars.append(var.negated())
                else:
                    current_vars.append(var)
        self._model.add_bool_or(current_vars)

        self._status = self._solver.solve(self._model)
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()
        return self._compute_solution()

    def _compute_solution(self):
        matrix = []
        for r in range(self.rows_number):
            row = []
            for c in range(self.columns_number):
                pos = Position(r, c)
                if self._solver.value(self._grid_vars[r][c]):
                    row.append(self._region_sizes[self._cell_region[pos]])
                else:
                    row.append(0)
            matrix.append(row)
        return Grid(matrix)

    def _add_constraints(self):
        self._add_clue_constraints()
        self._add_cross_constraints()
        self._add_one_number_per_region_constraints()
        self._add_no_adjacent_numbers_constraints()
        self._add_no_duplicate_in_row_constraints()
        self._add_no_duplicate_in_column_constraints()

    def _add_clue_constraints(self):
        for position, value in [(position, value) for position, value in self._clues_grid if value != self.empty and value != self.cross]:
            expected_size = self._region_sizes[self._cell_region[position]]
            if value != expected_size:
                raise ValueError(f"Clue at {position} has value {value}, but region size is {expected_size}")
            self._model.add(self._grid_vars[position.r][position.c] == 1)

    def _add_cross_constraints(self):
        for position, value in [(position, value) for position, value in self._clues_grid if value == self.cross]:
            self._model.add(self._grid_vars[position.r][position.c] == 0)

    def _add_one_number_per_region_constraints(self):
        for region_id, cells in self._regions.items():
            self._model.add(sum(self._grid_vars[pos.r][pos.c] for pos in cells) == 1)

    def _add_no_adjacent_numbers_constraints(self):
        for position, _ in self._regions_grid:
            for neighbor in self._regions_grid.neighbors_positions(position):
                if neighbor.r > position.r or neighbor.c > position.c:
                    self._model.add(self._grid_vars[position.r][position.c] + self._grid_vars[neighbor.r][neighbor.c] <= 1)

    def _add_no_duplicate_in_row_constraints(self):
        for r in range(self.rows_number):
            cells_by_size = {}
            for c in range(self.columns_number):
                pos = Position(r, c)
                size = self._region_sizes[self._cell_region[pos]]
                cells_by_size.setdefault(size, []).append(pos)
            for size, cells in cells_by_size.items():
                if len(cells) > 1:
                    self._model.add(sum(self._grid_vars[pos.r][pos.c] for pos in cells) <= 1)

    def _add_no_duplicate_in_column_constraints(self):
        for c in range(self.columns_number):
            cells_by_size = {}
            for r in range(self.rows_number):
                pos = Position(r, c)
                size = self._region_sizes[self._cell_region[pos]]
                cells_by_size.setdefault(size, []).append(pos)
            for size, cells in cells_by_size.items():
                if len(cells) > 1:
                    self._model.add(sum(self._grid_vars[pos.r][pos.c] for pos in cells) <= 1)
