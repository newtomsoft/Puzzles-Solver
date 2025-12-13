from typing import Tuple

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleBinairoPlusGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url) -> tuple[Grid, dict[str, list[Tuple[Position, Position]]]]:
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.cell')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cells = soup.find_all('div', class_=['cell', 'cell-0', 'cell-1'])
        values = [1 if 'cell-0' in cell['class'] else (0 if 'cell-1' in cell['class'] else -1) for cell in cells]
        cells_count = len(values)
        columns_number = sum(1 for cell in cells if 'top: 1px' in cell['style'])
        rows_number = sum(1 for cell in cells if 'left: 1px' in cell['style'])
        if columns_number * rows_number != cells_count:
            raise ValueError("Binairo Plus grid parsing error")
        matrix = []
        for r in range(rows_number):
            row = []
            for c in range(columns_number):
                row.append(values[r * columns_number + c])
            matrix.append(row)
        comparisons = self.get_comparisons_positions(soup)
        return Grid(matrix), comparisons

    @staticmethod
    def get_comparisons_positions(soup) -> dict[str, list[Tuple[Position, Position]]]:
        cell_size = 35
        equal = []
        non_equal = []

        for div_equal_horizontal in soup.find_all('div', class_='eqh'):
            style = div_equal_horizontal['style']
            index_row = int(style.split('top: ')[1].split('px')[0]) // cell_size - 1
            index_column = int(style.split('left: ')[1].split('px')[0]) // cell_size
            equal.append((Position(index_row, index_column), Position(index_row + 1, index_column)))

        for non_equal_horizontal_div in soup.find_all('div', class_='neh'):
            style = non_equal_horizontal_div['style']
            index_row = int(style.split('top: ')[1].split('px')[0]) // cell_size - 1
            index_column = int(style.split('left: ')[1].split('px')[0]) // cell_size
            non_equal.append((Position(index_row, index_column), Position(index_row + 1, index_column)))

        for div_equal_vertical in soup.find_all('div', class_='eqv'):
            style = div_equal_vertical['style']
            index_row = int(style.split('top: ')[1].split('px')[0]) // cell_size
            index_column = int(style.split('left: ')[1].split('px')[0]) // cell_size - 1
            equal.append((Position(index_row, index_column), Position(index_row, index_column + 1)))

        for non_equal_vertical_div in soup.find_all('div', class_='nev'):
            style = non_equal_vertical_div['style']
            index_row = int(style.split('top: ')[1].split('px')[0]) // cell_size
            index_column = int(style.split('left: ')[1].split('px')[0]) // cell_size - 1
            non_equal.append((Position(index_row, index_column), Position(index_row, index_column + 1)))

        return {
            'equal': equal,
            'non_equal': non_equal,
        }
