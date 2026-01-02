from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleYajilinGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page, url)

    def get_grid_from_html(self, html: str, url: str) -> Grid:
        pqq_string_list, size = self._get_canvas_data(html)
        data_grid = pqq_string_list
        matrix = [['' if data_grid[i * size + j] == "." else data_grid[i * size + j] for j in range(size)] for i in range(size)]
        return Grid(matrix)
