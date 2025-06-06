from Domain.Board.LinearPathGrid import LinearPathGrid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class ZipPlayer(PlaywrightPlayer):
    def play(self, solution: LinearPathGrid):
        page = self.browser.pages[0]
        frame = page.frames[1]
        game_board = frame.wait_for_selector('.game-board')
        cells_divs = game_board.query_selector_all('div.trail-cell')

        video, rectangle = self._get_data_video(frame, '.grid-board-wrapper', page, -12, -23, 12, 8)

        for position in solution.path:
            self.mouse_click_on_position(page.mouse, solution, position, cells_divs)

        self.close()
        self._process_video(video, "zip", rectangle, 1.5)
