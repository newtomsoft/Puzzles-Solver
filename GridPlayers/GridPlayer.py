from abc import ABC

from playwright.sync_api import BrowserContext


class GridPlayer(ABC):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        pass
