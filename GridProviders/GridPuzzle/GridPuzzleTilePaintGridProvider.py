from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Board.RegionsGrid import RegionsGrid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridTagProvider import GridPuzzleGridTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleTilePaintGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        opens = {'right', 'left', 'top', 'bottom'}
        open_matrix = [[set() for _ in range(column_count)] for _ in range(row_count)]
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

            open_matrix[row][col] = opens - cell_borders[row][col]

        sums_v = [self.extract_sum_value('vl', row_count, soup) for row_count in range(1, row_count + 1)]
        sums_h = [self.extract_sum_value('ht', column_count, soup) for column_count in range(1, column_count + 1)]

        return RegionsGrid(open_matrix), sums_v, sums_h

    @staticmethod
    def extract_sum_value(name: str, column_count: int, soup: BeautifulSoup):
        return int(soup.find('div', id=f'{name}_{column_count}').text) if soup.find('div', id=f'{name}_{column_count}').text != '\xa0' else -1
