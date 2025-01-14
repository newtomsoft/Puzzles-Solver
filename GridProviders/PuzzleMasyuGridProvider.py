import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider
from Utils.Grid import Grid


class PuzzleMasyuGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.loop-dot')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        dot_divs = soup.find_all('div', class_='loop-dot')
        dot_numbers = len(dot_divs)
        rows_number = int(math.sqrt(dot_numbers))
        if rows_number * rows_number != dot_numbers:
            raise ValueError('Invalid number of dots')
        columns_number = rows_number
        matrix = [[' ' for _ in range(columns_number)] for _ in range(rows_number)]
        for index, dot_div in enumerate(dot_divs):
            row = index // columns_number
            column = index % columns_number
            if 'dot-white' in dot_div['class']:
                matrix[row][column] = 'w'
                continue
            if 'dot-black' in dot_div['class']:
                matrix[row][column] = 'b'

        return Grid(matrix)
