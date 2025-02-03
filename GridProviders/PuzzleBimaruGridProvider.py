from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider
from Puzzles.Bimaru.BimaruSolver import BimaruSolver
from Utils.Grid import Grid


class PuzzleBimaruGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page)
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_=['cell'])
        grid_cell_divs = [cell_div for cell_div in cell_divs if 'task' not in cell_div.get('class', []) and 'ship' not in cell_div.get('class', [])]
        rows_count = len([1 for cell in grid_cell_divs if 'left: 3px' in cell['style']])
        columns_count = len([1 for cell in grid_cell_divs if 'top: 3px' in cell['style']])
        cells_count = rows_count * columns_count
        cells = [-1 if 'cell-off' in cell_div.get('class', []) else self.ship_type(cell_div.get('class', [])) for cell_div in grid_cell_divs]
        matrix = []
        for i in range(0, cells_count, columns_count):
            matrix.append(cells[i:i + columns_count])

        task_cells = [cell_div for cell_div in cell_divs if 'task' in cell_div.get('class', [])]
        ships_numbers = [int(cell_div.text) for cell_div in task_cells]
        ships_numbers_by_column_row = {'column': ships_numbers[:rows_count], 'row': ships_numbers[rows_count:]}

        ships_size_cells = [cell_div for cell_div in cell_divs if 'ship' in cell_div.get('class', [])]
        ships_number_by_size = {}
        for cell_div in ships_size_cells:
            classes = cell_div.get('class', [])
            for cls in classes:
                if cls.startswith('ship_helper_'):
                    x = int(cls.split('_')[-1])
                    if x in ships_number_by_size:
                        ships_number_by_size[x] += 1
                    else:
                        ships_number_by_size[x] = 1
        for ships_number in ships_number_by_size.items():
            ships_number_by_size[ships_number[0]] -= ships_number[0]

        return Grid(matrix), ships_numbers_by_column_row, ships_number_by_size

    @staticmethod
    def ship_type(classes: list[str]) -> int:
        if 'ship-bottom' in classes:
            return BimaruSolver.ship_bottom
        if 'ship-top' in classes:
            return BimaruSolver.ship_top
        if 'ship-single' in classes:
            return BimaruSolver.ship_single
        if 'ship-right' in classes:
            return BimaruSolver.ship_right
        if 'ship-left' in classes:
            return BimaruSolver.ship_left
        if 'ship-middle' in classes:
            return BimaruSolver.ship_middle_input
        return BimaruSolver.water
