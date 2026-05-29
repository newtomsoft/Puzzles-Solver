from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class CloudsSolver(GameSolver):
    def __init__(self, rows_counts: list[int], columns_counts: list[int]):
        self._rows_counts = rows_counts
        self._columns_counts = columns_counts
        self._rows_number = len(rows_counts)
        self._columns_number = len(columns_counts)
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
        self._add_lines_counts_constraints()
        self._add_shapes_rectangles_sizes_neighbors_constraints()
        self._add_sizes_constraints()

    def _add_lines_counts_constraints(self):
        for i, row in enumerate(self._grid_z3.matrix):
            self._model.Add(sum(row) == self._rows_counts[i])

        for i in range(self._columns_number):
            column_vars = [self._grid_z3[Position(r, i)] for r in range(self._rows_number)]
            self._model.Add(sum(column_vars) == self._columns_counts[i])

    def _add_shapes_rectangles_sizes_neighbors_constraints(self):
        for position, top_left in [(pos, val) for pos, val in self._grid_z3 if pos not in self._grid_z3.edge_down_positions() + self._grid_z3.edge_right_positions()]:
            top_right = self._grid_z3[position.right]
            bottom_left = self._grid_z3[position.down]
            bottom_right = self._grid_z3[position.down.right]
            self._add_rectangle_constraint(top_left, top_right, bottom_left, bottom_right)
            self._add_neighbor_constraint(top_left, top_right, bottom_left, bottom_right)

    def _add_rectangle_constraint(self, top_left, top_right, bottom_left, bottom_right):
        self._model.AddBoolOr([top_right.Not(), bottom_left.Not(), bottom_right.Not(), top_left])
        self._model.AddBoolOr([top_left.Not(), bottom_left.Not(), bottom_right.Not(), top_right])
        self._model.AddBoolOr([top_left.Not(), top_right.Not(), bottom_right.Not(), bottom_left])
        self._model.AddBoolOr([top_left.Not(), top_right.Not(), bottom_left.Not(), bottom_right])

    def _add_neighbor_constraint(self, top_left, top_right, bottom_left, bottom_right):
        self._model.AddBoolOr([top_left.Not(), top_right, bottom_right.Not(), bottom_left])
        self._model.AddBoolOr([top_left, top_right.Not(), bottom_right, bottom_left.Not()])

    def _add_sizes_constraints(self):
        for r in range(self._rows_number - 2):
            for c in range(self._columns_number - 2):
                center = self._grid_z3[Position(r + 1, c + 1)]
                up = self._grid_z3[Position(r, c + 1)]
                down = self._grid_z3[Position(r + 2, c + 1)]
                left = self._grid_z3[Position(r + 1, c)]
                right = self._grid_z3[Position(r + 1, c + 2)]
                down_right = self._grid_z3[Position(r + 2, c + 2)]
                self._model.AddBoolOr([center.Not(), left, up, down])
                self._model.AddBoolOr([center.Not(), left, up, right])
                self._model.AddBoolOr([center.Not(), left, up, down_right])

        for r in range(self._rows_number - 2):
            c = 0
            center = self._grid_z3[Position(r + 1, c)]
            up = self._grid_z3[Position(r, c)]
            down = self._grid_z3[Position(r + 2, c)]
            right = self._grid_z3[Position(r + 1, c + 1)]
            down_right = self._grid_z3[Position(r + 2, c + 1)]
            self._model.AddBoolOr([center.Not(), up, down])
            self._model.AddBoolOr([center.Not(), up, right])
            self._model.AddBoolOr([center.Not(), up, down_right])

            c = self._columns_number - 1
            center = self._grid_z3[Position(r + 1, c)]
            up = self._grid_z3[Position(r, c)]
            left = self._grid_z3[Position(r + 1, c - 1)]
            self._model.AddBoolOr([center.Not(), left, up])

        for c in range(self._columns_number - 2):
            r = 0
            center = self._grid_z3[Position(r, c + 1)]
            down = self._grid_z3[Position(r + 1, c + 1)]
            left = self._grid_z3[Position(r, c)]
            right = self._grid_z3[Position(r, c + 2)]
            down_right = self._grid_z3[Position(r + 1, c + 2)]
            self._model.AddBoolOr([center.Not(), left, down])
            self._model.AddBoolOr([center.Not(), left, right])
            self._model.AddBoolOr([center.Not(), left, down_right])

            r = self._columns_number - 1
            center = self._grid_z3[Position(r, c + 1)]
            up = self._grid_z3[Position(r - 1, c + 1)]
            left = self._grid_z3[Position(r, c)]
            self._model.AddBoolOr([center.Not(), left, up])
