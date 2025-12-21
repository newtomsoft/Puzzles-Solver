from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import (
    GridPuzzleGridCanvasProvider,
)
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleSlitherlinkGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, size = self._get_canvas_data(html_page)
        data_grid = pqq_string_list
        matrix = [[int(number) if (number:=data_grid[i * size + j]) != '.' else ' ' for j in range(size)] for i in range(size)]
        return Grid(matrix)