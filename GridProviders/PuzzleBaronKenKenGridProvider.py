import math
import re

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzleBaronGridProvider import PuzzleBaronGridProvider
from Utils.Grid import Grid
from Utils.Position import Position
from Utils.RegionsGrid import RegionsGrid


class PuzzleBaronKenKenGridProvider(GridProvider, PlaywrightGridProvider, PuzzleBaronGridProvider):
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
        regions_operators_results = []
        for position, (result, operator) in positions_numbers_operators.items():
            for region in regions:
                if position in region:
                    regions_operators_results.append((region, operator, result))
                    break
        return regions_operators_results

    @staticmethod
    def get_regions(column_count, cells) -> list[list[Position]]:
        row_count = column_count
        opens = {'right', 'left', 'top', 'bottom'}
        open_matrix = [[set() for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(cells):
            row = i // column_count
            col = i % column_count
            layout_class: str = next((cls for cls in cell.get('class', []) if re.match(r'^layout', cls)), '')
            layout = int(layout_class.removeprefix("layout"))
            match layout:
                case 1:
                    cell_borders = {}
                case 2:
                    cell_borders = {'left'}
                case 3:
                    cell_borders = {'top'}
                case 4:
                    cell_borders = {'right'}
                case 5:
                    cell_borders = {'bottom'}
                case 6:
                    cell_borders = {'left', 'top'}
                case 7:
                    cell_borders = {'left', 'right'}
                case 8:
                    cell_borders = {'left', 'bottom'}
                case 9:
                    cell_borders = {'top', 'right'}
                case 10:
                    cell_borders = {'top', 'bottom'}
                case 11:
                    cell_borders = {'right', 'bottom'}
                case 12:
                    cell_borders = {'left', 'top', 'right'}
                case 13:
                    cell_borders = {'right', 'top', 'bottom'}
                case 14:
                    cell_borders = {'left', 'right', 'bottom'}
                case 15:
                    cell_borders = {'left', 'top', 'bottom'}
                case _:
                    raise ValueError(f"Invalid layout class: {layout_class}")
            open_matrix[row][col] = opens - cell_borders

        regions_grid = RegionsGrid(open_matrix)
        regions_dict = regions_grid.get_regions()
        regions = [list(region) for region in regions_dict.values()]
        return regions
