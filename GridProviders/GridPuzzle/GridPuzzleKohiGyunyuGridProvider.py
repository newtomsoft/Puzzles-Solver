from rebrowser_playwright.async_api import BrowserContext
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

class GridPuzzleKohiGyunyuGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        pqq_string_list, size = self._get_canvas_data(html_page)

        # In Kohi-Gyunyu, pqq contains 'W' for milk, 'B' for coffee, and '.' for empty.
        # Based on MirukutiGridProvider, we handle 'W', 'V', '1' as Milk and 'B', 'C', '2' as Coffee/Biscuit.
        matrix = []
        for r in range(size):
            row = []
            for c in range(size):
                idx = r * size + c
                if idx < len(pqq_string_list):
                    val = self._convert(pqq_string_list[idx])
                else:
                    val = '.'
                row.append(val)
            matrix.append(row)
        return Grid(matrix)

    @staticmethod
    def _convert(data: str) -> str:
        if data in ('W', 'V', '1'):
            return 'W'  # Milk
        if data in ('B', 'C', '2'):
            return 'B'  # Coffee
        if data in ('G', '3'):
            return 'G'  # Gray circle
        return '.'
