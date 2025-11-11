from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleNumberCrossGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            try:
                matrix[row][col] = int(cell.text)
            except ValueError:
                matrix[row][col] = 0

        left = self.make_left(soup)
        up = self.make_top(soup)

        return Grid(matrix), left, up
