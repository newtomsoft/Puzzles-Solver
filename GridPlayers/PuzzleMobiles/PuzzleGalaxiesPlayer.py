import asyncio

from playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.PuzzleMobiles.Base.PlayStatus import PlayStatus


class PuzzleGalaxiesPlayer(PuzzlesMobilePlayer):
    def __init__(self, browser: BrowserContext):
        super().__init__(browser)
        self._solution: Grid | None = None

    async def play(self, solution) -> PlayStatus:
        self._solution = solution
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.loop-task-cell")
        different_neighbors_positions = solution.find_different_neighbors_positions()
        await self._draw_regions(cells, page, different_neighbors_positions)

        result = await self.submit_score(page)
        await asyncio.sleep(5)

        return result

    async def _draw_regions(self, cells, page, pairs_positions: list[tuple[Position, Position]]):
        for position0, position1 in pairs_positions:
            index = position0.r * self._solution.columns_number + position0.c
            await self._click(position0.direction_to(position1), page, cells[index])

    @staticmethod
    async def _click(direction: Direction, page, cell):
        box = await cell.bounding_box()
        cell_width = box['width']
        cell_height = box['height']
        x0 = box['x']
        y0 = box['y']
        if direction == Direction.right():
            await page.mouse.move(x0 + cell_width, y0 + cell_height / 2)
            await page.mouse.down()
            await page.mouse.up()
            return
        if direction == Direction.down():
            await page.mouse.move(x0 + cell_width / 2, y0 + cell_height)
            await page.mouse.down()
            await page.mouse.up()
            return
        raise ValueError(f"unexpected direction: {direction}")
