import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.Base.GridPuzzleProvider import GridPuzzleProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleHashiGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url, '.hashi_grid')
        matrix = self._get_grid_data(html_page)
        return Grid(matrix)

    @staticmethod
    def _get_grid_data(html_page: str) -> list[list]:
        soup = BeautifulSoup(html_page, 'html.parser')
        matrix_cells = soup.find_all('div', class_='cell')
        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        matrix = [[int(value) if (value := matrix_cells[c + r * column_count].text).isdigit() else '_' for c in range(column_count)] for r in range(row_count)]
        return matrix
