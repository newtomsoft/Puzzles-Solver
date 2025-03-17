from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer


class PuzzleBaronKenKenGridPlayer(GridPlayer):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        page = browser.pages[0]
        grid_box_divs = page.query_selector_all('div.gridbox')

        for position, digit in solution:
            index = solution.get_index(position)
            grid_box_divs[index].click()
            page.keyboard.press(str(digit))

        sleep(20)
