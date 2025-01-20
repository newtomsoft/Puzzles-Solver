import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider
from Utils.Grid import Grid


class PuzzleSkyscrapersGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page)
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        grid_cell_divs = soup.find_all('div', class_=['cell selectable', 'cell selectable immutable'])
        cells_count = len(grid_cell_divs)
        rows_count = math.isqrt(cells_count)
        columns_count = rows_count
        if rows_count * columns_count != cells_count:
            raise ValueError("The grid must be square")
        skyscrapers_level = [int(cell_div.text) if 'immutable' in cell_div.get('class', []) else 0 for cell_div in grid_cell_divs]
        matrix = []
        for i in range(0, cells_count, columns_count):
            matrix.append(skyscrapers_level[i:i + columns_count])

        tasks_right = soup.find_all('div', class_=['task-right'])
        right_numbers = [int(cell_div.text) if cell_div.text else 0 for cell_div in tasks_right]
        tasks_bottom = soup.find_all('div', class_=['task-bottom'])
        bottom_numbers = [int(cell_div.text) if cell_div.text else 0 for cell_div in tasks_bottom]
        tasks_left = soup.find_all('div', class_=['task-left'])
        left_numbers = [int(cell_div.text) if cell_div.text else 0 for cell_div in tasks_left]
        tasks_top = soup.find_all('div', class_=['task-top'])
        top_numbers = [int(cell_div.text) if cell_div.text else 0 for cell_div in tasks_top]
        skyscrapers_levels = {'by_west': left_numbers, 'by_east': right_numbers, 'by_north': top_numbers, 'by_south': bottom_numbers}
        return Grid(matrix), skyscrapers_levels
