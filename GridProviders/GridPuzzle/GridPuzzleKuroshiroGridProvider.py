from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

_ = ''
B = '■'
W = '□'


class GridPuzzleKuroshiroGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        pqq_string_list, size = self._get_canvas_data(html_page)
        matrix = [[self._convert(pqq_string_list[i * size + j]) for j in range(size)] for i in range(size)]
        return Grid(matrix)

    @staticmethod
    def _convert(data: str) -> str:
        if data == 'B':
            return B
        if data == 'W':
            return W
        return _
