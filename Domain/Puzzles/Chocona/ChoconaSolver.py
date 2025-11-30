from z3 import Solver, Not, And, Bool, is_true, Implies, sat

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class ChoconaSolver(GameSolver):
    def __init__(self, grid: Grid, regions_grid: Grid):
        self._numbers_grid = grid
        self._regions = regions_grid.get_regions()
        self._rows_number = self._numbers_grid.rows_number
        self._columns_number = self._numbers_grid.columns_number
        self._solver = Solver()
        self._previous_solution: Grid = Grid.empty()

    def _init_solver(self):
        self._grid_z3 = Grid([[Bool(f"cell_{r}-{c}") for c in range(self._numbers_grid.columns_number)] for r in range(self._numbers_grid.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        if self._solver.check() == sat:
            model = self._solver.model()
            self._previous_solution = Grid([[1 if is_true(model.eval(self._grid_z3.value(i, j))) else 0 for j in range(self._columns_number)] for i in range(self._rows_number)])
            return self._previous_solution

        return Grid.empty()

    def get_other_solution(self):
        constraints = []
        for position, value in self._previous_solution:
            constraints.append(self._grid_z3[position] if value else Not(self._grid_z3[position]))
        self._solver.add(Not(And(constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_region_number_constraints()
        self._add_all_shapes_are_rectangles_constraints()

    def _add_region_number_constraints(self):
        for position, number in [(position, number) for position, number in self._numbers_grid if number >= 0]:
            region_positions = self._get_region_positions(position)
            self._solver.add(sum([self._grid_z3[position] for position in region_positions]) == number)

    def _add_all_shapes_are_rectangles_constraints(self):
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                top_left = self._grid_z3[Position(r, c)]
                top_right = self._grid_z3[Position(r, c + 1)]
                bottom_left = self._grid_z3[Position(r + 1, c)]
                bottom_right = self._grid_z3[Position(r + 1, c + 1)]

                self._solver.add(Implies(And(top_right, bottom_left, bottom_right), top_left))
                self._solver.add(Implies(And(top_left, bottom_left, bottom_right), top_right))
                self._solver.add(Implies(And(top_left, top_right, bottom_right), bottom_left))
                self._solver.add(Implies(And(top_left, top_right, bottom_left), bottom_right))

    def _get_region_positions(self, position: Position) -> frozenset[Position]:
        for region in self._regions.values():
            if position in region:
                return region
        return frozenset([])
