from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class MinesweeperSolver(GameSolver):
    cell_empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._solver_initialized = False
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[self._model.NewBoolVar(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver_initialized:
            self._init_solver()
            self._solver_initialized = True
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._model.AddBoolOr([self._grid_z3[position].Not() if val == 1 else self._grid_z3[position] for position, val in self._previous_solution])
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if self._solver.Solve(self._model) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()
        return Grid([[bool(self._solver.Value(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_sum_constraints()

    def _add_initial_constraints(self):
        for position in [position for position, cell in self._grid if cell != self.empty]:
            self._model.Add(self._grid_z3[position] == 0)

    def _add_sum_constraints(self):
        for position, cell in [(position, cell) for position, cell in self._grid if cell != self.empty]:
            self._model.Add(sum([value for value in self._grid_z3.neighbors_values(position, 'diagonal')]) == cell)
