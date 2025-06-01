from time import sleep

from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class PuzzleAquariumGridPlayer(PuzzlesMobileGridPlayer, PlaywrightGridPlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        cells = page.query_selector_all("div.selectable")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                cells[index].click()

        sleep(2)
        self.submit_score(page)
        sleep(60)
