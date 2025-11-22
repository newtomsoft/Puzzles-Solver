from Domain.Board.IslandsGrid import IslandGrid
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleCanvasMultiLoopsPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    def play(self, solution: IslandGrid):
        cell_height, cell_width, page, x0, y0 = self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = self._get_data_video_viewport(page)

        self._draw_multi_loop(cell_height, cell_width, page, solution, x0, y0)

        self.close()
        self._process_video(video, rectangle)


    def _draw_multi_loop(self, cell_height, cell_width, page, solution, x0, y0):
        connected_positions = self._get_connected_positions(solution, False)
        for index, position in enumerate(connected_positions[:-1]):
            next_position = connected_positions[index + 1]
            direction = position.direction_to(next_position)
            self._trace_direction_from_position(direction, position, page, cell_width, cell_height, x0, y0)