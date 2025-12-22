from playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleCountryRoadGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, ar_string_list, ab_string_list, size = self._get_canvas_data_extended(html_page)
        numbers_matrix = [[int(number) if (number:=pqq_string_list[i * size + j]) != '' else None for j in range(size)] for i in range(size)]

        open_grid = Grid([[set() for _ in range(size)] for _ in range(size)])
        for i in range(len(ar_string_list)):
            row = i // size
            col = i % size
            position = Position(row, col)
            cell_border_right, cell_border_bottom = ar_string_list[i], ab_string_list[i]
            if row > 0 and ab_string_list[i - size] == '0':
                open_grid[position].add(Direction.up())
            if col > 0 and ar_string_list[i - 1] == '0':
                open_grid[position].add(Direction.left())
            if cell_border_right == '0':
                open_grid[position].add(Direction.right())
            if cell_border_bottom == '0':
                open_grid[position].add(Direction.down())

        return Grid(numbers_matrix), RegionsGrid.from_opened_grid(open_grid)
