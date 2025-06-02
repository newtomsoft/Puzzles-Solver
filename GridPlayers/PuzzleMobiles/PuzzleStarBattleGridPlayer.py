from time import sleep

from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobilePlayer


class PuzzleStarBattleGridPlayer(PuzzlesMobilePlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        cells = page.locator(".cell, .task-cell")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                cells.nth(index).click()
        sleep(2)
        self.submit_score(page)
        sleep(60)
