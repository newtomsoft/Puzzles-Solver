from Domain.Board.Grid import Grid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleNanroPlayer(PlaywrightPlayer):
    game_name = "nanro"
    def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = self._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")
        for position, solution_value in [(position, solution[position]) for position, value in solution if value != 0]:
            index = position.r * solution.columns_number + position.c
            if cells[index].text_content().strip() == str(solution_value):
                continue
            cells[index].click()
            page.keyboard.press(str(solution_value))

        self.close()
        self._process_video(video, rectangle, 0)
