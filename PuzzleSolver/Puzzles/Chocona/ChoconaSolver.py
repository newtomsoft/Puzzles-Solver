from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class ChoconaSolver(GameSolver):
    def __init__(self, grid: Grid, regions_grid: Grid):
        super().__init__()
        self._numbers_grid = grid
        self._regions = regions_grid.get_regions()
        self._rows_number = self._numbers_grid.rows_number
        self._columns_number = self._numbers_grid.columns_number
        self._model = cp_model.CpModel()
        self._solver_initialized = False
        self._previous_solution: Grid = Grid.empty()

    def _init_solver(self):
        self._grid_z3 = Grid([[self._model.NewBoolVar(f"cell_{r}-{c}") for c in range(self._numbers_grid.columns_number)] for r in range(self._numbers_grid.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver_initialized:
            self._init_solver()
            self._solver_initialized = True

        if self._solver.Solve(self._model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            self._previous_solution = Grid([[1 if bool(self._solver.Value(self._grid_z3.value(i, j))) else 0 for j in range(self._columns_number)] for i in range(self._rows_number)])
            return self._previous_solution

        return Grid.empty()

    def get_other_solution(self):
        self._model.AddBoolOr([self._grid_z3[position].Not() if value else self._grid_z3[position] for position, value in self._previous_solution])
        return self.get_solution()

    def _add_constraints(self):
        self._add_region_number_constraints()
        self._add_all_shapes_are_rectangles_constraints()

    def _add_region_number_constraints(self):
        for position, number in [(position, number) for position, number in self._numbers_grid if number >= 0]:
            region_positions = self._get_region_positions(position)
            self._model.Add(sum([self._grid_z3[position] for position in region_positions]) == number)

    def _add_all_shapes_are_rectangles_constraints(self):
        for position, top_left in [(pos, val) for pos, val in self._grid_z3 if pos not in self._grid_z3.edge_down_positions() + self._grid_z3.edge_right_positions()]:
            top_right = self._grid_z3[position.right]
            bottom_left = self._grid_z3[position.down]
            bottom_right = self._grid_z3[position.down.right]
            self._add_rectangle_constraint(top_left, top_right, bottom_right, bottom_left)

    def _add_rectangle_constraint(self, top_left, top_right, bottom_right, bottom_left):
        self._model.AddBoolOr([top_right.Not(), bottom_left.Not(), bottom_right.Not(), top_left])
        self._model.AddBoolOr([top_left.Not(), bottom_left.Not(), bottom_right.Not(), top_right])
        self._model.AddBoolOr([top_left.Not(), top_right.Not(), bottom_right.Not(), bottom_left])
        self._model.AddBoolOr([top_left.Not(), top_right.Not(), bottom_left.Not(), bottom_right])

    def _get_region_positions(self, position: Position) -> frozenset[Position]:
        for region in self._regions.values():
            if position in region:
                return region
        return frozenset([])
