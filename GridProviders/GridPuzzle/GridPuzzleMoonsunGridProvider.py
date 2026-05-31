from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.Moonsun.MoonsunSolver import MoonsunSolver
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleMoonsunGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        pqq_string_list, ar_string_list, ab_string_list, size = self._get_canvas_data_extended(html_page)
        circle_matrix = [[self.convert(pqq_string_list[i * size + j]) for j in range(size)] for i in range(size)]

        opened_grid = Grid([[set() for _ in range(size)] for _ in range(size)])
        for i in range(len(ar_string_list)):
            position = Position(*divmod(i, size))
            cell_border_right, cell_border_bottom = ar_string_list[i], ab_string_list[i]
            if position not in opened_grid.edge_up_positions() and ab_string_list[i - size] == '0':
                opened_grid[position].add(Direction.up())
            if position not in opened_grid.edge_left_positions() and ar_string_list[i - 1] == '0':
                opened_grid[position].add(Direction.left())
            if cell_border_right == '0':
                opened_grid[position].add(Direction.right())
            if cell_border_bottom == '0':
                opened_grid[position].add(Direction.down())

        return Grid(circle_matrix), RegionsGrid.from_opened_grid(opened_grid)

    @staticmethod
    def convert(value: str):
        match value:
            case 'B':
                return MoonsunSolver.black
            case 'W':
                return MoonsunSolver.white
            case _:
                return None
