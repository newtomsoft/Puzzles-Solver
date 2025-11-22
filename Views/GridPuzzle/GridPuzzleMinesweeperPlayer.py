from GridPlayers.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class GridPuzzleMinesweeperPlayer(PuzzlesMobilePlayer, PlaywrightPlayer):
    game_name = "minesweeper"
    def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = self._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")
        for position in [position for position, value in solution if value]:
            index = position.r * solution.columns_number + position.c
            cells[index].click()

        self.close()
        self._process_video(video, rectangle, 0)
