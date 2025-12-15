from playwright.sync_api import BrowserContext

from Domain.Board.RegionsGrid import RegionsGrid
from Domain.Puzzles.DosunFuwari.DosunFuwariSolver import DosunFuwariSolver
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleDosunFuwariGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        soup, row_count, column_count, _, matrix_cells = self._get_grid_data(html_page)
        opened_grid = self.make_opened_grid(row_count, column_count, matrix_cells)
        region_grid = RegionsGrid.from_opened_grid(opened_grid)
        for i, cell in enumerate(matrix_cells):
            classes = cell.get('class')
            if not 'black-bg' in classes:
                continue
            row = i // column_count
            col = i % column_count
            region_grid[row][col] = DosunFuwariSolver.wall

        return region_grid
