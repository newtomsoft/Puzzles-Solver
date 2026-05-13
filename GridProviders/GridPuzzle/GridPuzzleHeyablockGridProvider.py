from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleHeyablockGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str) -> tuple:
        soup, row_count, column_count, _, matrix_cells = self._get_grid_data(html_page)
        size = row_count

        grid = self.make_grid(column_count, [[None for _ in range(column_count)] for _ in range(row_count)], matrix_cells)
        region_grid = self._extract_regions(matrix_cells, size)

        return grid, region_grid

    @staticmethod
    def _extract_regions(matrix_cells, size):
        regions = [[0 for _ in range(size)] for _ in range(size)]
        cell_regions = {}
        region_id = 0

        for i in range(size * size):
            row = i // size
            col = i % size
            if (row, col) in cell_regions:
                continue
            region_cells = GridPuzzleHeyablockGridProvider._flood_fill_region(matrix_cells, size, row, col)
            for r, c in region_cells:
                regions[r][c] = region_id
                cell_regions[(r, c)] = region_id
            region_id += 1

        return Grid(regions)

    @staticmethod
    def _flood_fill_region(matrix_cells, size, start_row, start_col):
        result = []
        visited = set()
        queue = [(start_row, start_col)]

        while queue:
            row, col = queue.pop(0)
            if (row, col) in visited:
                continue
            visited.add((row, col))
            result.append((row, col))

            cell_idx = row * size + col
            cell = matrix_cells[cell_idx]
            data_h = cell.get("data-h", "0")
            data_v = cell.get("data-v", "0")

            if col > 0:
                left_cell = matrix_cells[row * size + (col - 1)]
                if left_cell.get("data-v", "0") == "0" and (row, col - 1) not in visited:
                    queue.append((row, col - 1))
            if col < size - 1 and data_v == "0" and (row, col + 1) not in visited:
                queue.append((row, col + 1))
            if row > 0:
                up_cell = matrix_cells[(row - 1) * size + col]
                if up_cell.get("data-h", "0") == "0" and (row - 1, col) not in visited:
                    queue.append((row - 1, col))
            if row < size - 1 and data_h == "0" and (row + 1, col) not in visited:
                queue.append((row + 1, col))

        return result
