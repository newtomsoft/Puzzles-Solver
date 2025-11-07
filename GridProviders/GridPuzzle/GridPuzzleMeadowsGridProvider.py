from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Meadows.MeadowsSolver import MeadowsSolver
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

_ = MeadowsSolver.empty

class GridPuzzleMeadowsGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    count = 0

    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        pqq_string_list, size = self._get_canvas_data(html_page)
        matrix = [[self._convert(pqq_string_list[i * size + j]) for j in range(size)] for i in range(size)]
        return Grid(matrix)

    def _convert(self, data: str) -> int | MeadowsSolver.empty:
        if data == 'O':
            self.count += 1
            return self.count
        return _
