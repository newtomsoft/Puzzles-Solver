import math
from typing import Dict, Tuple, List

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleKillerSudokuGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
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

        cages = self.get_cages(side, soup)
        return Grid(matrix), cages

    @staticmethod
    def get_cages(rows_number: int, soup: BeautifulSoup) -> Dict[int, Tuple[List[Position], int]]:
        columns_number = rows_number
        killer_cages_div = soup.find_all('div', class_='killer')
        cages: Dict[int, Tuple[List[Position], int]] = {}
        for index, cell in enumerate(killer_cages_div):
            row = index // columns_number
            column = index % columns_number
            position: Position = Position(row, column)
            cage_numbers_sum = int(cell.text) if cell.text else -1
            cage_class_cage = str(cell.get('class', [])[1])
            cage_id = int(cage_class_cage.replace('cage', ''))
            if cage_id not in cages:
                cages[cage_id] = ([position], cage_numbers_sum)
            else:
                cages[cage_id][0].append(position)

        return cages
