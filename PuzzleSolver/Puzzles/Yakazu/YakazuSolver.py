from typing import Literal

from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver

TypeLine = Literal["row", "column"]


class YakazuSolver(GameSolver):
    def __init__(self, numbers_grid: Grid[int], blacks_grid: Grid[bool]):
        super().__init__()
        self._numbers_grid = numbers_grid
        self._blacks_grid = blacks_grid
        self._rows_number = self._numbers_grid.rows_number
        self._columns_number = self._numbers_grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_var: Grid = Grid.empty()
        self._previous_solution: Grid = Grid.empty()

    def get_solution(self) -> Grid:
        max_abs = self._rows_number * self._columns_number
        self._grid_var = Grid([[self._model.new_int_var(-max_abs, max_abs, f"grid_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        eq_vars = []
        for position, value in [(position, value) for position, value in self._previous_solution if value > 0]:
            b = self._model.new_bool_var(f"block_{position.r}_{position.c}")
            self._model.add(self._grid_var[position] == value).OnlyEnforceIf(b)
            self._model.add(self._grid_var[position] != value).OnlyEnforceIf(b.Not())
            eq_vars.append(b)
        self._model.add(sum(eq_vars) <= len(eq_vars) - 1)
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        status = self._solver.Solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()
        solution = Grid([[self._solver.Value(self._grid_var.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
        return solution

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_group_constraints()

    def _add_initial_constraints(self):
        max_value = min(self._rows_number, self._columns_number)
        for position, value in [(position, value) for position, value in self._numbers_grid]:
            if self._blacks_grid[position]:
                self._model.add(self._grid_var[position] == 0)
            elif value != GameSolver.cell_empty:
                self._model.add(self._grid_var[position] == value)
            else:
                self._model.add(self._grid_var[position] >= 1)
                self._model.add(self._grid_var[position] <= max_value)

    def _add_group_constraints(self):
        self._add_horizontal_group_constraints()
        self._add_vertical_group_constraints()

    def _add_vertical_group_constraints(self):
        for col_index in range(self._columns_number):
            column = [self._grid_var[r][col_index] for r in range(self._rows_number)]
            groups = self._build_groups(col_index, column, "column")
            for group in groups:
                if len(group) >= 2:
                    self._add_group_constraint(group)

    def _add_horizontal_group_constraints(self):
        for row_index, row in enumerate(self._grid_var.matrix):
            groups = self._build_groups(row_index, row, "row")
            for group in groups:
                if len(group) >= 2:
                    self._add_group_constraint(group)

    def _build_groups(self, line_index: int, line: list, type_line: TypeLine = "row"):
        groups = []
        current_group = []
        for i, cell in enumerate(line):
            position = Position(line_index, i) if type_line == "row" else Position(i, line_index)
            if self._blacks_grid[position]:
                if current_group:
                    groups.append(current_group)
                    current_group = []
            else:
                current_group.append(cell)
        if current_group:
            groups.append(current_group)
        return groups

    def _add_group_constraint(self, cells: list):
        self._model.add_min_equality(1, cells)
        self._model.add_max_equality(len(cells), cells)
        self._model.add_all_different(cells)
