from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleMidLoopGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        pqq_string_list, matrix_size = self._get_canvas_data(html_page)
        large_size = matrix_size * 2 - 1
        large_matrix = [[False if pqq_string_list[i * large_size + j] == '.' else True for j in range(large_size)] for i in range(large_size)]
        large_grid = Grid(large_matrix)

        circles_positions: dict[int, Position] = {}
        for i, position in enumerate([position/2 for position, value in large_grid if value]):
            circles_positions[i + 1] = position

        return (matrix_size, matrix_size), circles_positions
