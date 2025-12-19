from z3 import And, Int, Not, Solver, unsat

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class DoubleMinesweeperSolver(GameSolver):
    empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        return Grid([[model.eval(self._grid_z3[Position(i, j)]).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_neighbors_constraints()

    def _add_initial_constraints(self):
        for position, cell in self._grid:
            if cell != self.empty:
                self._solver.add(self._grid_z3[position] == 0)
            else:
                self._solver.add(self._grid_z3[position] >= 0, self._grid_z3[position] <= 2)

    def _add_neighbors_constraints(self):
        for position, cell in [(position, cell) for position, cell in self._grid if cell != self.empty]:
            self._solver.add(sum([value for value in self._grid_z3.neighbors_values(position, 'diagonal')]) == cell)