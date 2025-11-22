from abc import ABC, abstractmethod

class IGridProvider(ABC):
    @abstractmethod
    def get_grid(self, url: str):
        pass
