from time import sleep

from playwright.sync_api import BrowserContext

from Board.Grid import Grid
from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class GridPuzzleStr8tsPlayer(GridPlayer, PlaywrightGridPlayer):
    @classmethod
    def play(cls, solution: (Grid, Grid), browser: BrowserContext):
        grid_solution, grid_blank = solution
        page = browser.pages[0]
        video, rectangle = cls._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")
        for position, solution_value in [(position, grid_solution[position]) for position, value in grid_blank if value]:
            index = position.r * grid_solution.columns_number + position.c
            cells[index].click()
            page.keyboard.press(str(solution_value))

        sleep(3)
        browser.close()
        cls._process_video(video, "str8ts", rectangle, 0)
