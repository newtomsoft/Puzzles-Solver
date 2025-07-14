from z3 import Solver, Bool, Not, And, is_true, sat, Or

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class FobidoshiSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Bool(f"cell_{r}-{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_circle_connected()
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        previous_solution_constraints = []
        for position, _ in [(position, value) for (position, value) in self._previous_solution if not value]:
            previous_solution_constraints.append(Not(self._grid_z3[position]))
        self._solver.add(Not(And(previous_solution_constraints)))

        return self.get_solution()

    def _ensure_all_circle_connected(self) -> tuple[Grid, int]:
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self._columns_number)] for i in range(self._rows_number)])
            circles_shapes = current_grid.get_all_shapes()
            if len(circles_shapes) == 1:
                return current_grid, proposition_count

            biggest_circles_shapes = max(circles_shapes, key=len)
            circles_shapes.remove(biggest_circles_shapes)
            for circles_shape in circles_shapes:
                in_all_circle = And([self._grid_z3[position] for position in circles_shape])
                around_all_false = And([Not(self._grid_z3[position]) for position in ShapeGenerator.around_shape(circles_shape) if position in self._grid_z3])
                constraint = Not(And(around_all_false, in_all_circle))
                self._solver.add(constraint)

        return Grid.empty(), proposition_count

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_not_same_4_adjacent_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid:
            if value == 1:
                self._solver.add(self._grid_z3[position])
            elif value == 0:
                self._solver.add(Not(self._grid_z3[position]))

    def _add_not_same_4_adjacent_constraints(self):
        self._add_not_same_4_adjacent_horizontally_constraints()
        self._add_not_same_4_adjacent_vertically_constraints()

    def _add_not_same_4_adjacent_horizontally_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number - 3):
                cells = [self._grid_z3[Position(r, c + i)] for i in range(4)]
                self._solver.add(Or([Not(cell) for cell in cells]))

    def _add_not_same_4_adjacent_vertically_constraints(self):
        for c in range(self._columns_number):
            for r in range(self._rows_number - 3):
                cells = [self._grid_z3[Position(r + i, c)] for i in range(4)]
                self._solver.add(Or([Not(cell) for cell in cells]))
