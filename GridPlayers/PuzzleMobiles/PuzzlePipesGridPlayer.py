from time import sleep

from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Pipes.PipeShapeTransition import PipeShapeTransition
from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class PuzzlePipesGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, solution: Grid[PipeShapeTransition], browser: BrowserContext):
        page = browser.pages[0]
        cells = page.query_selector_all("div.selectable")
        for position, pipe_shape_transition in solution:
            index = position.r * solution.columns_number + position.c
            cells[index].click(click_count=pipe_shape_transition.clockwise_rotation)

        sleep(2)
        cls.submit_score(page)
        sleep(60)
