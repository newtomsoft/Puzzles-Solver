import math
import re

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronGridProvider import PuzzleBaronGridProvider
from Utils.Grid import Grid
from Utils.Position import Position
from Utils.RegionsGrid import RegionsGrid


class PuzzleBaronCalcudokuGridProvider(GridProvider, PlaywrightGridProvider, PuzzleBaronGridProvider):
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

        regions = self.get_regions(rows_count, grid_box_divs)
        position_to_region = {position: region for region in regions for position in region}
        regions_operators_results = []
        for position, (result, operator) in positions_numbers_operators.items():
            region = position_to_region[position]
            regions_operators_results.append((region, operator, result))

        return regions_operators_results

    @staticmethod
    def get_regions(column_count, cells) -> list[list[Position]]:
        row_count = column_count
        open_matrix = PuzzleBaronCalcudokuGridProvider._build_open_borders_matrix(row_count, column_count, cells)
        regions_grid = RegionsGrid(open_matrix)
        regions_dict = regions_grid.get_regions()
        return [list(region) for region in regions_dict.values()]

    @staticmethod
    def _build_open_borders_matrix(row_count, column_count, cells):
        open_matrix = [[set() for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(cells):
            row = i // column_count
            col = i % column_count
            open_borders = PuzzleBaronCalcudokuGridProvider._get_cell_borders(cell)
            open_matrix[row][col] = open_borders

        return open_matrix

    @staticmethod
    def _get_cell_borders(cell):
        open_border_mappings = {
            1: {'right', 'left', 'top', 'bottom'},
            2: {'right', 'top', 'bottom'},
            3: {'right', 'left', 'bottom'},
            4: {'left', 'top', 'bottom'},
            5: {'right', 'left', 'top'},
            6: {'right', 'bottom'},
            7: {'top', 'bottom'},
            8: {'right', 'top'},
            9: {'left', 'bottom'},
            10: {'right', 'left'},
            11: {'left', 'top'},
            12: {'bottom'},
            13: {'left'},
            14: {'top'},
            15: {'right'},
        }
        layout_class: str = next((cls for cls in cell.get('class', []) if re.match(r'^layout', cls)), '')
        layout = int(layout_class.removeprefix("layout"))
        if layout not in open_border_mappings:
            raise ValueError(f"Invalid layout class: layout{layout}")

        return open_border_mappings[layout]
