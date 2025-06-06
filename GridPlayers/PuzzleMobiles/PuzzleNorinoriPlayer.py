from time import sleep

from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleNorinoriPlayer(PuzzlesMobilePlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        cells = page.locator(".cell")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                cells.nth(index).click()

        self.submit_score(page)
        sleep(60)
