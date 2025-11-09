from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Minesweeper.MinesweeperSolver import MinesweeperSolver
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Puzzles.Tasukuea.TasukueaSolver import TasukueaSolver


class GridPuzzleTasukueaGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        _, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            text = cell.text
            matrix[row][col] = self.convert(text) if text != '' else MinesweeperSolver.empty

        return Grid(matrix)

    @staticmethod
    def convert(text: str):
        if text == '':
            return TasukueaSolver.empty
        elif text == '?':
            return TasukueaSolver.unknown
        else:
            return int(text)
