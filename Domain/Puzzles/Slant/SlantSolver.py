from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class SlantSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.grid = grid

    def get_solution(self) -> Grid:
        # Skeleton implementation
        return self.grid

    def get_other_solution(self) -> Grid:
        return self.grid
