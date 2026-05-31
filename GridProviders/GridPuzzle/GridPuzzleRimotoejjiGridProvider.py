from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleRimotoejjiGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str) -> Grid:
        pqq_string_list, size = self._get_canvas_data(html_page)
        symbol_map = {
            'R': '→',
            'L': '←',
            'U': '↑',
            'D': '↓',
            'X': '+',
            '.': ' ',
        }
        matrix = [
            [symbol_map.get(pqq_string_list[i * size + j], pqq_string_list[i * size + j]) for j in range(size)]
            for i in range(size)
        ]
        return Grid(matrix)
