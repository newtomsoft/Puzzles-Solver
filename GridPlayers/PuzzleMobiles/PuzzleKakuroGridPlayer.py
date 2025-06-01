from time import sleep

from Domain.Board.Grid import Grid
from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class PuzzleKakuroGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
        def play(self, solution):
        solution = Grid([line + [0] for line in solution.matrix])
        page = self.browser.pages[0]
        cells = page.locator(".cell")

        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                cells.nth(index).click()
                page.keyboard.press(str(value))

        cls.submit_score(page)
        sleep(60)
