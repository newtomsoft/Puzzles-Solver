from z3 import Solver, sat, Int, And, Not, Distinct

from Puzzles.Hashi.Island import Island
from Utils.Grid import Grid
from Utils.Position import Position


class HashiGame:
    def __init__(self, islands: list[Island]):
        self._islands = islands
        self._solver: Solver | None = None
        self._grid_z3: Grid | None = None
        self._last_solution_grid: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._solver = Solver()
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._solver is None:
            self._init_solver()
        if self._solver.check() != sat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._number(Position(r, c))).as_long() for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._last_solution_grid = grid
        return grid

    def get_other_solution(self):
        exclusion_constraint = Not(And([self._number(Position(r, c)) == self._last_solution_grid[Position(r, c)] for r in range(self.rows_number) for c in range(self.columns_number) if self._last_solution_grid.value(r, c)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _number(self, position):
        return self._grid_z3[position]

    def _add_constraints(self):
        pass
