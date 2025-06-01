from Domain.Board.IslandsGrid import IslandGrid
from GridPlayers.GridPuzzle.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class GridPuzzleKoburinPlayer(PlaywrightGridPlayer, GridPuzzleCanvasPlayer):
    def play(self, solution: IslandGrid):
        cell_height, cell_width, page, x0, y0 = self._get_canvas_data(solution)
        video, rectangle = self._get_data_video_viewport(page)

        self.mark_black_cells(cell_height, cell_width, page, solution, x0, y0)
        self._draw_path(cell_height, cell_width, page, solution, x0, y0)

        self.close()
        self._process_video(video, "koburin", rectangle)

    def mark_black_cells(self, cell_height, cell_width, page, solution, x0, y0):
        for position in [position for position, value in solution if value == "■"]:
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            self.mouse_click(page)
