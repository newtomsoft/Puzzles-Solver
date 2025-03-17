from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer
from Pipes.PipeShapeTransition import PipeShapeTransition
from Utils.Grid import Grid


class PuzzlePipesGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, solution: Grid[PipeShapeTransition], browser: BrowserContext):
        page = browser.pages[0]
        cells = page.query_selector_all("div.selectable")
        for position, pipe_shape_transition in solution:
            index = position.r * solution.columns_number + position.c
            for _ in range(pipe_shape_transition.clockwise_rotation):
                cells[index].click()

        sleep(2)
        cls.submit_score(page)
        sleep(60)
