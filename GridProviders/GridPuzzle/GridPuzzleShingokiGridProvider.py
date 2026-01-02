from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleShingokiGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page, url)

    def get_grid_from_html(self, html: str, url: str) -> Grid:
        pqq_string_list, size = self._get_canvas_data(html)
        matrix = [[self.format_value(value) if (value := pqq_string_list[i * size + j]) != '.' else ' ' for j in range(size)] for i in range(size)]
        return Grid(matrix)

    @staticmethod
    def format_value(value):
        return value[1].lower() + value[0] if len(value) > 1 else value.lower() + '0'
