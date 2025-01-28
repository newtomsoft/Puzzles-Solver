from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class PuzzleHitoriGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        page = browser.pages[0]
        cells = page.query_selector_all("div.cell.selectable")
        for index, _ in [(solution.get_index(position), value) for position, value in solution if not value]:
            cells[index].click()

        cls.submit_score(page)
        sleep(60)
