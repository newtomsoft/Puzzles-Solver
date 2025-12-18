from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleTilePaintGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        opened_grid = self.make_opened_grid(row_count, column_count, matrix_cells)
        sums_v = [self.extract_sum_value('vl', row_count, soup) for row_count in range(1, row_count + 1)]
        sums_h = [self.extract_sum_value('ht', column_count, soup) for column_count in range(1, column_count + 1)]

        return RegionsGrid.from_opened_grid(opened_grid), sums_v, sums_h

    @staticmethod
    def extract_sum_value(name: str, column_count: int, soup: BeautifulSoup):
        return int(soup.find('div', id=f'{name}_{column_count}').text) if soup.find('div', id=f'{name}_{column_count}').text != '\xa0' else -1
