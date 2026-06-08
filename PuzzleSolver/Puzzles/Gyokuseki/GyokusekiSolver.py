from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class GyokusekiSolver(GameSolver):
    def __init__(self, counts: dict[str, list[int]]):
        super().__init__()
        self._counts_by_edge: dict[str, list[int]] = counts
        self.rows_number = len(self._counts_by_edge['up'])
        self.columns_number = len(self._counts_by_edge['left'])
        self._model = cp_model.CpModel()
        self._grid_z3: Grid | None = None
        self._previous_solution_grid = None
        self._solver_initialized = False
        self._counter = 0

    def _init_solver(self):
        self._grid_z3 = Grid([[self._model.NewIntVar(0, 2, f"cell{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
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
        self._add_initial_constraints()
        self._add_blacks_constraints()
        self._add_whites_constraints()

    def _add_initial_constraints(self):
        for _, value in self._grid_z3:
            self._model.AddAllowedAssignments([value], [(0,), (1,), (2,)])

    def _add_blacks_constraints(self):
        for r in range(self.rows_number):
            bs = []
            for c in range(self.columns_number):
                b = self._model.NewBoolVar(f"black_r{r}_c{c}")
                v = self._grid_z3[Position(r, c)]
                self._model.Add(v == 2).OnlyEnforceIf(b)
                self._model.Add(v != 2).OnlyEnforceIf(b.Not())
                bs.append(b)
            self._model.Add(sum(bs) == 1)

        for c in range(self.columns_number):
            bs = []
            for r in range(self.rows_number):
                b = self._model.NewBoolVar(f"black_c{c}_r{r}")
                v = self._grid_z3[Position(r, c)]
                self._model.Add(v == 2).OnlyEnforceIf(b)
                self._model.Add(v != 2).OnlyEnforceIf(b.Not())
                bs.append(b)
            self._model.Add(sum(bs) == 1)

    def _add_whites_constraints(self):
        for edge, counts_line in self._counts_by_edge.items():
            match edge:
                case 'up':
                    for index, c in enumerate(range(self.columns_number)):
                        positions = [self._grid_z3[Position(r, c)] for r in range(self.rows_number)]
                        self._add_segment_whites_constraints(counts_line[index], positions)
                case 'down':
                    for index, c in enumerate(range(self.columns_number)):
                        positions = [self._grid_z3[Position(r, c)] for r in range(self.rows_number - 1, -1, -1)]
                        self._add_segment_whites_constraints(counts_line[index], positions)
                case 'left':
                    for index, r in enumerate(range(self.rows_number)):
                        positions = [self._grid_z3[Position(r, c)] for c in range(self.columns_number)]
                        self._add_segment_whites_constraints(counts_line[index], positions)
                case 'right':
                    for index, r in enumerate(range(self.rows_number)):
                        positions = [self._grid_z3[Position(r, c)] for c in range(self.columns_number - 1, -1, -1)]
                        self._add_segment_whites_constraints(counts_line[index], positions)

    def _add_segment_whites_constraints(self, count: int, values_z3: list):
        if count == -1:
            return

        whites_count = count - 1
        for black_index in range(whites_count):
            self._model.Add(values_z3[black_index] != 2)
        for black_index in range(whites_count, len(values_z3)):
            b_black = self._model.NewBoolVar(f"seg_black_{self._counter}")
            self._counter += 1
            self._model.Add(values_z3[black_index] == 2).OnlyEnforceIf(b_black)
            self._model.Add(values_z3[black_index] != 2).OnlyEnforceIf(b_black.Not())

            wbs = []
            for index in range(black_index):
                wb = self._model.NewBoolVar(f"seg_white_{self._counter}")
                self._counter += 1
                self._model.Add(values_z3[index] == 1).OnlyEnforceIf(wb)
                self._model.Add(values_z3[index] != 1).OnlyEnforceIf(wb.Not())
                wbs.append(wb)
            if wbs:
                self._model.Add(sum(wbs) == whites_count).OnlyEnforceIf(b_black)


