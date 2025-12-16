import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileRegionGridProvider import PuzzlesMobileRegionGridProvider


class PuzzleHeyawakeGridProvider(PlaywrightGridProvider, PuzzlesMobileRegionGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.selectable')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')

        regions_grid = self._scrap_region_grid(html_page)

        cells_divs = soup.find_all('div', class_='cell')
        matrix_cells = [cell_div for cell_div in cells_divs if 'selectable' in cell_div.get('class', [])]
        numbers_divs = soup.find_all('div', class_='number')
        numbers_str = [text if (text := cell_div.text) else -1 for cell_div in matrix_cells]
        cells_count = len(matrix_cells)
        side = int(math.sqrt(cells_count))
        conversion_base = side + 1
        numbers = [int(number, conversion_base) if number != -1 else -1 for number in numbers_str]
        matrix = []
        for i in range(0, cells_count, side):
            matrix.append(numbers[i:i + side])

        return Grid(matrix), regions_grid
