from rebrowser_playwright.async_api import BrowserContext
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

class GridPuzzleRabbitsAndTreesGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url) -> Grid:
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        # GridPuzzleTagProvider.make_grid handles cell.text conversion to int or None
        grid = self.make_grid(column_count, matrix, matrix_cells)
        return grid
