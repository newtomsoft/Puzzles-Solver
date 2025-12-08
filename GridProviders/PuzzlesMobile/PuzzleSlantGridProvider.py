import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleSlantGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.board-back')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')

        cells_divs = soup.find_all('div', class_='cell')

        rows_number = int(math.sqrt(len(cells_divs)))
        if rows_number * rows_number != len(cells_divs):
             pass

        matrix = [['' for _ in range(rows_number)] for _ in range(rows_number)]

        return Grid(matrix)
