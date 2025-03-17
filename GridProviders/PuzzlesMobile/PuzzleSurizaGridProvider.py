from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider
from Utils.Grid import Grid


class PuzzleSurizaGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.loop-task-cell')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        number_divs = soup.find_all('div', class_='loop-task-cell')
        rows_number = sum(1 for cell in number_divs if 'left: 4px' in cell['style'])
        columns_number = sum(1 for cell in number_divs if 'top: 4px' in cell['style'])
        matrix = [[' ' for _ in range(columns_number)] for _ in range(rows_number)]
        for index, number_div in enumerate(number_divs):
            row = index // columns_number
            column = index % columns_number
            matrix[row][column] = int(number_div.text) if number_div.text != '' else ' '

        return Grid(matrix)
