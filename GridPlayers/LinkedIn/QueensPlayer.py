from Domain.Board.Grid import Grid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class QueensPlayer(PlaywrightPlayer):
    game_name = "queens"
    def play(self, solution: Grid):
        page = self.browser.pages[0]
        frame = page.frames[0]
        game_board = frame.wait_for_selector('.game-board')
        cells_divs = game_board.query_selector_all('div.queens-cell-with-border')

        video, rectangle = self._get_data_video(frame, '.game-board', page, 12, 23, 12, 8)

        for position in [position for position, value in solution if value]:
            index = position.r * solution.columns_number + position.c
            cell = cells_divs[index]
            if cell.is_enabled():
                cell.click(click_count=2)

        self.close(delay_sec=4)
        self._process_video(video, rectangle, 1.5)
