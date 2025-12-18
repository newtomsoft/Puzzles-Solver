from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleNanroGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, "#puzzle_main")
        _, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            text = cell.get_text().strip()
            if text:
                matrix[row][col] = int(text)

        opened_grid = self.make_opened_grid(row_count, column_count, matrix_cells)

        return Grid(matrix), RegionsGrid.from_opened_grid(opened_grid)
