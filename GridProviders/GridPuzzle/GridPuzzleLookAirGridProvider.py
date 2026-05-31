from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleLookAirGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, "#puzzle-main")
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        _, _, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            text = cell.get_text().strip()
            matrix[row][col] = int(text) if text != '' else -1

        return Grid(matrix)
