from z3 import Solver, Not, And, Bool, is_true, Implies, sat, BoolRef

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
        for position, top_left in [(pos, val) for pos, val in self._grid_z3 if pos not in self._grid_z3.edge_down_positions() + self._grid_z3.edge_right_positions()]:
            top_right = self._grid_z3[position.right]
            bottom_left = self._grid_z3[position.down]
            bottom_right = self._grid_z3[position.down.right]
            self._add_rectangle_constraint(top_left, top_right, bottom_right, bottom_left)

    def _add_rectangle_constraint(self, top_left: BoolRef, top_right: BoolRef, bottom_right: BoolRef, bottom_left: BoolRef):
        self._solver.add(Implies(And(top_right, bottom_left, bottom_right), top_left))
        self._solver.add(Implies(And(top_left, bottom_left, bottom_right), top_right))
        self._solver.add(Implies(And(top_left, top_right, bottom_right), bottom_left))
        self._solver.add(Implies(And(top_left, top_right, bottom_left), bottom_right))

    def _get_region_positions(self, position: Position) -> frozenset[Position]:
        for region in self._regions.values():
            if position in region:
                return region
        return frozenset([])
