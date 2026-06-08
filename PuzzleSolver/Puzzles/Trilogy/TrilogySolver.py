from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver

class TrilogySolver(GameSolver):
    def __init__(self, grid: Grid[int]):
        super().__init__()
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[self._model.new_int_var(1, 3, f"grid_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        eq_vars = []
        for position, value in [(position, value) for position, value in self._previous_solution if value > 0]:
            b = self._model.new_bool_var(f"block_{position.r}_{position.c}")
            self._model.Add(self._grid_z3[position] == value).OnlyEnforceIf(b)
            self._model.Add(self._grid_z3[position] != value).OnlyEnforceIf(b.Not())
            eq_vars.append(b)
        self._model.Add(sum(eq_vars) <= len(eq_vars) - 1)
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        status = self._solver.Solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()
        solution = Grid([[self._solver.Value(self._grid_z3[Position(i, j)]) for j in range(self._columns_number)] for i in range(self._rows_number)])
        return solution

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_row_constraints()
        self._add_columns_constraints()
        self._add_up_right_diagonals_constraints()
        self._add_up_left_diagonals_constraints()

    def _add_initial_constraints(self):
        for position, value in [(position, value) for position, value in self._grid if value > 0]:
            self._model.Add(self._grid_z3[position] == value)
        for position, value in [(position, value) for position, value in self._grid if value == 0]:
            self._model.Add(self._grid_z3[position] > 0)
            self._model.Add(self._grid_z3[position] < 4)

    def _add_row_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number - 2):
                first_position = Position(r, c)
                second_position = Position(r, c + 1)
                third_position = Position(r, c + 2)
                self._add_not_same_constraint(first_position, second_position, third_position)
                self._add_not_all_different_constraint(first_position, second_position, third_position)

    def _add_columns_constraints(self):
        for r in range(self._rows_number - 2):
            for c in range(self._columns_number):
                first_position = Position(r, c)
                second_position = Position(r + 1, c)
                third_position = Position(r + 2, c)
                self._add_not_same_constraint(first_position, second_position, third_position)
                self._add_not_all_different_constraint(first_position, second_position, third_position)

    def _add_up_right_diagonals_constraints(self):
        for r in range(2, self._rows_number):
            for c in range(self._columns_number - 2):
                first_position = Position(r, c)
                second_position = Position(r - 1, c + 1)
                third_position = Position(r - 2, c + 2)
                self._add_not_same_constraint(first_position, second_position, third_position)
                self._add_not_all_different_constraint(first_position, second_position, third_position)

    def _add_up_left_diagonals_constraints(self):
        for r in range(2, self._rows_number):
            for c in range(2, self._columns_number):
                first_position = Position(r, c)
                second_position = Position(r - 1, c - 1)
                third_position = Position(r - 2, c - 2)
                self._add_not_same_constraint(first_position, second_position, third_position)
                self._add_not_all_different_constraint(first_position, second_position, third_position)

    def _add_not_all_different_constraint(self, a, b, c):
        eq_ab = self._model.new_bool_var(f"eq_{a.r}_{a.c}_{b.r}_{b.c}")
        eq_ac = self._model.new_bool_var(f"eq_{a.r}_{a.c}_{c.r}_{c.c}")
        eq_bc = self._model.new_bool_var(f"eq_{b.r}_{b.c}_{c.r}_{c.c}")
        self._model.Add(self._grid_z3[a] == self._grid_z3[b]).OnlyEnforceIf(eq_ab)
        self._model.Add(self._grid_z3[a] != self._grid_z3[b]).OnlyEnforceIf(eq_ab.Not())
        self._model.Add(self._grid_z3[a] == self._grid_z3[c]).OnlyEnforceIf(eq_ac)
        self._model.Add(self._grid_z3[a] != self._grid_z3[c]).OnlyEnforceIf(eq_ac.Not())
        self._model.Add(self._grid_z3[b] == self._grid_z3[c]).OnlyEnforceIf(eq_bc)
        self._model.Add(self._grid_z3[b] != self._grid_z3[c]).OnlyEnforceIf(eq_bc.Not())
        self._model.AddBoolOr([eq_ab, eq_ac, eq_bc])

    def _add_not_same_constraint(self, a, b, c):
        eq_ab = self._model.new_bool_var(f"notsame_eq_{a.r}_{a.c}_{b.r}_{b.c}")
        eq_ac = self._model.new_bool_var(f"notsame_eq_{a.r}_{a.c}_{c.r}_{c.c}")
        self._model.Add(self._grid_z3[a] == self._grid_z3[b]).OnlyEnforceIf(eq_ab)
        self._model.Add(self._grid_z3[a] != self._grid_z3[b]).OnlyEnforceIf(eq_ab.Not())
        self._model.Add(self._grid_z3[a] == self._grid_z3[c]).OnlyEnforceIf(eq_ac)
        self._model.Add(self._grid_z3[a] != self._grid_z3[c]).OnlyEnforceIf(eq_ac.Not())
        self._model.AddBoolOr([eq_ab.Not(), eq_ac.Not()])
