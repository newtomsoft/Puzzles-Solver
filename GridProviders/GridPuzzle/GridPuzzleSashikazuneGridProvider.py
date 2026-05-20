import re
from rebrowser_playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleSashikazuneGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str) -> Grid:
        pqq_string_list, size = self._get_canvas_data(html_page)

        grid = []
        for r in range(size):
            row = []
            for c in range(size):
                val = pqq_string_list[r * size + c]
                if val == "":
                    row.append(None)
                else:
                    try:
                        row.append(int(val))
                    except ValueError:
                        row.append(val)
            grid.append(row)

        return Grid(grid)
