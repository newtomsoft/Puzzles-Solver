from playwright.sync_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.GridPuzzle.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleRenkatsuPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    def __init__(self, browser: BrowserContext):
        super().__init__(browser)
        self._solution: Grid | None = None

    def play(self, solution: Grid):
        self._solution = solution
        cell_height, cell_width, page, x0, y0 = self._get_canvas_data(solution)
        video, rectangle = self._get_data_video_viewport(page)

        pairs_positions = self._find_unique_different_pairs_positions()
        self._draw_regions(cell_height, cell_width, page, pairs_positions, x0, y0)

        self.close()
        self._process_video(video, "renkatsu", rectangle)

    def _find_unique_different_pairs_positions(self) -> list[tuple[Position, Position]]:
        pairs = []
        if self._solution is None:
            return pairs
        for position, value in self._solution:
            neighbors = filter(None, [self._solution.neighbor_right(position), self._solution.neighbor_down(position)])
            for neighbor in neighbors:
                neighbor_value = self._solution[neighbor]
                if neighbor_value != value:
                    pairs.append((position, neighbor))
        return pairs

    def _draw_regions(self, cell_height, cell_width, page, pairs_positions: list[tuple[Position, Position]], x0, y0):
        for position0, position1 in pairs_positions:
            self._trace(position0.direction_to(position1), position0, page, cell_width, cell_height, x0, y0)

    @staticmethod
    def _trace(direction: Direction, position, page, cell_width, cell_height, x0, y0):
        if direction == Direction.right():
            page.mouse.move(x0 + cell_width + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.down()
            page.mouse.up()
            return
        if direction == Direction.down():
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height + position.r * cell_height)
            page.mouse.down()
            page.mouse.up()
            return