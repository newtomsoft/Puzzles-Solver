from abc import ABC, abstractmethod

from Domain.Board.Grid import Grid


class GameSolver(ABC):
    no_clue = None

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_solution(self) -> Grid:
        pass

    @abstractmethod
    def get_other_solution(self) -> Grid:
        pass
