from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleDotchiLoopGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    _ = 0
    B = 1
    W = 2

    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        pqq_string_list, ar_string_list, ab_string_list, size = self._get_canvas_data_extended(html_page)

        value_matrix = [[self.convert(value) if (value:=pqq_string_list[i * size + j]) != '' else self._ for j in range(size)] for i in range(size)]

        open_matrix = [[set() for _ in range(size)] for _ in range(size)]
        for i in range(len(ar_string_list)):
            row = i // size
            col = i % size
            cell_border_right, cell_border_bottom = ar_string_list[i], ab_string_list[i]
            if row > 0 and ab_string_list[i - size] == '0':
                open_matrix[row][col].add('top')
            if col > 0 and ar_string_list[i - 1] == '0':
                open_matrix[row][col].add('left')
            if cell_border_right == '0':
                open_matrix[row][col].add('right')
            if cell_border_bottom == '0':
                open_matrix[row][col].add('bottom')

        return RegionsGrid(open_matrix), Grid(value_matrix)

    @staticmethod
    def convert(value: str):
        if value == 'B':
            return GridPuzzleDotchiLoopGridProvider.B
        elif value == 'W':
            return GridPuzzleDotchiLoopGridProvider.W
        else:
            return GridPuzzleDotchiLoopGridProvider._
