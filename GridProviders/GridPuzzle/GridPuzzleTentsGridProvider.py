from bs4 import BeautifulSoup, ResultSet, Tag
from bs4.element import NavigableString, PageElement
from rebrowser_playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Tents.TentsSolver import TentsSolver
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleTentsGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    tree_value = -1

    async def scrap_grid(self, browser: BrowserContext, url) -> tuple[Grid, dict]:
        grid, left, up = await self.scrap_grid_left_up(browser, url)
        tents_numbers_by_column_row = {'column': up, 'row': left}
        return grid, tents_numbers_by_column_row

    @staticmethod
    def _get_grid_data(html_page: str) -> tuple[BeautifulSoup, int, int, list[list], ResultSet[PageElement | Tag | NavigableString]]:
        soup = BeautifulSoup(html_page, 'html.parser')
        matrix_cells = soup.find_all('div', class_='g_cell')
        cells_count = len(matrix_cells)

        top_container = soup.find('div', class_='ft_txt')
        column_count = len(top_container.find_all('div', class_='text-center')) if top_container else 0

        left_container = soup.find('div', class_='fl_txt')
        row_count = len(left_container.find_all('div', class_='justify-content-around')) if left_container else 0

        if row_count * column_count != cells_count:
            puzzle_main = soup.find(id='puzzle_main') or soup.find(id='puzzle-main')
            if puzzle_main:
                for cls in puzzle_main.get('class', []):
                    if cls.startswith('ps'):
                        try:
                            row_count = int(cls[2:])
                            column_count = cells_count // row_count
                            break
                        except ValueError:
                            pass

        if row_count * column_count != cells_count:
            import math
            row_count = int(math.sqrt(cells_count))
            column_count = row_count

        matrix = [[0 for _ in range(column_count)] for _ in range(row_count)]
        return soup, row_count, column_count, matrix, matrix_cells

    @staticmethod
    def make_grid(column_count: int, matrix: list[list], matrix_cells: ResultSet[PageElement | Tag | NavigableString]) -> Grid:
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            classes = cell.get('class', [])
            data_a = cell.get('data-a', '')
            if 'tree' in classes or data_a == '#':
                matrix[row][col] = TentsSolver.tree_value
            else:
                matrix[row][col] = 0
        return Grid(matrix)

    def get_grid_left_up_from_html(self, html_page: str) -> tuple[Grid, list, list]:
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        grid = self.make_grid(column_count, matrix, matrix_cells)
        left = self.make_left(soup)
        up = self.make_top(soup)
        return grid, left, up
