import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzleBaron.Base.PuzzleBaronRegionGridProvider import PuzzleBaronRegionGridProvider


class PuzzleBaronCalcudokuGridProvider(PlaywrightGridProvider, PuzzleBaronRegionGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.gridbox')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        grid_box_divs = soup.find_all('div', class_='gridbox')
        numbers_operators = [(int(text[:-1]), text[-1]) if ((text := number_div.get_text()) != '') else None for number_div in grid_box_divs]
        cells_count = len(grid_box_divs)
        rows_count = int(math.sqrt(cells_count))
        columns_count = rows_count
        if rows_count * columns_count != cells_count:
            raise ValueError("The grid must be square")
        matrix = []
        for i in range(0, cells_count, columns_count):
            matrix.append(numbers_operators[i:i + rows_count])
        grid = Grid(matrix)
        positions_numbers_operators = {}
        for position, value in [(position, number_operator) for position, number_operator in grid if number_operator is not None]:
            positions_numbers_operators[position] = value

        regions = self._get_regions_grid(rows_count, columns_count, grid_box_divs)
        position_to_region = {position: region for region in regions for position in region}
        regions_operators_results = []
        for position, (result, operator) in positions_numbers_operators.items():
            region = position_to_region[position]
            regions_operators_results.append((region, operator, result))

        return regions_operators_results
