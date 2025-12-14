import math

from bs4 import BeautifulSoup
from bs4.element import AttributeValueList

from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzlesMobileRegionGridProvider(PuzzlesMobileGridProvider):
    @staticmethod
    def _scrap_region_grid(html_page: str):
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_='cell')
        matrix_cells = [cell_div for cell_div in cell_divs if 'selectable' in cell_div.get('class', [])]
        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        borders_dict = {'br': 'right', 'bl': 'left', 'bt': 'top', 'bb': 'bottom'}
        opens = {'right', 'left', 'top', 'bottom'}
        open_matrix = [[set() for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            cell_classes = cell.get('class', AttributeValueList([]))
            if row == 0:
                cell_classes.append('bt')
            if row == row_count - 1:
                cell_classes.append('bb')
            if col == 0:
                cell_classes.append('bl')
            if col == column_count - 1:
                cell_classes.append('br')
            cell_borders = {borders_dict[cls] for cls in cell_classes if cls in borders_dict.keys()}
            open_matrix[row][col] = opens - cell_borders

        regions_grid = RegionsGrid(open_matrix)

        return regions_grid
