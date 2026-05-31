from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class DoubleMinesweeperSolver(GameSolver):
    cell_empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None
        self._counter = 0

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[self._model.NewIntVar(0, 2, f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        bs = []
        for position, value in self._previous_solution:
            b = self._model.NewBoolVar(f"block_{self._counter}")
            self._counter += 1
            self._model.Add(self._grid_z3[position] == value).OnlyEnforceIf(b)
            self._model.Add(self._grid_z3[position] != value).OnlyEnforceIf(b.Not())
            bs.append(b)
        self._model.Add(sum(bs) <= len(bs) - 1)
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if self._solver.Solve(self._model) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()
        return Grid([[self._solver.Value(self._grid_z3[Position(i, j)]) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_neighbors_constraints()

    def _add_initial_constraints(self):
        for position, cell in self._grid:
            if cell != self.empty:
                self._model.Add(self._grid_z3[position] == 0)
            else:
                self._model.Add(self._grid_z3[position] >= 0)
                self._model.Add(self._grid_z3[position] <= 2)

    def _add_neighbors_constraints(self):
        for position, cell in [(position, cell) for position, cell in self._grid if cell != self.empty]:
            self._model.Add(sum([value for value in self._grid_z3.neighbors_values(position, 'diagonal')]) == cell)
