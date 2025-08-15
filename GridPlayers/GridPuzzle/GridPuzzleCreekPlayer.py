from Domain.Board.Grid import Grid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleCreekPlayer(PlaywrightPlayer):
    game_name = "creek"
    def play(self, grid_solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = self._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")
        for position in [position for position, solution_value in grid_solution if solution_value]:
            index = position.r * grid_solution.columns_number + position.c
            cells[index].click(click_count=2)

        self.close()
        self._process_video(video, rectangle, 0)
