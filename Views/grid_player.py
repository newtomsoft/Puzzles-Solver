from abc import ABC, abstractmethod


class GridPlayer(ABC):
    @abstractmethod
    def __init__(self, browser_context):
        self.browser_context = browser_context

    @abstractmethod
    def play(self, solution):
        pass
