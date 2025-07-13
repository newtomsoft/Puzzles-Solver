from Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from GridPlayers.GridPuzzle.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleWamazuPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    game_name = "wamazu"

    def play(self, solution: IslandGrid):
        cell_height, cell_width, page, x0, y0 = self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = self._get_data_video_viewport(page)

        self._draw_paths(cell_height, cell_width, page, solution, x0, y0)

        self.close()
        self._process_video(video, rectangle)

    def _draw_paths(self, cell_height, cell_width, page, solution, x0, y0):
        start_positions = self._get_circles_starts(solution)
        for start_position in start_positions:
            connected_positions = self._get_connected_positions_from_position(solution, start_position)
            for index, position in enumerate(connected_positions[:-1]):
                next_position = connected_positions[index + 1]
                direction = position.direction_to(next_position)
                self._trace_direction_from_position(direction, position, page, cell_width, cell_height, x0, y0)

    def _get_circles_starts(self, solution: IslandGrid) -> set[Position]:
        circles_positions = self._get_circles_positions(solution)
        ends_circles = set()
        for position in circles_positions:
            if position not in ends_circles:
                end_circle = solution.follow_path(position)[-1]
                ends_circles.add(end_circle)
        return ends_circles

    @staticmethod
    def _get_circles_positions(solution: IslandGrid) -> set[Position]:
        positions = set(position for position, island in solution if island.bridges_count == 1)
        return positions

