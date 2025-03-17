import math

from bs4 import BeautifulSoup, Tag
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronGridProvider import PuzzleBaronGridProvider


class PuzzleBaronAkariGridProvider(GridProvider, PlaywrightGridProvider, PuzzleBaronGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.gridbox')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        grid_box_divs = soup.find_all('div', class_='gridbox')
        cells: list[Tag] = list(soup.find_all('div', class_='gridbox'))
        values = [(int(cell.text) if cell.text != '' else -1) if 'tdblack' in cell['class'] else None for cell in cells]
        cells_count = len(grid_box_divs)
        rows_number = int(math.sqrt(cells_count))
        columns_number = rows_number
        if rows_number * columns_number != cells_count:
            raise ValueError("The grid must be square")

        matrix = []
        for r in range(rows_number):
            row = []
            for c in range(columns_number):
                row.append(values[r * columns_number + c])
            matrix.append(row)

        black_cells = {(r, c) for r in range(rows_number) for c in range(columns_number) if matrix[r][c] is not None}
        number_constraints = {(r, c): matrix[r][c] for r in range(rows_number) for c in range(columns_number) if matrix[r][c] is not None and matrix[r][c] != -1}
        return {
            'columns_number': columns_number,
            'rows_number': rows_number,
            'black_cells': black_cells,
            'number_constraints': number_constraints
        }
