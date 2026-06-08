from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class GradesSolver(GameSolver):
    no_value = None

    def __init__(self, grid: Grid, clues: dict[str, list[int]]):
        super().__init__()
        self._grid = grid
        self._clues: dict[str, list[int]] = clues
        self.rows_number = len(clues['left'])
        self.columns_number = len(clues['top'])
        self._model = cp_model.CpModel()
        self._grid_z3: Grid | None = None
        self._previous_solution_grid = None
        self._solver_initialized = False
        self._counter = 0

    def _init_solver(self):
        self._grid_z3 = Grid([[self._model.NewIntVar(0, 100, f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._solver_initialized = True

    def get_solution(self) -> Grid:
        if not self._solver_initialized:
            self._init_solver()
        if self._solver.Solve(self._model) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()
        grid = Grid([[self._solver.Value(self._grid_z3[Position(r, c)]) for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._previous_solution_grid = grid
        return grid

    def get_other_solution(self):
        bs = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                v = self._previous_solution_grid.value(r, c)
                if v:
                    b = self._model.NewBoolVar(f"block_{self._counter}")
                    self._counter += 1
                    self._model.Add(self._grid_z3[Position(r, c)] == v).OnlyEnforceIf(b)
                    self._model.Add(self._grid_z3[Position(r, c)] != v).OnlyEnforceIf(b.Not())
                    bs.append(b)
        self._model.Add(sum(bs) <= len(bs) - 1)
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraint()
        self._add_counts_clues_constraint()
        self._add_sums_clues_constraint()
        self._add_no_neighbors_constraints()

    def _add_initial_constraint(self):
        for position, value in self._grid:
            if value == self.no_value:
                self._model.Add(self._grid_z3[position] >= 0)
            else:
                self._model.Add(self._grid_z3[position] == value)

    def _add_counts_clues_constraint(self):
        for row, count in enumerate(self._clues['left']):
            if count != self.no_value:
                bs = []
                for col in range(self.columns_number):
                    b = self._model.NewBoolVar(f"count_l_{row}_{col}")
                    self._model.Add(self._grid_z3[row, col] != 0).OnlyEnforceIf(b)
                    self._model.Add(self._grid_z3[row, col] == 0).OnlyEnforceIf(b.Not())
                    bs.append(b)
                self._model.Add(sum(bs) == count)

        for col, count in enumerate(self._clues['top']):
            if count != self.no_value:
                bs = []
                for row in range(self.rows_number):
                    b = self._model.NewBoolVar(f"count_t_{row}_{col}")
                    self._model.Add(self._grid_z3[row, col] != 0).OnlyEnforceIf(b)
                    self._model.Add(self._grid_z3[row, col] == 0).OnlyEnforceIf(b.Not())
                    bs.append(b)
                self._model.Add(sum(bs) == count)

    def _add_sums_clues_constraint(self):
        for row, sum_value in enumerate(self._clues['right']):
            if sum_value != self.no_value:
                self._model.Add(sum([self._grid_z3[row, col] for col in range(self.columns_number)]) == sum_value)

        for col, sum_value in enumerate(self._clues['bottom']):
            if sum_value != self.no_value:
                self._model.Add(sum([self._grid_z3[row, col] for row in range(self.rows_number)]) == sum_value)

    def _add_no_neighbors_constraints(self):
        for position, value in self._grid_z3:
            b = self._model.NewBoolVar(f"no_neigh_{position.row}_{position.column}")
            self._model.Add(value != 0).OnlyEnforceIf(b)
            self._model.Add(value == 0).OnlyEnforceIf(b.Not())
            for neighbors_value in self._grid_z3.neighbors_values(position, 'diagonal'):
                self._model.Add(neighbors_value == 0).OnlyEnforceIf(b)
