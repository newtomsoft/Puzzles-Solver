from time import sleep

from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleHeyawakePlayer(PuzzlesMobilePlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        cells = page.query_selector_all("div.selectable")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if not value:
                cells[index].click()

        sleep(2)
        self.submit_score(page)
        sleep(3)
