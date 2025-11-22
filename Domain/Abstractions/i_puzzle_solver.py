from abc import ABC, abstractmethod

class IPuzzleSolver(ABC):
    @abstractmethod
    def solve(self):
        pass
