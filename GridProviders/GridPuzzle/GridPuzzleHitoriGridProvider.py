import math
from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleHitoriGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    @staticmethod
    def _get_grid_data(html_page: str):
        soup = BeautifulSoup(html_page, 'html.parser')
        matrix_cells = soup.find_all('div', class_='cell')
        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        matrix = [[0 for _ in range(column_count)] for _ in range(row_count)]
        return soup, row_count, column_count, matrix, matrix_cells

    def get_grid_from_html(self, html_page: str):
        _, _, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            matrix[row][col] = int(cell.get_text(strip=True))
        return Grid(matrix)
