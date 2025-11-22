from abc import abstractmethod

from Domain.Abstractions.i_puzzle_solver import IPuzzleSolver
from Domain.Board.Grid import Grid


class GameSolver(IPuzzleSolver):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_solution(self) -> Grid:
        pass

    def solve(self) -> Grid:
        return self.get_solution()

    @abstractmethod
    def get_other_solution(self) -> Grid:
        pass
