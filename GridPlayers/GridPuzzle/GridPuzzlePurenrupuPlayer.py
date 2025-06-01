from time import sleep

from playwright.sync_api import BrowserContext

from Domain.Board.IslandsGrid import IslandGrid
from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.GridPuzzle.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class GridPuzzlePurenrupuPlayer(GridPlayer, PlaywrightGridPlayer, GridPuzzleCanvasPlayer):
    @classmethod
    def play(cls, solution: IslandGrid, browser: BrowserContext):
        cell_height, cell_width, page, x0, y0 = cls._get_canvas_data(browser, solution)
        video, rectangle = cls._get_data_video_viewport(page)

        cls._trace_path(cell_height, cell_width, page, solution, x0, y0)

        sleep(3)
        browser.close()
        cls._process_video(video, "purenrupu", rectangle)
