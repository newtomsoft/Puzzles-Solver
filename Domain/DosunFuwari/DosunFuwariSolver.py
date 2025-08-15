from z3 import Solver, Bool, Not, And, unsat, Or, Implies, is_true, Int

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class DosunFuwariSolver(GameSolver):
    empty = 0
    black = 1
    white = 2
    wall = empty

    def __init__(self, region_grid: Grid):
        self._region_grid = region_grid
        self._positions_by_region = region_grid.get_regions()
        self.rows_number = self._region_grid.rows_number
        self.columns_number = self._region_grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"cell_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self):
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._grid_z3[Position(i, j)]).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_initials_constraints()
        self._add_count_constraints()
        self._add_gravity_constraints()

    def _add_initials_constraints(self):
        for position, value in self._region_grid:
            if value == self.wall:
                self._solver.add(self._grid_z3[position] == self.empty)
                continue
            self._solver.add(self._grid_z3[position] >= self.empty, self._grid_z3[position] <= self.white)

    def _add_count_constraints(self):
        for positions in [positions for region_id, positions in self._positions_by_region.items() if region_id != self.wall]:
            self._solver.add(sum([self._grid_z3[position] == self.black for position in positions]) == 1)
            self._solver.add(sum([self._grid_z3[position] == self.white for position in positions]) == 1)

    def _add_gravity_constraints(self):
        for position in [position for position, value in self._region_grid if value != self.wall]:
            black = self._grid_z3[position] == self.black
            no_down = True if self._grid_z3.is_position_in_edge_down(position) else False
            down_wall = True if not no_down and self._region_grid[position.down] == self.wall else False
            down_black = self._grid_z3[position.down] == self.black if not self._grid_z3.is_position_in_edge_down(position) else False
            self._solver.add(Implies(black, Or(down_black, down_wall, no_down)))

            white = self._grid_z3[position] == self.white
            no_up = True if self._grid_z3.is_position_in_edge_up(position) else False
            up_wall = True if not no_up and self._region_grid[position.up] == self.wall else False
            up_white = self._grid_z3[position.up] == self.white if not self._grid_z3.is_position_in_edge_up(position) else False
            self._solver.add(Implies(white, Or(up_white, up_wall, no_up)))

            down_white = self._grid_z3[position.down] == self.white if not self._grid_z3.is_position_in_edge_down(position) else False
            self._solver.add(Not(And([black, down_white])))