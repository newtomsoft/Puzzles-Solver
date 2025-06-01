from Domain.Board.IslandsGrid import IslandGrid
from GridPlayers.GridPuzzle.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class GridPuzzlePurenrupuPlayer(PlaywrightGridPlayer, GridPuzzleCanvasPlayer):
    def play(self, solution: IslandGrid):
        cell_height, cell_width, page, x0, y0 = self._get_canvas_data(solution)
        video, rectangle = self._get_data_video_viewport(page)

        self._draw_path(cell_height, cell_width, page, solution, x0, y0)

        self.close()
        self._process_video(video, "purenrupu", rectangle)
