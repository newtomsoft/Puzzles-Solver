from playwright.async_api import BrowserContext
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

class GridPuzzleMirukutiGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, size = self._get_canvas_data(html_page)
        
        # In Mirukuti, pqq might contain 'W' for milk, 'B' for biscuit, and '.' for empty.
        # Sometimes there might be other characters, let's be robust.
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
            return 'B'  # Biscuit
        return '.'
