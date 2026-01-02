from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleGalaxiesGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page, url)

    def get_grid_from_html(self, html: str, url: str):
        pqq_string_list, original_matrix_size = self._get_canvas_data(html)
        large_size = original_matrix_size * 2 - 1
        large_matrix = [[int(pqq_string_list[i * large_size + j]) for j in range(large_size)] for i in range(large_size)]
        large_grid = Grid(large_matrix)

        circles_positions: dict[int, Position] = {}
        for i, position in enumerate([position/2 for position, value in large_grid if value > 0]):
            circles_positions[i + 1] = position

        return (original_matrix_size, original_matrix_size), circles_positions
