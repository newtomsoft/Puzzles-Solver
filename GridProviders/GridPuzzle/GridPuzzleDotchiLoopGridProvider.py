from playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleDotchiLoopGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    _ = 0
    B = 1
    W = 2

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, ar_string_list, ab_string_list, size = self._get_canvas_data_extended(html_page)

        value_matrix = [[self.convert(value) if (value:=pqq_string_list[i * size + j]) != '' else self._ for j in range(size)] for i in range(size)]

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

        return RegionsGrid.from_opened_grid(opened_grid), Grid(value_matrix)

    @staticmethod
    def convert(value: str):
        if value == 'B':
            return GridPuzzleDotchiLoopGridProvider.B
        elif value == 'W':
            return GridPuzzleDotchiLoopGridProvider.W
        else:
            return GridPuzzleDotchiLoopGridProvider._
