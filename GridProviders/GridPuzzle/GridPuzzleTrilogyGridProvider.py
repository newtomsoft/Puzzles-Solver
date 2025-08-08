from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridTagProvider import GridPuzzleGridTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleTrilogyGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            div = cell.find('div')
            if div:
                div_class = div.get('class', '')[0]
                if div_class == 'circle':
                    matrix[row][col] = 1
                elif div_class == 'square':
                    matrix[row][col] = 2
                elif div_class == 'triangle':
                    matrix[row][col] = 3
                else:
                    matrix[row][col] = 0
            else:
                matrix[row][col] = 0

        return Grid(matrix)
