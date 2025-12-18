from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Arofuro.ArofuroSolver import ArofuroSolver
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleArofuroGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            text = cell.get('data-val').strip()
            matrix[row][col] = self.convert(text)

        return Grid(matrix)

    @staticmethod
    def convert(text: str):
        if text == '#':
            return ArofuroSolver.Black
        if text == '':
            return ArofuroSolver.Empty
        return int(text)