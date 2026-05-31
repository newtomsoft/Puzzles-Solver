from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Meadows.MeadowsSolver import MeadowsSolver
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

_ = MeadowsSolver.empty

class GridPuzzleMeadowsGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    count = 0

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        pqq_string_list, size = self._get_canvas_data(html_page)
        self.count = 0
        matrix = [[self._convert(pqq_string_list[i * size + j]) for j in range(size)] for i in range(size)]
        return Grid(matrix)

    def _convert(self, data: str) -> int | MeadowsSolver.empty:
        if data == 'O':
            self.count += 1
            return self.count
        return _
