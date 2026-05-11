from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleBinairoGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        _, _, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        return self.make_grid(column_count, matrix, matrix_cells)

    @staticmethod
    def make_grid(column_count: int, matrix: list[list], matrix_cells) -> Grid:
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            data_val = cell.get('data-val', '')
            if data_val == 'b':
                matrix[row][col] = 1
            elif data_val == 'w':
                matrix[row][col] = 0
            else:
                matrix[row][col] = None
        return Grid(matrix)
