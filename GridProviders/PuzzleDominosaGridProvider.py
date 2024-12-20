import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Utils.Grid import Grid


class PuzzleDominosaGridProvider(GridProvider, PlaywrightGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        html_page = page.content()
        browser.close()
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_='cell')
        number_spans = [span for span in cell_divs if span.find('div').find('span')]
        numbers = [int(text) if (text := number_span.get_text()) else -1 for number_span in number_spans]
        cells_count = len(numbers)
        rows_count = int(math.sqrt(cells_count))
        columns_count = rows_count + 1
        if rows_count * columns_count != cells_count:
            raise ValueError("The grid must be a rectangle with columns_count = rows_count + 1")
        matrix = []
        for i in range(0, cells_count, columns_count):
            matrix.append(numbers[i:i + columns_count])
        browser.close()
        return Grid(matrix)
