from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class GridPuzzleSnakeGridPlayer(GridPlayer, PlaywrightGridPlayer):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        page = browser.pages[0]
        video, rectangle = cls._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")
        for position_index in [position.r * solution.columns_number + position.c for position, value in solution if value]:
            cells[position_index].click()

        sleep(3)
        browser.close()
        cls._process_video(video, "snake", rectangle, 0)
