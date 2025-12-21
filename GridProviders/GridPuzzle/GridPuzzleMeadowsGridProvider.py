from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Meadows.MeadowsSolver import MeadowsSolver
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

_ = MeadowsSolver.empty

class GridPuzzleMeadowsGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    count = 0

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, size = await self._get_canvas_data(html_page)
        matrix = [[self._convert(pqq_string_list[i * size + j]) for j in range(size)] for i in range(size)]
        return Grid(matrix)

    def _convert(self, data: str) -> int | MeadowsSolver.empty:
        if data == 'O':
            self.count += 1
            return self.count
        return _
