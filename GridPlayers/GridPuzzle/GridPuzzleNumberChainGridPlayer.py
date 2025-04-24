from time import sleep

from playwright.sync_api import BrowserContext

from Board.LinearPathGrid import LinearPathGrid
from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class GridPuzzleNumberChainGridPlayer(GridPlayer, PlaywrightGridPlayer):
    @classmethod
    def play(cls, solution: LinearPathGrid, browser: BrowserContext):
        page = browser.pages[0]
        rows_number = solution.rows_number
        columns_number = solution.columns_number
        bounded_box = page.locator("canvas").bounding_box()
        x0 = bounded_box['x']
        y0 = bounded_box['y']
        width = bounded_box['width']
        height = bounded_box['height']
        cell_width = width / columns_number
        cell_height = height / rows_number
        video, rectangle = cls.get_data_video(page, page, '#puzzle_container', -20, -20, 40, 40)

        page.mouse.move(x0 + cell_width / 2 + solution.path[0].c * cell_width, y0 + cell_height / 2 + solution.path[0].r * cell_height)
        page.mouse.down()
        for position in solution.path[1:]:
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
        page.mouse.up()
        sleep(3)

        browser.close()
        cls.process_video(video, "NumberChain", rectangle)
