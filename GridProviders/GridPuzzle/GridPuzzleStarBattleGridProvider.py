from playwright.sync_api import BrowserContext

from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleStarBattleGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
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

        regions_grid = RegionsGrid(open_matrix)
        stars_count = 2 if 'starbattle2' in url else 1
        return regions_grid, stars_count
