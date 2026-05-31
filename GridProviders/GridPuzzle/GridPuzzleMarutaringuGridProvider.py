from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleMarutaringuGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, "#puzzle")
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup, row_count, column_count, _, cells = self._get_grid_data(html_page)
        if not cells:
            puzzle_main = soup.find('div', id='puzzle-main') or soup.find('div', class_='puzzle_main')
            cells = puzzle_main.find_all('div', class_='p_cell') if puzzle_main else []

        # Parse regions from borders
        opened_grid_matrix = [[set(Direction.orthogonal_directions()) for _ in range(column_count)] for _ in range(row_count)]
        clues = {}

        for i, cell in enumerate(cells):
            row = i // column_count
            col = i % column_count

            # Borders
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
            
            text = cell.get_text(strip=True)
            if text.isdigit():
                clues[i] = int(text)

        opened_grid = Grid(opened_grid_matrix)
        regions_grid = RegionsGrid.from_opened_grid(opened_grid)

        clues_grid_matrix = [[0 for _ in range(column_count)] for _ in range(row_count)]
        for cell_idx, val in clues.items():
            r = cell_idx // column_count
            c = cell_idx % column_count
            clues_grid_matrix[r][c] = val

        clues_grid = Grid(clues_grid_matrix) if clues else None
        return regions_grid, clues_grid
