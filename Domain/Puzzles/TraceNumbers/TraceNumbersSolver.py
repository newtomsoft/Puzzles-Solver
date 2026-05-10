from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class TraceNumbersSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self._compute_solution()
        pass

    def _compute_solution(self, blocks: list[Grid] | None = None) -> Grid:
        pass
