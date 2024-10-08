import math
import re

from playwright.sync_api import BrowserContext

from Grid import Grid
from GridProviders.GridProvider import GridProvider
from PlaywrightGridProvider import PlaywrightGridProvider


class QueensGridProvider(GridProvider, PlaywrightGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.new_page()
        page.goto(url)
        frame = page.frames[1]
        start_game_button = frame.wait_for_selector('button:has-text("Commencer une partie")')
        start_game_button.click()
        queens_board = frame.wait_for_selector('section.queens-board')
        pre_color_class = 'cell-color-'
        color_regex = re.compile(rf'{pre_color_class}(\d+)')
        cell_color_divs = queens_board.query_selector_all(f'div[class*="{pre_color_class}"]')
        colors_numbers = []
        for color_div in cell_color_divs:
            match = color_regex.search(color_div.get_attribute('class'))
            if match:
                colors_numbers.append(int(match.group(1)))
        cells_count = len(colors_numbers)
        side = int(math.sqrt(cells_count))
        matrix = []
        for i in range(0, cells_count, side):
            matrix.append(colors_numbers[i:i + side])
        return Grid(matrix)
