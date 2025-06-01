from time import sleep

from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class PuzzleAkariGridPlayer(PuzzlesMobileGridPlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        cells = page.query_selector_all("div.cell, div.light-up-task-cell")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                cells[index].click()

        self.submit_score(page)
        sleep(60)
