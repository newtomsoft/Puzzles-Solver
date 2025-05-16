from ortools.sat.python.cp_model import CpModel, CpSolver, INFEASIBLE

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class No4InARowSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 4:
            raise ValueError("No 4 in a Row grid must be at least 4x4")
        self._model = CpModel()
        self._solver = CpSolver()
        self._grid_ortools = None
        self._previous_solution = None
        self._blocked_solutions = []

    def get_solution(self) -> Grid:
        self._grid_ortools = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                self._grid_ortools[(r, c)] = self._model.NewBoolVar(f"matrix_{r}_{c}")

        self._add_constraints()

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution and not self._previous_solution.is_empty():
            solution_as_list = []
            for r in range(self.rows_number):
                for c in range(self.columns_number):
                    if self._previous_solution.value(r, c) == 1:
                        solution_as_list.append(self._grid_ortools[(r, c)])
                    else:
                        solution_as_list.append(self._model.NewBoolVar("not_" + str(len(self._blocked_solutions))))
                        self._model.AddBoolAnd([solution_as_list[-1]]).OnlyEnforceIf(self._grid_ortools[(r, c)].Not())
                        self._model.AddBoolAnd([solution_as_list[-1].Not()]).OnlyEnforceIf(self._grid_ortools[(r, c)])

            self._model.AddBoolOr([var.Not() for var in solution_as_list])
            self._blocked_solutions.append(solution_as_list)

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        status = self._solver.Solve(self._model)

        if status == INFEASIBLE:
            return Grid.empty()

        grid_values = []
        for r in range(self.rows_number):
            row_values = []
            for c in range(self.columns_number):
                value = self._solver.BooleanValue(self._grid_ortools[(r, c)])
                row_values.append(value)
            grid_values.append(row_values)

        return Grid(grid_values)

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_not_same_4_adjacent_horizontally_constraints()
        self._add_not_same_4_adjacent_vertically_constraints()
        self._add_not_same_4_adjacent_diagonally_constraints()

    def _add_initial_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == 0:
                    self._model.Add(self._grid_ortools[(r, c)] == 0)
                elif self._grid.value(r, c) == 1:
                    self._model.Add(self._grid_ortools[(r, c)] == 1)

    def _add_not_same_4_adjacent_horizontally_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number - 3):
                cells = [self._grid_ortools[(r, c + i)] for i in range(4)]
                self._model.AddBoolOr([cell.Not() for cell in cells])
                self._model.AddBoolOr(cells)

    def _add_not_same_4_adjacent_vertically_constraints(self):
        for c in range(self.columns_number):
            for r in range(self.rows_number - 3):
                cells = [self._grid_ortools[(r + i, c)] for i in range(4)]
                self._model.AddBoolOr([cell.Not() for cell in cells])
                self._model.AddBoolOr(cells)

    def _add_not_same_4_adjacent_diagonally_constraints(self):
        for r in range(self.rows_number - 3):
            for c in range(self.columns_number - 3):
                cells = [self._grid_ortools[(r + i, c + i)] for i in range(4)]
                self._model.AddBoolOr([cell.Not() for cell in cells])
                self._model.AddBoolOr(cells)

        for r in range(self.rows_number - 3):
            for c in range(3, self.columns_number):
                cells = [self._grid_ortools[(r + i, c - i)] for i in range(4)]
                self._model.AddBoolOr([cell.Not() for cell in cells])
                self._model.AddBoolOr(cells)
