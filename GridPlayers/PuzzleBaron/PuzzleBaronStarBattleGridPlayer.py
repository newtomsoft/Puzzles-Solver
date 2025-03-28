from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer


class PuzzleBaronStarBattleGridPlayer(GridPlayer):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        page = browser.pages[0]
        grid_box_divs = page.query_selector_all('div.box')

        for position, _ in [(position, value) for position, value in solution if value]:
            index = solution.get_index_from_position(position)
            grid_box_divs[index].click(click_count=2)

        sleep(20)
