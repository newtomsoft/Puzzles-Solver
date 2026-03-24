from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleTrilogyGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            div = cell.find('div')
            if div:
                div_classes = div.get('class', '')
                div_class = div_classes[0] if div_classes else ''
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
