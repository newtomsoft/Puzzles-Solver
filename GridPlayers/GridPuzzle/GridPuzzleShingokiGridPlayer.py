from time import sleep

from playwright.sync_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class GridPuzzleShingokiGridPlayer(GridPlayer, PlaywrightGridPlayer):
    @classmethod
    def play(cls, solution: IslandGrid, browser: BrowserContext):
        cell_height, cell_width, page, x0, y0 = cls._get_canvas_data(browser, solution)
        video, rectangle = cls._get_data_video_viewport(page)

        for island in solution.islands.values():
            if Direction.right() in island.direction_position_bridges:
                page.mouse.move(x0 + cell_width / 2 + island.position.c * cell_width, y0 + cell_height / 2 + island.position.r * cell_height)
                page.mouse.down()
                page.mouse.move(x0 + cell_width / 2 + (island.position.c + 1) * cell_width, y0 + cell_height / 2 + island.position.r * cell_height)
                page.mouse.up()
            if Direction.down() in island.direction_position_bridges:
                page.mouse.move(x0 + cell_width / 2 + island.position.c * cell_width, y0 + cell_height / 2 + island.position.r * cell_height)
                page.mouse.down()
                page.mouse.move(x0 + cell_width / 2 + island.position.c * cell_width, y0 + cell_height / 2 + (island.position.r + 1) * cell_height)
                page.mouse.up()
        sleep(3)

        browser.close()
        cls._process_video(video, "shingoki", rectangle)
