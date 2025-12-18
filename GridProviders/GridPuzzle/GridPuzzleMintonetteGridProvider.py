from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleMintonetteGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, size = self._get_canvas_data(html_page)
        data_grid = pqq_string_list
        matrix = [[self.convert_to_domain(data_grid[i * size + j]) for j in range(size)] for i in range(size)]
        return Grid(matrix)

    @staticmethod
    def convert_to_domain(cell_code: str):
        if cell_code == '.':
            return None
        if cell_code == '?':
            return -1  # Empty circle
        if cell_code.isdigit():
            return int(cell_code)
        return None
