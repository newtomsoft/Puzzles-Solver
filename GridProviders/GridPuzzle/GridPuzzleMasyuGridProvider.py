from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleMasyuGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, size = await self._get_canvas_data(html_page)
        data_grid = pqq_string_list
        matrix = [[self.convert_to_domain(data_grid[i * size + j]) for j in range(size)] for i in range(size)]
        return Grid(matrix)

    @staticmethod
    def convert_to_domain(circle_code: str) -> str:
        return {'B': 'b', 'W': 'w', '.': ' '}.get(circle_code, -1)
