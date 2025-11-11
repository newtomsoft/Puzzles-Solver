import math

from bs4 import BeautifulSoup, ResultSet, Tag
from bs4.element import NavigableString, PageElement
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleProvider import GridPuzzleProvider


class GridPuzzleTagProvider(GridPuzzleProvider):
    @staticmethod
    def _get_grid_data(html_page: str) -> tuple[BeautifulSoup, int, int, list[list], ResultSet[PageElement | Tag | NavigableString]]:
        soup = BeautifulSoup(html_page, 'html.parser')
        matrix_cells = soup.find_all('div', class_='g_cell')
        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        matrix = [[0 for _ in range(column_count)] for _ in range(row_count)]
        return soup, row_count, column_count, matrix, matrix_cells

    @staticmethod
    def make_grid(column_count: int, matrix: list[list], matrix_cells: ResultSet[PageElement | Tag | NavigableString]) -> Grid:
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            try:
                matrix[row][col] = int(cell.text)
            except ValueError:
                matrix[row][col] = None

        grid = Grid(matrix)
        return grid

    def scrap_grid_left_up(self, browser: BrowserContext, url) -> tuple[Grid, list, list]:
        html_page = self.get_html(browser, url)
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        grid = self.make_grid(column_count, matrix, matrix_cells)
        left = self.make_left(soup)
        up = self.make_top(soup)
        return grid, left, up

    @staticmethod
    def make_clues(soup: BeautifulSoup, place_first_letter: str) -> list:
        """Return clues for a given grid position: init_place = t=> top; b=> bottom; l=> left; r=> right"""
        if place_first_letter not in {'t', 'b', 'l', 'r'}:
            raise ValueError(f'Invalid init_place: {place_first_letter}')

        container = soup.find('div', class_=f'f{place_first_letter}_txt')
        result = []
        if container:
            class_value = 'text-center' if place_first_letter in {'t', 'b'} else 'justify-content-around'
            clue_divs = container.find_all('div', class_={class_value})
            for div in clue_divs:
                text = div.get_text(strip=True)
                try:
                    result.append(int(text))
                except (ValueError, AttributeError):
                    result.append(None)

        return result

    @staticmethod
    def make_top(soup: BeautifulSoup) -> list:
        container = soup.find('div', class_='ft_txt')
        result = []
        if container:
            up_divs = container.find_all('div', class_='text-center')
            for div in up_divs:
                text = div.get_text(strip=True)
                try:
                    result.append(int(text))
                except (ValueError, AttributeError):
                    result.append(None)
        return result

    @staticmethod
    def make_right(soup) -> list:
        container = soup.find('div', class_='fr_txt')
        result = []
        if container:
            left_divs = container.find_all('div', class_='justify-content-around')
            for div in left_divs:
                text = div.get_text(strip=True)
                text = text.replace('\xa0', '').strip()
                try:
                    result.append(int(text))
                except (ValueError, AttributeError):
                    result.append(None)
        return result

    @staticmethod
    def make_bottom(soup) -> list:
        container = soup.find('div', class_='fb_txt')
        result = []
        if container:
            up_divs = container.find_all('div', class_='text-center')
            for div in up_divs:
                text = div.get_text(strip=True)
                try:
                    result.append(int(text))
                except (ValueError, AttributeError):
                    result.append(None)
        return result

    @staticmethod
    def make_left(soup: BeautifulSoup) -> list:
        container = soup.find('div', class_='fl_txt')
        result = []
        if container:
            left_divs = container.find_all('div', class_='justify-content-around')
            for div in left_divs:
                text = div.get_text(strip=True)
                text = text.replace('\xa0', '').strip()
                try:
                    result.append(int(text))
                except (ValueError, AttributeError):
                    result.append(None)
        return result

    @staticmethod
    def make_bounded_matrix(row_count, column_count, matrix_cells):
        opens = {'right', 'left', 'top', 'bottom'}
        bounded_matrix = [[set() for _ in range(column_count)] for _ in range(row_count)]
        cell_borders = [[set() for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            cell_border_right, cell_border_bottom = [cls for cls in cell.get('class', []) if 'border' in cls][0].split('_')[1:3]
            if row == 0:
                cell_borders[row][col].add('top')
            if row == row_count - 1:
                cell_borders[row][col].add('bottom')
            if col == 0:
                cell_borders[row][col].add('top')
            if col == column_count - 1:
                cell_borders[row][col].add('right')
            if cell_border_right == '1':
                cell_borders[row][col].add('right')
                if col != column_count - 1:
                    cell_borders[row][col + 1].add('left')
            if cell_border_bottom == '1':
                cell_borders[row][col].add('bottom')
                if row != row_count - 1:
                    cell_borders[row + 1][col].add('top')

            bounded_matrix[row][col] = opens - cell_borders[row][col]
        return bounded_matrix
