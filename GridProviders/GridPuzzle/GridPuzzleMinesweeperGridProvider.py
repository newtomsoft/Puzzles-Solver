from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Minesweeper.MinesweeperSolver import MinesweeperSolver
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleMinesweeperGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        _, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            text = cell.text
            matrix[row][col] = int(text) if text != '' else MinesweeperSolver.empty

        return Grid(matrix)
