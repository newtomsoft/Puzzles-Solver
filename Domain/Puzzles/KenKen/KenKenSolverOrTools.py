import uuid

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class KenKenSolverOrTools(GameSolver):
    def __init__(self, regions_operators_results: list):
        self._regions_operators_results = regions_operators_results
        self.rows_number, self.columns_number = self._get_rows_columns_number()
        if self.rows_number != self.columns_number:
            raise ValueError("KenKen grid must be square")
        self._grid_vars = None
        self._model = cp_model.CpModel()
        self._previous_solution = None

    def get_solution(self) -> (Grid | None, int):
        self._grid_vars = Grid([[self._model.NewIntVar(1, self.rows_number, f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        self._previous_solution = Grid([[solver.Value(self._grid_vars.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return self._previous_solution

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()
        if self._previous_solution.is_empty():
            return Grid.empty()

        uuid_str = str(uuid.uuid4())
        bool_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                prev_val = self._previous_solution.value(r, c)
                diff_var = self._model.NewBoolVar(f"diff_r{r}_c{c}_{uuid_str}")
                self._model.Add(self._grid_vars[Position(r, c)] != prev_val).OnlyEnforceIf(diff_var)
                self._model.Add(self._grid_vars[Position(r, c)] == prev_val).OnlyEnforceIf(diff_var.Not())
                bool_vars.append(diff_var)

        self._model.AddBoolOr(bool_vars)

        return self._compute_solution()

    def _add_constraints(self):
        self._initials_constraints()
        self._add_distinct_in_rows_and_columns_constraints()
        self._add_operations_add_constraints()
        self._add_operations_sub_constraints()
        # Multiplication and division constraints are intentionally ignored

    def _initials_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                self._model.Add(self._grid_vars[Position(r, c)] >= 1)
                self._model.Add(self._grid_vars[Position(r, c)] <= self.rows_number)

    def _add_distinct_in_rows_and_columns_constraints(self):
        for r in range(self.rows_number):
            self._model.AddAllDifferent([self._grid_vars[Position(r, c)] for c in range(self.columns_number)])
        for c in range(self.columns_number):
            self._model.AddAllDifferent([self._grid_vars[Position(r, c)] for r in range(self.rows_number)])

    def _add_operations_add_constraints(self):
        for region, operator_str, result in self._regions_operators_results:
            if operator_str == '+':
                self._model.Add(sum([self._grid_vars[position] for position in region]) == result)

    def _add_operations_sub_constraints(self):
        for region, operator_str, result in self._regions_operators_results:
            if operator_str == '-':
                if len(region) != 2:
                    raise ValueError("Subtraction can only be applied to two positions")

                a = self._grid_vars[region[0]]
                b = self._grid_vars[region[1]]

                case1 = self._model.NewBoolVar(f"sub_case1_{region[0].r}_{region[0].c}_{region[1].r}_{region[1].c}")
                case2 = self._model.NewBoolVar(f"sub_case2_{region[0].r}_{region[0].c}_{region[1].r}_{region[1].c}")

                self._model.Add(a - b == result).OnlyEnforceIf(case1)
                self._model.Add(b - a == result).OnlyEnforceIf(case2)

                self._model.Add(case1 + case2 == 1)

    def _get_rows_columns_number(self) -> (int, int):
        all_positions = [pos for sublist, _, _ in self._regions_operators_results for pos in sublist]
        min_r = min(pos.r for pos in all_positions)
        max_r = max(pos.r for pos in all_positions)
        min_c = min(pos.c for pos in all_positions)
        max_c = max(pos.c for pos in all_positions)
        return max_r - min_r + 1, max_c - min_c + 1
