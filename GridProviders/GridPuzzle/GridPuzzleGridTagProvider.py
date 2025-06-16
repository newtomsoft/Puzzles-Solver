import math

from bs4 import BeautifulSoup, ResultSet, PageElement, Tag, NavigableString

from GridProviders.GridPuzzle.GridPuzzleGridProvider import GridPuzzleGridProvider


class GridPuzzleGridTagProvider(GridPuzzleGridProvider):
    @staticmethod
    def _get_grid_data(html_page: str) -> tuple[BeautifulSoup, int, int, list[list], ResultSet[PageElement | Tag | NavigableString]]:
        soup = BeautifulSoup(html_page, 'html.parser')
        matrix_cells = soup.find_all('div', class_='g_cell')
        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        matrix = [[0 for _ in range(column_count)] for _ in range(row_count)]
        return soup, row_count, column_count, matrix, matrix_cells
