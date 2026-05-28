from rebrowser_playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleNorinoriGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        opened_grid = self._make_opened_grid_from_border_classes(row_count, column_count, matrix_cells)
        return RegionsGrid.from_opened_grid(opened_grid)

    @staticmethod
    def _make_opened_grid_from_border_classes(row_count: int, column_count: int, matrix_cells) -> Grid:
        all_borders = set(Direction.orthogonal_directions())
        opened_grid = Grid([[set() for _ in range(column_count)] for _ in range(row_count)])

        right_borders = [[False] * column_count for _ in range(row_count)]
        bottom_borders = [[False] * column_count for _ in range(row_count)]

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            classes = cell.get('class', [])
            for cls in classes:
                if cls.startswith('border_'):
                    parts = cls.split('_')
                    if len(parts) == 3:
                        right_borders[row][col] = parts[1] == '1'
                        bottom_borders[row][col] = parts[2] == '1'
                        break

        for row in range(row_count):
            for col in range(column_count):
                closed_borders = set()
                if right_borders[row][col]:
                    closed_borders.add(Direction.right())
                if bottom_borders[row][col]:
                    closed_borders.add(Direction.down())
                if col == 0 or (col > 0 and right_borders[row][col - 1]):
                    closed_borders.add(Direction.left())
                if row == 0 or (row > 0 and bottom_borders[row - 1][col]):
                    closed_borders.add(Direction.up())
                if col == column_count - 1:
                    closed_borders.add(Direction.right())
                if row == row_count - 1:
                    closed_borders.add(Direction.down())
                opened_grid[Position(row, col)] = all_borders - closed_borders

        return opened_grid
