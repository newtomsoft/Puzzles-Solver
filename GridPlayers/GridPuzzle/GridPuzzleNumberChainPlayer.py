from time import sleep

from playwright.sync_api import BrowserContext

from Board.LinearPathGrid import LinearPathGrid
from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class GridPuzzleNumberChainPlayer(GridPlayer, PlaywrightGridPlayer):
    @classmethod
    def play(cls, solution: LinearPathGrid, browser: BrowserContext):
        cell_height, cell_width, page, x0, y0 = cls._get_canvas_data(browser, solution)
        video, rectangle = cls._get_data_video_viewport(page)

        page.mouse.move(x0 + cell_width / 2 + solution.path[0].c * cell_width, y0 + cell_height / 2 + solution.path[0].r * cell_height)
        page.mouse.down()
        for position in solution.path[1:]:
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
        page.mouse.up()

        sleep(2)
        browser.close()
        cls._process_video(video, "numberChain", rectangle)
