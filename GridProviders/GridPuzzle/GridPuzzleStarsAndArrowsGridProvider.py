from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleStarsAndArrowsGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        arrow_map = {
            'arrow_1': '→',
            'arrow_2': '↘',
            'arrow_3': '↓',
            'arrow_4': '↙',
            'arrow_5': '←',
            'arrow_6': '↖',
            'arrow_7': '↑',
            'arrow_8': '↗',
        }
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            div = cell.find('div')
            div_classes = div.get('class', ' ')
            if div_classes:
                div_class = div_classes[0]
                matrix[row][col] = arrow_map.get(div_class, '')
            else :
                matrix[row][col] = ''

        count_left = [self.extract_sum_value('vl', row_count, soup) for row_count in range(1, row_count + 1)]
        count_up = [self.extract_sum_value('ht', column_count, soup) for column_count in range(1, column_count + 1)]

        return Grid(matrix), {'up': count_up, 'left': count_left}

    @staticmethod
    def extract_sum_value(name: str, column_count: int, soup: BeautifulSoup):
        return int(soup.find('div', id=f'{name}_{column_count}').text) if soup.find('div', id=f'{name}_{column_count}').text != '\xa0' else -1
