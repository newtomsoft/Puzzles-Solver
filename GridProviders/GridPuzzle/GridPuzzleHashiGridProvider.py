import math

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleProvider import GridPuzzleProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleHashiGridProvider(PlaywrightGridProvider, GridPuzzleProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.hashi_grid')
        return self.get_grid_from_html(html_page, url)

    def get_grid_from_html(self, html: str, url: str) -> Grid:
        matrix = self._get_grid_data(html)
        return Grid(matrix)

    @staticmethod
    def _get_grid_data(html_page: str) -> list[list]:
        soup = BeautifulSoup(html_page, 'html.parser')
        matrix_cells = soup.find_all('div', class_='cell')
        cells_count = len(matrix_cells)
        if cells_count == 0:
            return []
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        matrix = [[int(value) if (value := matrix_cells[c + r * column_count].text).isdigit() else '_' for c in range(column_count)] for r in range(row_count)]
        return matrix
