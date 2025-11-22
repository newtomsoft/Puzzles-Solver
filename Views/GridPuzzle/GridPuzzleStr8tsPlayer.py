from Domain.Board.Grid import Grid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleStr8tsPlayer(PlaywrightPlayer):
    game_name = "str8ts"
    def play(self, solution: tuple[Grid, Grid]):
        grid_solution, grid_blank = solution
        page = self.browser.pages[0]
        video, rectangle = self._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")
        for position, solution_value in [(position, grid_solution[position]) for position, value in grid_blank if value]:
            index = position.r * grid_solution.columns_number + position.c
            cells[index].click()
            page.keyboard.press(str(solution_value))

        self.close()
        self._process_video(video, rectangle, 0)
