from abc import ABC, abstractmethod


class GridPlayer(ABC):
    @abstractmethod
    def play(self, solution):
        pass
