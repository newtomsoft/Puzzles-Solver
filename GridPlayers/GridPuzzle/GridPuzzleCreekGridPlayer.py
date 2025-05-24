from time import sleep

from playwright.sync_api import BrowserContext

from Board.Grid import Grid
from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class GridPuzzleCreekGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, grid_solution: Grid, browser: BrowserContext):
        page = browser.pages[0]
        cells = page.query_selector_all("div.g_cell")
        for position, solution_value in [(position, solution_value) for position, solution_value in grid_solution if solution_value]:
            index = position.r * grid_solution.columns_number + position.c
            cells[index].click(click_count=2)

        sleep(6)
