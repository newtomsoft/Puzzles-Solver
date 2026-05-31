from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleNondangoGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        has_circle_mask = self._make_has_circle_mask(column_count, matrix_cells)
        regions_grid = self._extract_regions(column_count, row_count, matrix_cells)

        return regions_grid, has_circle_mask

    @staticmethod
    def _make_has_circle_mask(column_count: int, matrix_cells) -> Grid:
        grid_data = [[0 for _ in range(column_count)] for _ in range(len(matrix_cells) // column_count)]
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            has_dango = cell.find('div', class_='dango') is not None
            grid_data[row][col] = 1 if has_dango else 0
        return Grid(grid_data)

    @staticmethod
    def _extract_regions(column_count: int, row_count: int, matrix_cells) -> RegionsGrid:
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

            if row == 0:
                opened_grid_matrix[row][col].discard(Direction.up())
            if row == row_count - 1:
                opened_grid_matrix[row][col].discard(Direction.down())
            if col == 0:
                opened_grid_matrix[row][col].discard(Direction.left())
            if col == column_count - 1:
                opened_grid_matrix[row][col].discard(Direction.right())

        opened_grid = Grid(opened_grid_matrix)
        return RegionsGrid.from_opened_grid(opened_grid)
