from rebrowser_playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleArukoneNo2x2GridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str) -> Grid:
        size, pqq, pqq_string = self._extract_gpl_data(html_page)
        pqq_string_list = self._split_to_list(pqq_string, size)

        matrix = [[-1 for _ in range(size)] for _ in range(size)]
        for i, val in enumerate(pqq_string_list):
            if val:
                row = i // size
                col = i % size
                matrix[row][col] = int(val)

        return Grid(matrix)