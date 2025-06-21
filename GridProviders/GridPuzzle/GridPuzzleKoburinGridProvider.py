from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleKoburinGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        pqq_string_list, size = self._get_canvas_data(html_page)
        matrix = [[-1 if (data:=pqq_string_list[i * size + j]) == "." else int(data) for j in range(size)] for i in range(size)]
        return Grid(matrix)
