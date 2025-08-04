from z3 import Solver, Bool, Not, And, is_true, sat, Implies

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class CloudsSolver(GameSolver):
    def __init__(self, rows_counts: list[int], columns_counts: list[int]):
        self._rows_counts = rows_counts
        self._columns_counts = columns_counts
        self._rows_number = len(rows_counts)
        self._columns_number = len(columns_counts)
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid(
            [[Bool(f"cell_{r}-{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution = self._compute_solution()
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        previous_solution_constraints = []
        for position, _ in [(position, value) for (position, value) in self._previous_solution if value]:
            previous_solution_constraints.append(self._grid_z3[position])
        self._solver.add(Not(And(previous_solution_constraints)))

        return self.get_solution()

    def _compute_solution(self) -> Grid:
        if self._solver.check() == sat:
            model = self._solver.model()
            return Grid([[is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self._columns_number)] for i in
                         range(self._rows_number)])

        return Grid.empty()

    def _add_constraints(self):
        self._add_lines_counts_constraints()
        self._add_shapes_rectangles_sizes_neighbors_constraints()
        self._add_sizes_constraints()

    def _add_lines_counts_constraints(self):
        for i, row in enumerate(self._grid_z3.matrix):
            self._solver.add(sum(row) == self._rows_counts[i])

        for i in range(self._columns_number):
            column_vars = [self._grid_z3[Position(r, i)] for r in range(self._rows_number)]
            self._solver.add(sum(column_vars) == self._columns_counts[i])

    def _add_shapes_rectangles_sizes_neighbors_constraints(self):
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                top_left = self._grid_z3[Position(r, c)]
                top_right = self._grid_z3[Position(r, c + 1)]
                bottom_left = self._grid_z3[Position(r + 1, c)]
                bottom_right = self._grid_z3[Position(r + 1, c + 1)]

                self._add_rectangle_constraint(top_left, top_right, bottom_left, bottom_right)
                self._add_neighbor_constraint(top_left, top_right, bottom_left, bottom_right)

    def _add_rectangle_constraint(self, top_left, top_right, bottom_left, bottom_right):
        self._solver.add(Implies(And(top_right, bottom_left, bottom_right), top_left))
        self._solver.add(Implies(And(top_left, bottom_left, bottom_right), top_right))
        self._solver.add(Implies(And(top_left, top_right, bottom_right), bottom_left))
        self._solver.add(Implies(And(top_left, top_right, bottom_left), bottom_right))

    def _add_neighbor_constraint(self, top_left, top_right, bottom_left, bottom_right):
        self._solver.add(Not(And(top_left, Not(top_right), bottom_right, Not(bottom_left))))
        self._solver.add(Not(And(Not(top_left), top_right, Not(bottom_right), bottom_left)))

    def _add_sizes_constraints(self):
        for r in range(self._rows_number - 2):
            for c in range(self._columns_number - 2):
                center = self._grid_z3[Position(r + 1, c + 1)]
                up = self._grid_z3[Position(r, c + 1)]
                down = self._grid_z3[Position(r + 2, c + 1)]
                left = self._grid_z3[Position(r + 1, c)]
                right = self._grid_z3[Position(r + 1, c + 2)]
                down_right = self._grid_z3[Position(r + 2, c + 2)]
                self._solver.add(Implies(And(center, Not(left), Not(up)), And(down, right, down_right)))

        for r in range(self._rows_number - 2):
            c = 0
            center = self._grid_z3[Position(r + 1, c)]
            up = self._grid_z3[Position(r, c)]
            down = self._grid_z3[Position(r + 2, c)]
            right = self._grid_z3[Position(r + 1, c + 1)]
            down_right = self._grid_z3[Position(r + 2, c + 1)]
            self._solver.add(Implies(And(center, Not(up)), And(down, right, down_right)))

            c = self._columns_number - 1
            center = self._grid_z3[Position(r + 1, c)]
            up = self._grid_z3[Position(r, c)]
            left = self._grid_z3[Position(r + 1, c - 1)]
            self._solver.add(Not(And(center, Not(left), Not(up))))

        for c in range(self._columns_number - 2):
            r = 0
            center = self._grid_z3[Position(r, c + 1)]
            down = self._grid_z3[Position(r + 1, c + 1)]
            left = self._grid_z3[Position(r, c)]
            right = self._grid_z3[Position(r, c + 2)]
            down_right = self._grid_z3[Position(r + 1, c + 2)]
            self._solver.add(Implies(And(center, Not(left)), And(down, right, down_right)))

            r = self._columns_number - 1
            center = self._grid_z3[Position(r, c + 1)]
            up = self._grid_z3[Position(r - 1, c + 1)]
            left = self._grid_z3[Position(r, c)]
            self._solver.add(Not(And(center, Not(left), Not(up))))
