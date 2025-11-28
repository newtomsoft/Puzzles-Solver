from playwright.sync_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.GridPuzzle.Base.GridPuzzleTagByBlockPlayer import GridPuzzleTagByBlockPlayer


class GridPuzzleBorderBlockPlayer(GridPuzzleTagByBlockPlayer):
    game_name = "border-block"
    board_margin = 8

    def __init__(self, browser: BrowserContext):
        super().__init__(browser)
        self._solution: Grid = Grid.empty()

    def play(self, solution: Grid):
        self._solution = solution
        cell_height, cell_width, page, x0, y0 = self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = self._get_data_video_viewport(page)

        pairs_positions = self._find_unique_different_pairs_positions()
        self._draw_regions(cell_height, cell_width, page, pairs_positions, x0, y0)

        self.close()
        self._process_video(video, rectangle)

    def _find_unique_different_pairs_positions(self) -> list[tuple[Position, Position]]:
        pairs: list[tuple[Position, Position]] = list()
        if self._solution is None:
            return pairs

        min_value = self._solution.min_value()
        max_value = self._solution.max_value()

        for cell_value in range(min_value, max_value + 1):
            for cell_position in [position for position, value in self._solution if value == cell_value]:
                for neighbor_position in self._solution.neighbors_positions(cell_position):
                    neighbor_value = self._solution[neighbor_position]
                    if neighbor_value != cell_value:
                        pair = (cell_position, neighbor_position) if cell_position < neighbor_position else (neighbor_position, cell_position)
                        if pair not in pairs:
                            pairs.append(pair)
        return pairs

    def _draw_regions(self, cell_height, cell_width, page, pairs_positions: list[tuple[Position, Position]], x0, y0):
        for position0, position1 in pairs_positions:
            self._click(position0.direction_to(position1), position0, page, cell_width, cell_height, x0, y0)

    @staticmethod
    def _click(direction: Direction, position, page, cell_width, cell_height, x0, y0):
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
        raise ValueError(f"unexpected direction: {direction}")