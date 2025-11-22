from abc import ABC, abstractmethod

class IView(ABC):
    @abstractmethod
    def show_grid(self, grid):
        pass
