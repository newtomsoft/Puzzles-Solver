from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class GyokusekiSolver(GameSolver):
    def __init__(self, counts: dict[str, list[int]]):
        self._counts_by_edge: dict[str, list[int]] = counts
        self.rows_number = len(self._counts_by_edge['up'])
        self.columns_number = len(self._counts_by_edge['left'])
        self._solver = cp_model.CpSolver()
        self._model = cp_model.CpModel()
        self._white: Grid | None = None
        self._black: Grid | None = None
        self._previous_solution_grid = None
        self._initialized = False

    def _init_solver(self):
        self._model = cp_model.CpModel()
        self._white = Grid([[self._model.new_bool_var(f"w_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._black = Grid([[self._model.new_bool_var(f"b_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._initialized = True

    def get_solution(self) -> Grid:
        if not self._initialized:
            self._init_solver()
        return self._solve()

    def get_other_solution(self):
        if self._previous_solution_grid is None:
            return self.get_solution()
        if self._previous_solution_grid.is_empty():
            return Grid.empty()
        exclusion_literals = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                val = self._previous_solution_grid.value(r, c)
                if val == 0:
                    continue
                if val == 1:
                    exclusion_literals.append(self._white[Position(r, c)].Not())
                else:
                    exclusion_literals.append(self._black[Position(r, c)].Not())
        self._model.add_bool_or(exclusion_literals)
        return self._solve()

    def _solve(self) -> Grid:
        status = self._solver.solve(self._model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            grid = Grid([
                [
                    1 if self._solver.boolean_value(self._white[Position(r, c)])
                    else 2 if self._solver.boolean_value(self._black[Position(r, c)])
                    else 0
                    for c in range(self.columns_number)
                ]
                for r in range(self.rows_number)
            ])
            self._previous_solution_grid = grid
            return grid
        return Grid.empty()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_blacks_constraints()
        self._add_whites_constraints()

    def _add_initial_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                self._model.add(self._white[Position(r, c)] + self._black[Position(r, c)] <= 1)

    def _add_blacks_constraints(self):
        for r in range(self.rows_number):
            self._model.add(sum(self._black[Position(r, c)] for c in range(self.columns_number)) == 1)
        for c in range(self.columns_number):
            self._model.add(sum(self._black[Position(r, c)] for r in range(self.rows_number)) == 1)

    def _add_whites_constraints(self):
        for edge, counts_line in self._counts_by_edge.items():
            match edge:
                case 'up':
                    for index, c in enumerate(range(self.columns_number)):
                        positions = [Position(r, c) for r in range(self.rows_number)]
                        self._add_segment_whites_constraints(counts_line[index], positions)
                case 'down':
                    for index, c in enumerate(range(self.columns_number)):
                        positions = [Position(r, c) for r in range(self.rows_number - 1, -1, -1)]
                        self._add_segment_whites_constraints(counts_line[index], positions)
                case 'left':
                    for index, r in enumerate(range(self.rows_number)):
                        positions = [Position(r, c) for c in range(self.columns_number)]
                        self._add_segment_whites_constraints(counts_line[index], positions)
                case 'right':
                    for index, r in enumerate(range(self.rows_number)):
                        positions = [Position(r, c) for c in range(self.columns_number - 1, -1, -1)]
                        self._add_segment_whites_constraints(counts_line[index], positions)

    def _add_segment_whites_constraints(self, count: int, positions: list[Position]):
        if count == -1:
            return
        whites_count = count - 1
        for i in range(whites_count):
            self._model.add(self._black[positions[i]] == 0)
        for i in range(whites_count, len(positions)):
            sum_whites_before = sum(self._white[positions[j]] for j in range(i))
            c = self._model.add(sum_whites_before == whites_count)
            c.only_enforce_if(self._black[positions[i]])


