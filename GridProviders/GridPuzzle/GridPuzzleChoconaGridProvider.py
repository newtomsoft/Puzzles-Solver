from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleChoconaGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        
        # Sur gridpuzzle.com, les bordures des régions semblent être définies par data-h et data-v
        # h=1 signifie bordure à droite, v=1 signifie bordure en bas
        from PuzzleSolver.Board.Position import Position
        from PuzzleSolver.Board.Direction import Direction
        
        opened_grid = Grid([[set() for _ in range(column_count)] for _ in range(row_count)])
        all_borders = set(Direction.orthogonal_directions())

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            pos = Position(row, col)
            
            # Valeurs numériques
            text = cell.get_text().strip()
            matrix[row][col] = int(text) if text else -1
            
            # Bordures pour RegionsGrid
            h = cell.get('data-h')
            v = cell.get('data-v')
            
            closed_borders = set()
            if h == '1': closed_borders.add(Direction.right())
            if v == '1': closed_borders.add(Direction.down())
            
            # Bordures opposées (si elles existent)
            # if col > 0:
            #     prev_cell = matrix_cells[i-1]
            #     if prev_cell.get('data-h') == '1': closed_borders.add(Direction.left())
            # if row > 0:
            #     above_cell = matrix_cells[i-column_count]
            #     if above_cell.get('data-v') == '1': closed_borders.add(Direction.up())
                
            # Bordures extérieures
            # if row == 0: closed_borders.add(Direction.up())
            # if row == row_count - 1: closed_borders.add(Direction.down())
            # if col == 0: closed_borders.add(Direction.left())
            # if col == column_count - 1: closed_borders.add(Direction.right())
            
            opened_grid[pos] = all_borders - closed_borders

        return Grid(matrix), RegionsGrid.from_opened_grid(opened_grid)
