from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleGappyGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        gaps_v = [self.extract_sum_value('vl', row_count, soup) for row_count in range(1, row_count + 1)]
        gaps_h = [self.extract_sum_value('ht', column_count, soup) for column_count in range(1, column_count + 1)]

        return [gaps_v, gaps_h]

    @staticmethod
    def extract_sum_value(name: str, column_count: int, soup: BeautifulSoup):
        return int(soup.find('div', id=f'{name}_{column_count}').text) if soup.find('div', id=f'{name}_{column_count}').text != '\xa0' else -1
