from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleShingokiGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        pqq_string_list, size = self._get_canvas_data(html_page)
        matrix = [[self.format_value(value) if (value := pqq_string_list[i * size + j]) != '.' else ' ' for j in range(size)] for i in range(size)]
        return Grid(matrix)

    @staticmethod
    def format_value(value):
        return value[1].lower() + value[0] if len(value) > 1 else value.lower() + '0'
