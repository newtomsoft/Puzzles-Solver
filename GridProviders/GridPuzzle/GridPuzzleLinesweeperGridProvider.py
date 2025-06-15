from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridProvider import GridPuzzleGridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleLinesweeperGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        pqq_string_list, size = self.get_canvas_data(html_page)
        data_grid = pqq_string_list[0]
        matrix = [[int(number) if (number:=data_grid[i * size + j]) != '.' else -1 for j in range(size)] for i in range(size)]
        return Grid(matrix)
