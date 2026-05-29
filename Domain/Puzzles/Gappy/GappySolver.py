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
        self._solver_initialized = False
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid(
            [[self._model.NewBoolVar(f"cell_{r}-{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver_initialized:
            self._init_solver()
            self._solver_initialized = True

        solution = self._compute_solution()
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        previous_solution_constraints = []
        for position, _ in [(position, value) for (position, value) in self._previous_solution if value]:
            previous_solution_constraints.append(self._grid_z3[position])
        self._model.AddBoolOr([v.Not() for v in previous_solution_constraints])
        return self.get_solution()

    def _compute_solution(self) -> Grid:
        if self._solver.Solve(self._model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid([[bool(self._solver.Value(self._grid_z3.value(i, j))) for j in range(self._columns_number)] for i in range(self._rows_number)])

        return Grid.empty()

    def _add_constraints(self):
        self._add_2_black_cells_by_line_constraints()
        self._add_isolated_black_cells_constraints()
        self._add_gaps_constraints()

    def _add_2_black_cells_by_line_constraints(self):
        for row_z3 in self._grid_z3.matrix:
            self._model.Add(sum(row_z3[c] for c in range(self._columns_number)) == 2)
        for column_z3 in zip(*self._grid_z3.matrix):
            self._model.Add(sum(column_z3[r] for r in range(self._rows_number)) == 2)

    def _add_isolated_black_cells_constraints(self):
        for position, value in self._grid_z3:
            neighbors_values = self._grid_z3.neighbors_values(position, 'diagonal')
            self._model.Add(sum(neighbors_values) == 0).OnlyEnforceIf(value)

    def _add_gaps_constraints(self):
        for index_row, row_z3 in enumerate(self._grid_z3.matrix):
            self._add_line_gap_constraint(row_z3, self._rows_number, self._rows_gaps[index_row])

        for index_column, column_z3 in enumerate(zip(*self._grid_z3.matrix)):
            self._add_line_gap_constraint(column_z3, self._columns_number, self._columns_gaps[index_column])

    def _add_line_gap_constraint(self, line_z3, line_size, gap):
        if gap == -1:
            return
        pattern_bools = []
        for index in range(line_size - gap - 1):
            b = self._model.NewBoolVar(f"pattern_{index}")
            conditions = [line_z3[index], line_z3[index + gap + 1]]
            conditions.extend([line_z3[i].Not() for i in range(line_size) if i != index and i != index + gap + 1])
            self._model.AddBoolAnd(conditions).OnlyEnforceIf(b)
            pattern_bools.append(b)
        self._model.AddBoolOr(pattern_bools)
