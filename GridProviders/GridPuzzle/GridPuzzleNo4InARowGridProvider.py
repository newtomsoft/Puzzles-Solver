from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridProvider import GridPuzzleGridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleNo4InARowGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        _, _, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            if 'x1' in cell.get('class'):
                matrix[row][col] = True
            elif 'o1' in cell.get('class'):
                matrix[row][col] = False
            else:
                matrix[row][col] = -1

        return Grid(matrix)
