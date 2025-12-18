from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleShingokiGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, size = self._get_canvas_data(html_page)
        matrix = [[self.format_value(value) if (value := pqq_string_list[i * size + j]) != '.' else ' ' for j in range(size)] for i in range(size)]
        return Grid(matrix)

    @staticmethod
    def format_value(value):
        return value[1].lower() + value[0] if len(value) > 1 else value.lower() + '0'
