from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridTagProvider import GridPuzzleGridTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleTilePaintGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        bounded_matrix = self.make_bounded_matrix(row_count, column_count, matrix_cells)
        sums_v = [self.extract_sum_value('vl', row_count, soup) for row_count in range(1, row_count + 1)]
        sums_h = [self.extract_sum_value('ht', column_count, soup) for column_count in range(1, column_count + 1)]

        return RegionsGrid(bounded_matrix), sums_v, sums_h

    @staticmethod
    def extract_sum_value(name: str, column_count: int, soup: BeautifulSoup):
        return int(soup.find('div', id=f'{name}_{column_count}').text) if soup.find('div', id=f'{name}_{column_count}').text != '\xa0' else -1
