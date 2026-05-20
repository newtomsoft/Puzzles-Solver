from rebrowser_playwright.async_api import BrowserContext
from Domain.Board.Grid import Grid
from Domain.Puzzles.SheepAndWolves.SheepAndWolvesSolver import SheepAndWolvesSolver
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

class GridPuzzleSheepAndWolvesGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        pqq_string_list, size = self._get_canvas_data(html_page)

        grid_matrix = [[None for _ in range(size)] for _ in range(size)]

        for i in range(len(pqq_string_list)):
            row = i // size
            col = i % size
            val = pqq_string_list[i]

            if val == '.':
                grid_matrix[row][col] = None
            elif val == 'S':
                grid_matrix[row][col] = SheepAndWolvesSolver.S
            elif val == 'W':
                grid_matrix[row][col] = SheepAndWolvesSolver.W
            elif val.isdigit():
                grid_matrix[row][col] = int(val)
            else:
                grid_matrix[row][col] = val

        return Grid(grid_matrix)
