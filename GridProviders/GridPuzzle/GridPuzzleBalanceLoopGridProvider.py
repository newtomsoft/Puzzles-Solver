from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.BalanceLoop.BalanceLoopSolver import BalanceLoopSolver
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleBalanceLoopGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, size = await self._get_canvas_data(html_page)
        matrix = [[self.convert_value(pqq_string_list[i * size + j]) for j in range(size)] for i in range(size)]
        return Grid(matrix)

    @staticmethod
    def convert_value(value: str) -> str:
        if value == '':
            return BalanceLoopSolver.empty

        if value == '200':
            return BalanceLoopSolver.black + '0'

        if value == '100':
            return BalanceLoopSolver.white + '0'

        if len(value) >= 3: # black+number
            return BalanceLoopSolver.black + value[2:]

        # withe+value
        return BalanceLoopSolver.white + value
