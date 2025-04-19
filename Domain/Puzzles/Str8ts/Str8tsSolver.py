from Domain.Board.Position import Position
from Domain.Board.Grid import Grid
from Domain.Ports.SolverEngine import SolverEngine


class Str8tsSolver:
    def __init__(self, numbers_grid: Grid[int], blacks_grid: Grid[bool], solver_engine: SolverEngine):
        self._numbers_grid = numbers_grid
        self._blacks_grid = blacks_grid
        self._rows_number = self._numbers_grid.rows_number
        self._columns_number = self._numbers_grid.columns_number
        if self._rows_number != self._columns_number:
            raise ValueError("Str8ts has to be a square")
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> (Grid, int):
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[position] == value for position, value in self._previous_solution if value > 0])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if not self._solver.has_solution():
            return Grid.empty()
        solution_with_black_negative = Grid([[(self._solver.eval(self._grid_z3.value(i, j))) for j in range(self._columns_number)] for i in range(self._rows_number)])
        solution = Grid([[max(0, solution_with_black_negative.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
        return solution

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_distinct_constraints()
        self._add_consecutive_constraints()

    def _add_initial_constraints(self):
        for position, value in [(position, value) for position, value in self._numbers_grid if value > 0]:
            self._solver.add(self._grid_z3[position] == value)

        black_count = 0
        for position, is_black in self._blacks_grid:
            if is_black and self._numbers_grid[position] == 0:
                black_count += 1
                self._solver.add(self._grid_z3[position] == -black_count)
            else:
                self._solver.add(self._grid_z3[position] > 0)
                self._solver.add(self._grid_z3[position] <= self._rows_number)

    def _add_distinct_constraints(self):
        for index, row in enumerate(self._grid_z3.matrix):
            self._solver.add(self._solver.distinct(row))

        for index, column_tuple in enumerate(zip(*self._grid_z3.matrix)):
            column = list(column_tuple)
            self._solver.add(self._solver.distinct(column))

    def _add_consecutive_constraints(self):
        for column_index, row in enumerate(self._grid_z3.matrix):
            groups = self._build_groups(column_index, row, "row")
            self.add_consecutive_for_groups_constraints(groups)

        for row_index, column_tuple in enumerate(zip(*self._grid_z3.matrix)):
            column = list(column_tuple)
            groups = self._build_groups(row_index, column, "column")
            self.add_consecutive_for_groups_constraints(groups)

    def _build_groups(self, line_index: int, line: list, type_line: str = "column"):
        groups = []
        current_group = []
        for other_line_type_index, cell in enumerate(line):
            position = Position(other_line_type_index, line_index) if type_line == "column" else Position(line_index, other_line_type_index)
            if self._blacks_grid[position]:
                if current_group:
                    groups.append(current_group)
                    current_group = []
            else:
                current_group.append(cell)
        if current_group:
            groups.append(current_group)
        return groups

    def add_consecutive_for_groups_constraints(self, groups: list[list]):
        for cells in groups:
            if len(cells) < 2:
                continue
            self.add_consecutive_constraint(cells)

    def add_consecutive_constraint(self, cells: list):
        for index_cell, cell_0 in enumerate(cells):
            constraints = []
            for cell_i in [cells[i] for i in range(len(cells)) if i != index_cell]:
                constraints.append(self._solver.abs(cell_0 - cell_i) == 1)
            self._solver.add(self._solver.Or(constraints))
