from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzleBaronGridProvider import PuzzleBaronGridProvider
from Utils.Grid import Grid


class PuzzleBaronVectorsGridProvider(GridProvider, PlaywrightGridProvider, PuzzleBaronGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.gridbox')
        grid_box_divs = page.query_selector_all('div.gridbox')
        div_to_view = page.query_selector('#container')
        div_to_view.scroll_into_view_if_needed()
        numbers = [int(inner_text) if (inner_text := number_div.inner_text()) else '' for number_div in grid_box_divs]
        cells_count = len(grid_box_divs)
        rows_count = len(page.query_selector_all('table.numberlink tr'))
        columns_count = cells_count // rows_count
        matrix = []
        for i in range(0, cells_count, columns_count):
            matrix.append(numbers[i:i + columns_count])
        return Grid(matrix)
