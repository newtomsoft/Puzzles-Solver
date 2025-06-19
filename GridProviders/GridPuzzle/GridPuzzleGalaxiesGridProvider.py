from playwright.sync_api import BrowserContext

from Board.Position import Position
from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleGalaxiesGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        pqq_string_list, original_matrix_size = self._get_canvas_data(html_page)
        large_size = original_matrix_size * 2 - 1
        large_matrix = [[int(pqq_string_list[i * large_size + j]) for j in range(large_size)] for i in range(large_size)]
        large_grid = Grid(large_matrix)

        circles_positions: dict[int, Position] = {}
        for i, position in enumerate([position/2 for position, value in large_grid if value > 0]):
            circles_positions[i + 1] = position

        return (original_matrix_size, original_matrix_size), circles_positions
