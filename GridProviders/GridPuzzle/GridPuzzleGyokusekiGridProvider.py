from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleGyokusekiGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        left = [self.extract_value('vl', row_count, soup) for row_count in range(1, row_count + 1)]
        up = [self.extract_value('ht', column_count, soup) for column_count in range(1, column_count + 1)]
        right = self.extract_values_right(soup)
        down = self.extract_values_down(soup)

        return {'left': left,
                'up': up,
                'right': right,
                'down': down
                }

    @staticmethod
    def extract_value(name: str, column_count: int, soup: BeautifulSoup):
        return int(soup.find('div', id=f'{name}_{column_count}').text) if soup.find('div', id=f'{name}_{column_count}').text != '\xa0' else -1

    @staticmethod
    def extract_values_right(soup) -> list[int]:
        containers = soup.find_all(
            'div',
            class_=lambda c: c and all(cls in c.split() for cls in ['fr_txt', 'd-flex', 'flex-column'])
        )
        if not containers:
            return []
        container = containers[0]
        rows = container.find_all('div', class_='justify-content-around', recursive=False)
        values: list[int] = []
        for row in rows:
            text = row.get_text(strip=True)
            if text == '':
                values.append(-1)
            else:
                try:
                    values.append(int(text))
                except ValueError:
                    values.append(-1)

        return values

    @staticmethod
    def extract_values_down(soup) -> list[int]:
        containers = soup.find_all(
            'div',
            class_=lambda c: c and all(cls in c.split() for cls in ['fb_txt'])
        )
        if not containers:
            return []
        container = containers[0]
        rows = container.find_all('div', class_='flex-fill', recursive=False)
        values: list[int] = []
        for row in rows:
            text = row.get_text(strip=True)
            if text == '':
                values.append(-1)
            else:
                try:
                    values.append(int(text))
                except ValueError:
                    values.append(-1)

        return values

