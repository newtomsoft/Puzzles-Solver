from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class JumpSolver(GameSolver):
    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number

        self._model: cp_model.CpModel | None = None
        self._x: dict | None = None
        self._non_blocked_positions: list[Position] | None = None
        self._max_number: int = 0
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._model = cp_model.CpModel()
        self._x = {}
        self._prefilled: dict[Position, int] = {}
        self._non_blocked_positions = [
            position for position, value in self._grid if value != self.cell_blocked
        ]
        for position, value in self._grid:
            if isinstance(value, int):
                self._prefilled[position] = value
        self._max_number = len(self._non_blocked_positions)
        self._previous_solution = None

        self._init_variables()
        self._add_one_value_per_cell()
        self._add_one_cell_per_number()
        self._add_prefilled_constraints()
        self._add_knight_move_constraints()

        status = self._solver.solve(self._model)
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            self._previous_solution = self._build_solution()
            return self._previous_solution

        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None or self._previous_solution.is_empty():
            return Grid.empty()

        self._exclude_solution(self._previous_solution)

        status = self._solver.solve(self._model)
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            self._previous_solution = self._build_solution()
            return self._previous_solution

        return Grid.empty()

    def _init_variables(self):
        for position in self._non_blocked_positions:
            for k in range(1, self._max_number + 1):
                self._x[(position.r, position.c, k)] = self._model.new_bool_var(
                    f"x_{position.r}_{position.c}_{k}"
                )

    def _add_one_value_per_cell(self):
        for position in self._non_blocked_positions:
            self._model.add(
                sum(self._x[(position.r, position.c, k)] for k in range(1, self._max_number + 1)) == 1
            )

    def _add_one_cell_per_number(self):
        for k in range(1, self._max_number + 1):
            self._model.add(
                sum(self._x[(position.r, position.c, k)] for position in self._non_blocked_positions) == 1
            )

    def _add_prefilled_constraints(self):
        for position, value in self._prefilled.items():
            self._model.add(self._x[(position.r, position.c, value)] == 1)

    def _add_knight_move_constraints(self):
        kwargs = dict(r=self.rows_number, c=self.columns_number, blocked=self.cell_blocked)
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        knight_of: dict[tuple, list[Position]] = {}

        for p in self._non_blocked_positions:
            moves: list[Position] = []
            for dr, dc in offsets:
                nr, nc = p.r + dr, p.c + dc
                q = Position(nr, nc)
                if 0 <= nr < kwargs['r'] and 0 <= nc < kwargs['c']:
                    if self._grid[nr][nc] != kwargs['blocked']:
                        moves.append(q)
            knight_of[(p.r, p.c)] = moves

        for k in range(1, self._max_number):
            for p in self._non_blocked_positions:
                neighbours = knight_of[(p.r, p.c)]
                if neighbours:
                    self._model.add(
                        sum(self._x[(q.r, q.c, k + 1)] for q in neighbours)
                        >= self._x[(p.r, p.c, k)]
                    )

    def _exclude_solution(self, solution: Grid):
        lits = []
        for position, value in solution:
            if value != self.cell_blocked:
                lit = self._model.new_bool_var(f"prev_{position.r}_{position.c}")
                self._model.add(self._x[(position.r, position.c, value)] == 1).only_enforce_if(lit)
                self._model.add(self._x[(position.r, position.c, value)] == 0).only_enforce_if(lit.negated())
                lits.append(lit)

        if lits:
            self._model.add_bool_or([lit.negated() for lit in lits])

    def _build_solution(self) -> Grid:
        matrix = [[self.cell_blocked for _ in range(self.columns_number)] for _ in range(self.rows_number)]
        for position in self._non_blocked_positions:
            for k in range(1, self._max_number + 1):
                if self._solver.value(self._x[(position.r, position.c, k)]):
                    matrix[position.r][position.c] = k
                    break
        return Grid(matrix)

