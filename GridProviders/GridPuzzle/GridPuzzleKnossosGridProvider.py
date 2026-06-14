from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Knossos.KnossosSolver import KnossosSolver
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

_ = KnossosSolver.cell_empty


class GridPuzzleKnossosGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    """
    Knossos puzzle provider.
    Each region contains exactly one number representing the total perimeter length of that region.
    """

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str) -> Grid:
        """
        Parse Knossos puzzle data from HTML.
        Returns a Grid with numbers for clues and -1 for empty cells.
        """
        pqq_string_list, size = self._get_canvas_data(html_page)

        matrix = [[KnossosSolver.cell_empty for _c in range(size)] for _r in range(size)]
        for i, cell_str in enumerate(pqq_string_list):
            if i >= size * size:
                break
            if cell_str and cell_str.strip() and cell_str != '|':
                try:
                    num_value = int(cell_str)
                    r, c = divmod(i, size)
                    matrix[r][c] = num_value
                except ValueError:
                    pass

        return Grid(matrix)
