from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleNumberCrossGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            try:
                matrix[row][col] = int(cell.text)
            except ValueError:
                matrix[row][col] = 0

        left = self.make_left(soup)
        up = self.make_top(soup)

        return Grid(matrix), left, up
