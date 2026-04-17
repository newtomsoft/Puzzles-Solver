from playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleRegionBorderPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    game_name = None
    board_margin = 0

    def __init__(self, browser: BrowserContext):
        super().__init__(browser)
        self._solution: Grid | None = None

    async def play(self, solution: Grid):
        self._solution = solution
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        pairs_positions = self._find_unique_different_pairs_positions()
        await self._draw_regions(cell_height, cell_width, page, pairs_positions, x0, y0)

        await self.close()
        await self._process_video(video, rectangle)

    def _find_unique_different_pairs_positions(self) -> list[tuple[Position, Position]]:
        if self._solution is None:
            return []

        return self._solution.find_different_neighbors_positions()

    async def _draw_regions(self, cell_height, cell_width, page, pairs_positions: list[tuple[Position, Position]], x0, y0):
        for position0, position1 in pairs_positions:
            await self._click(position0.direction_to(position1), position0, page, cell_width, cell_height, x0, y0)

    @staticmethod
    async def _click(direction: Direction, position, page, cell_width, cell_height, x0, y0):
        if direction == Direction.right():
            await page.mouse.move(x0 + cell_width + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            await page.mouse.down()
            await page.mouse.up()
            return
        if direction == Direction.down():
            await page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height + position.r * cell_height)
            await page.mouse.down()
            await page.mouse.up()
            return
        raise ValueError(f"unexpected direction: {direction}")
