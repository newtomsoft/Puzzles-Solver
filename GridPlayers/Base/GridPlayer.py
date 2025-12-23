from abc import ABC, abstractmethod

from GridPlayers.Base.PlayStatus import PlayStatus


class GridPlayer(ABC):
    @abstractmethod
    def __init__(self, browser_context):
        self.browser_context = browser_context

    @abstractmethod
    async def play(self, solution) -> PlayStatus:
        pass
