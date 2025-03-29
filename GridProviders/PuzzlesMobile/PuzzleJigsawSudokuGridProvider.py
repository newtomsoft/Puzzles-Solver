import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Board.RegionsGrid import RegionsGrid


class PuzzleJigsawSudokuGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.selectable')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cells_divs = soup.find_all('div', class_='cell')
        matrix_cells = [cell_div for cell_div in cells_divs if 'selectable' in cell_div.get('class', [])]
        numbers_divs = soup.find_all('div', class_='number')
        numbers_str = [text if (text := cell_div.text) else -1 for cell_div in numbers_divs]
        cells_count = len(matrix_cells)
        side = int(math.sqrt(cells_count))
        conversion_base = side + 1
        numbers = [int(number, conversion_base) if number != -1 else -1 for number in numbers_str]
        matrix = []
        for i in range(0, cells_count, side):
            matrix.append(numbers[i:i + side])

        regions = self.get_regions(side, matrix_cells)
        return Grid(matrix), regions

    @staticmethod
    def get_regions(column_count, cells) -> list[list[Position]]:
        row_count = column_count
        borders_dict = {'br': 'right', 'bl': 'left', 'bt': 'top', 'bb': 'bottom'}
        opens = {'right', 'left', 'top', 'bottom'}
        open_matrix = [[set() for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(cells):
            row = i // column_count
            col = i % column_count
            cell_classes = cell.get('class', [])
            if row == 0:
                cell_classes.append('bt')
            if row == row_count - 1:
                cell_classes.append('bb')
            if col == 0:
                cell_classes.append('bl')
            if col == column_count - 1:
                cell_classes.append('br')
            cell_borders = {borders_dict[cls] for cls in cell_classes if cls in borders_dict.keys()}
            open_matrix[row][col] = opens - cell_borders

        regions_grid = RegionsGrid(open_matrix)
        regions_dict = regions_grid.get_regions()
        regions = [list(region) for region in regions_dict.values()]
        return regions

