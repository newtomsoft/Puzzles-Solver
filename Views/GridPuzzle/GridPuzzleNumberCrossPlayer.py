from Domain.Board.Grid import Grid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleNumberCrossPlayer(PlaywrightPlayer):
    game_name = "number cross"

    def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = self._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")
        for position, solution_value in [(position, solution_value) for position, solution_value in solution if solution_value == 0]:
            index = position.r * solution.columns_number + position.c
            cells[index].click()

        self.close()
        self._process_video(video, rectangle, 0)
