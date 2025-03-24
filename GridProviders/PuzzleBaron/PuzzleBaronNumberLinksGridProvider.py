import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Grid.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronGridProvider import PuzzleBaronGridProvider


class PuzzleBaronNumberLinksGridProvider(GridProvider, PlaywrightGridProvider, PuzzleBaronGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.gridbox')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        grid_box_divs = soup.find_all('div', class_='gridbox')
        numbers = [int(text) if ((text := number_div.get_text()) != '') else 0 for number_div in grid_box_divs]
        cells_count = len(grid_box_divs)
        rows_count = int(math.sqrt(cells_count))
        columns_count = rows_count
        if rows_count * columns_count != cells_count:
            raise ValueError('Invalid grid')
        matrix = []
        for i in range(0, cells_count, columns_count):
            matrix.append(numbers[i:i + columns_count])
        return Grid(matrix)
