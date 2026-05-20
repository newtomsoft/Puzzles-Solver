from collections import deque
from rebrowser_playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleProvider import GridPuzzleProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleHeyawakeGridProvider(PlaywrightGridProvider, GridPuzzleProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str) -> tuple:
        from bs4 import BeautifulSoup
        import math

        soup = BeautifulSoup(html_page, "html.parser")
        matrix_cells = soup.find_all("div", class_="g_cell")
        cells_count = len(matrix_cells)
        size = int(math.sqrt(cells_count))

        matrix = [[None for _ in range(size)] for _ in range(size)]
        regions = [[0 for _ in range(size)] for _ in range(size)]

        for i, cell in enumerate(matrix_cells):
            row = i // size
            col = i % size
            text = cell.get_text(strip=True)
            try:
                val = int(text)
                matrix[row][col] = val if val >= 0 else None
            except ValueError:
                matrix[row][col] = None

        cell_regions = {}
        region_id = 0

        for i, cell in enumerate(matrix_cells):
            row = i // size
            col = i % size

            if (row, col) in cell_regions:
                continue

            region_cells = self._flood_fill_region(matrix_cells, size, row, col)
            for r, c in region_cells:
                regions[r][c] = region_id
                cell_regions[(r, c)] = region_id
            region_id += 1

        return Grid(matrix), Grid(regions)

    @staticmethod
    def _flood_fill_region(matrix_cells, size, start_row, start_col):
        result = []
        visited = set()
        queue = deque([(start_row, start_col)])

        while queue:
            row, col = queue.popleft()
            if (row, col) in visited:
                continue
            visited.add((row, col))
            result.append((row, col))

            cell_idx = row * size + col
            cell = matrix_cells[cell_idx]
            data_h = cell.get("data-h", "0")
            data_v = cell.get("data-v", "0")

            neighbors = []
            if col > 0:
                left_cell_idx = row * size + (col - 1)
                left_cell = matrix_cells[left_cell_idx]
                if left_cell.get("data-v", "0") == "0":
                    neighbors.append((row, col - 1))
            if col < size - 1 and data_v == "0":
                neighbors.append((row, col + 1))
            if row > 0:
                up_cell_idx = (row - 1) * size + col
                up_cell = matrix_cells[up_cell_idx]
                if up_cell.get("data-h", "0") == "0":
                    neighbors.append((row - 1, col))
            if row < size - 1 and data_h == "0":
                neighbors.append((row + 1, col))

            for nr, nc in neighbors:
                if (nr, nc) not in visited:
                    queue.append((nr, nc))

        return result
