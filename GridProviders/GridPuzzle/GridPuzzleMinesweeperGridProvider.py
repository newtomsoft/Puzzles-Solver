from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Minesweeper.MinesweeperSolver import MinesweeperSolver
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleMinesweeperGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        _, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            text = cell.text
            matrix[row][col] = int(text) if text != '' else MinesweeperSolver.cell_empty

        return Grid(matrix)
