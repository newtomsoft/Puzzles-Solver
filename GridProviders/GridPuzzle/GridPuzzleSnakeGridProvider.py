import base64
import math
import re

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class GridPuzzleSnakeGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        matrix_cells = soup.find_all('div', class_='g_cell')
        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        matrix = [[0 for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(matrix_cells):
            if 'body_bg' in cell.get('class'):
                row = i // column_count
                col = i % column_count
                matrix[row][col] = 1

        sums_v = [self.method_name('vl', row_count, soup) for row_count in range(1, row_count + 1)]
        sums_h = [self.method_name('ht', column_count, soup) for column_count in range(1, column_count + 1)]
        return Grid(matrix), sums_v, sums_h,

    @staticmethod
    def method_name(name, column_count, soup):
        return int(soup.find('div', id=f'{name}_{column_count}').text) if soup.find('div', id=f'{name}_{column_count}').text != '\xa0' else -1
