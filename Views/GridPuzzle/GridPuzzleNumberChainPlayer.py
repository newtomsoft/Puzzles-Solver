from Domain.Board.LinearPathGrid import LinearPathGrid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleNumberChainPlayer(PlaywrightPlayer):
    game_name = "number_chain"
    def play(self, solution: LinearPathGrid):
        cell_height, cell_width, page, x0, y0 = self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = self._get_data_video_viewport(page)

        page.mouse.move(x0 + cell_width / 2 + solution.path[0].c * cell_width, y0 + cell_height / 2 + solution.path[0].r * cell_height)
        page.mouse.down()
        for position in solution.path[1:]:
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
        page.mouse.up()

        self.close()
        self._process_video(video, rectangle)
