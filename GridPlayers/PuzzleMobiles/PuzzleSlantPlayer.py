from time import sleep

from Domain.Board.Grid import Grid
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleSlantPlayer(PuzzlesMobilePlayer):
    def play(self, solution: Grid):
        page = self.browser.pages[0]
        cell_elements = page.locator('div.cell')

        for position, target_val in solution:
            idx = position.r * solution.columns_number + position.c
            if target_val:
                cell_elements.nth(idx).click(button="left")
            else:
                cell_elements.nth(idx).click(button="right")

        self.submit_score(page)
        sleep(3)
