from abc import ABC, abstractmethod

from playwright.sync_api import BrowserContext


class GridPlayer(ABC):
    @classmethod
    @abstractmethod
    def play(cls, solution, browser: BrowserContext):
        pass
