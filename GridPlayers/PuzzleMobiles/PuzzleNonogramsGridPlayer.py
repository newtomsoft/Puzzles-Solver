from time import sleep

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class PuzzleNonogramsGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
        def play(self, solution):
        page = self.browser.pages[0]
        cells = page.query_selector_all("div.cell.selectable")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                cells[index].click()

        cls.submit_score(page)
        sleep(60)
