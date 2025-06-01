from time import sleep

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class PuzzleStarBattleGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
        def play(self, solution):
        page = self.browser.pages[0]
        cells = page.locator(".cell, .task-cell")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                cells.nth(index).click()
        sleep(2)
        cls.submit_score(page)
        sleep(60)
