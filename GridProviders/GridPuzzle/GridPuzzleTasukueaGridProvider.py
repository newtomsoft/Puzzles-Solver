from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Tasukuea.TasukueaSolver import TasukueaSolver
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleTasukueaGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        _, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            text = cell.text
            matrix[row][col] = self.convert(text) if text != '' else TasukueaSolver.cell_empty

        return Grid(matrix)

    @staticmethod
    def convert(text: str):
        if text == '':
            return TasukueaSolver.cell_empty
        elif text == '?':
            return TasukueaSolver.unknown
        else:
            return int(text)
