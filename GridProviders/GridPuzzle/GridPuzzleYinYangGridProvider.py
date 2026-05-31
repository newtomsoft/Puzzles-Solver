from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleYinYangGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        _, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            classes = cell.get('class', [])
            data_val = cell.get('data-val', '')

            if 'b_circle_dot' in classes or data_val == 'b':
                matrix[row][col] = 0  # Black
            elif 'w_circle_dot' in classes or data_val == 'w':
                matrix[row][col] = 1  # White
            else:
                matrix[row][col] = None  # Empty

        return Grid(matrix)
