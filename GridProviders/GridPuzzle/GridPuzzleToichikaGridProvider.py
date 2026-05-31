import math

from bs4 import BeautifulSoup
from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleToichikaGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, "#puzzle_main")
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        # Parse regions from borders
        opened_grid_matrix = [[set(Direction.orthogonal_directions()) for _ in range(column_count)] for _ in range(row_count)]

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count

            classes = cell.get('class', [])
            h, v = 0, 0
            for cls in classes:
                if cls.startswith('border_'):
                    parts = cls.split('_')
                    if len(parts) == 3:
                        h = int(parts[1])
                        v = int(parts[2])
                        break

            if h == 1:
                opened_grid_matrix[row][col].discard(Direction.right())
                if col + 1 < column_count:
                    opened_grid_matrix[row][col + 1].discard(Direction.left())

            if v == 1:
                opened_grid_matrix[row][col].discard(Direction.down())
                if row + 1 < row_count:
                    opened_grid_matrix[row + 1][col].discard(Direction.up())

            # Edges
            if row == 0:
                opened_grid_matrix[row][col].discard(Direction.up())
            if row == row_count - 1:
                opened_grid_matrix[row][col].discard(Direction.down())
            if col == 0:
                opened_grid_matrix[row][col].discard(Direction.left())
            if col == column_count - 1:
                opened_grid_matrix[row][col].discard(Direction.right())

        opened_grid = Grid(opened_grid_matrix)
        regions_grid = RegionsGrid.from_opened_grid(opened_grid)

        # Parse given arrows (only system arrows with class sys_arrow)
        arrow_map = {'^': 1, 'v': 2, '>': 3, '<': 4}
        given_arrows_matrix = [[0 for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            classes = cell.get('class', [])
            if 'sys_arrow' in classes:
                arrow = cell.get('data-a', '.')
                given_arrows_matrix[row][col] = arrow_map.get(arrow, 0)

        given_arrows_grid = Grid(given_arrows_matrix)

        return regions_grid, given_arrows_grid
