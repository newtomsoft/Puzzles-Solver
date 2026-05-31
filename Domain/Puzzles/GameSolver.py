from abc import ABC, abstractmethod

from Domain.Board.Grid import Grid


class GameSolver(ABC):
    cell_empty = None

    @abstractmethod
    def __init__(self, *args, **kwargs):
        self._solver = None

    @abstractmethod
    def get_solution(self) -> Grid:
        pass

    @abstractmethod
    def get_other_solution(self) -> Grid:
        pass

    def get_stats(self) -> dict:
        """Return solver statistics. Must be called after get_solution()."""
        return {
            "num_conflicts": self._solver.num_conflicts,
            "num_branches": self._solver.num_branches,
            "wall_time": self._solver.wall_time,
        }