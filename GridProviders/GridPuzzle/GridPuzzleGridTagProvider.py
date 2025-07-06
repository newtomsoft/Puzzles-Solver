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

    @staticmethod
    def make_bounded_matrix(row_count, column_count, matrix_cells):
        opens = {'right', 'left', 'top', 'bottom'}
        bounded_matrix = [[set() for _ in range(column_count)] for _ in range(row_count)]
        cell_borders = [[set() for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            cell_border_right, cell_border_bottom = [cls for cls in cell.get('class', []) if 'border' in cls][0].split('_')[1:3]
            if row == 0:
                cell_borders[row][col].add('top')
            if row == row_count - 1:
                cell_borders[row][col].add('bottom')
            if col == 0:
                cell_borders[row][col].add('top')
            if col == column_count - 1:
                cell_borders[row][col].add('right')
            if cell_border_right == '1':
                cell_borders[row][col].add('right')
                if col != column_count - 1:
                    cell_borders[row][col + 1].add('left')
            if cell_border_bottom == '1':
                cell_borders[row][col].add('bottom')
                if row != row_count - 1:
                    cell_borders[row + 1][col].add('top')

            bounded_matrix[row][col] = opens - cell_borders[row][col]
        return bounded_matrix