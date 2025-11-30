from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class MintonetteSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.grid = grid

    def get_solution(self):
        pass

    def get_other_solution(self) -> Grid:
        pass
