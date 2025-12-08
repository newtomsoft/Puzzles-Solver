from abc import abstractmethod

from playwright.sync_api import Page

from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleSlantPlayer(PuzzlesMobilePlayer):
    def play(self, solution):
        # Skeleton implementation
        # Typically we iterate over the solution grid and click the corresponding cells
        # lines are usually placed by clicking.
        # Click once -> one diagonal
        # Click twice -> other diagonal
        pass
