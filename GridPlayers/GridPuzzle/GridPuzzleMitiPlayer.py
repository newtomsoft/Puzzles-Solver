
from Domain.Board.Grid import Grid
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleMitiPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    game_name = "miti"

    def play(self, solution: Grid):
        # TODO: Implement play logic
        # cell_height, cell_width, page, x0, y0 = self._get_canvas_data(solution.columns_number, solution.rows_number)
        # video, rectangle = self._get_data_video_viewport(page)
        # ... drawing logic ...
        # self.close()
        # self._process_video(video, rectangle)
        pass
