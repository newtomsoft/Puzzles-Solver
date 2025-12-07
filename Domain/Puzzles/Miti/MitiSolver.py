
from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class MitiSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._input_grid = grid

    def get_solution(self) -> Grid:
        # TODO: Implement Miti logic
        raise NotImplementedError("Miti logic not implemented yet")
