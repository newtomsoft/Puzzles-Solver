from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class GappySolver(GameSolver):
    def __init__(self, gaps: list[list[int]]):
        self._rows_gaps = gaps[0]
        self._columns_gaps = gaps[1]
        self._rows_number = len(self._rows_gaps)
        self._columns_number = len(self._columns_gaps)
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_vars = Grid(
            [[self._model.new_bool_var(f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()
        solution = self._compute_solution()
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        if self._previous_solution is None:
            return Grid.empty()
        previous_black_positions = [pos for pos, val in self._previous_solution if val]
        self._model.add_bool_or([self._grid_vars[pos].negated() for pos in previous_black_positions])
        return self.get_solution()

    def _compute_solution(self) -> Grid:
        status = self._solver.solve(self._model)
        if status in {cp_model.OPTIMAL, cp_model.FEASIBLE}:
            return Grid([[self._solver.boolean_value(self._grid_vars.value(r, c)) for c in range(self._columns_number)] for r in range(self._rows_number)])
        return Grid.empty()

    def _add_constraints(self):
        self._add_2_black_cells_by_line_constraints()
        self._add_isolated_black_cells_constraints()
        self._add_gaps_constraints()

    def _add_2_black_cells_by_line_constraints(self):
        for row in self._grid_vars.matrix:
            self._model.add(sum(row) == 2)
        for column in zip(*self._grid_vars.matrix):
            self._model.add(sum(column) == 2)

    def _add_isolated_black_cells_constraints(self):
        for position, cell_var in self._grid_vars:
            neighbors = self._grid_vars.neighbors_positions(position, 'diagonal')
            for neighbor in neighbors:
                self._model.add(cell_var + self._grid_vars[neighbor] <= 1)

    def _add_gaps_constraints(self):
        for index_row, row in enumerate(self._grid_vars.matrix):
            self._add_line_gap_constraint(row, self._rows_number, self._rows_gaps[index_row], f"r{index_row}")
        for index_column, column in enumerate(zip(*self._grid_vars.matrix)):
            self._add_line_gap_constraint(list(column), self._columns_number, self._columns_gaps[index_column], f"c{index_column}")

    def _add_line_gap_constraint(self, line, line_size, gap, name):
        if gap == -1:
            return
        start_vars = []
        for i in range(line_size - gap - 1):
            start_var = self._model.new_bool_var(f"gap_{name}_{i}")
            self._model.add(line[i] == 1).only_enforce_if(start_var)
            self._model.add(line[i + gap + 1] == 1).only_enforce_if(start_var)
            for j in range(line_size):
                if j != i and j != i + gap + 1:
                    self._model.add(line[j] == 0).only_enforce_if(start_var)
            start_vars.append(start_var)
        self._model.add_bool_or(start_vars)
