from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer
from Utils.Grid import Grid


class PuzzleKakuroGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        solution = Grid([line + [0] for line in solution.matrix])
        page = browser.pages[0]
        cells = page.locator(".cell")

        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                cells.nth(index).click()
                page.keyboard.press(str(value))

        cls.submit_score(page)
        sleep(60)
