from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

_ = ''
B = '■'
W = '□'


class GridPuzzleShirokuroGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, size = self._get_canvas_data(html_page)
        matrix = [[self._convert(pqq_string_list[i * size + j]) for j in range(size)] for i in range(size)]
        return Grid(matrix)

    @staticmethod
    def _convert(data: str) -> str:
        if data == 'B':
            return B
        if data == 'W':
            return W
        return _
