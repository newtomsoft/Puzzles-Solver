import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridProvider import GridPuzzleGridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleCreekGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        soup = BeautifulSoup(html_page, 'html.parser')
        matrix_cells = soup.find_all('div', class_='g_cell')

        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count

        matrix = [[-1 for _ in range(column_count+1)] for _ in range(row_count+1)]
        tree_cells = soup.find_all('div', class_='tip_q_num')
        for cell in tree_cells:
            parent_div = cell.parent
            data_id = int(parent_div.get('data-id')) - 1
            row = data_id // column_count
            col = data_id % column_count

            cell_classes = cell.get('class')
            if 'top-100' in cell_classes:
                row += 1
            if 'start-100' in cell_classes:
                col += 1

            text = cell.get_text().strip()
            if text:
                matrix[row][col] = int(text)

        return Grid(matrix)
