from time import sleep

from GridPlayers.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleBinairoPlayer(PuzzlesMobilePlayer, PlaywrightPlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        cells = page.locator(".cell, .task-cell")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                cells.nth(index).click(button="right")
            else:
                cells.nth(index).click()
        self.submit_score(page)
        sleep(60)
