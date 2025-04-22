from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class GridPuzzleNo4InARowGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        page = browser.pages[0]
        cells = page.query_selector_all("div.g_cell")
        previous_value = False
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            class_attr = cells[index].get_attribute('class')
            if 'x1' in class_attr or 'o1' in class_attr:
                continue
            if value == previous_value:
                cells[index].click()
            else:
                cells[index].click(click_count=2)
            previous_value = value

        sleep(6)
