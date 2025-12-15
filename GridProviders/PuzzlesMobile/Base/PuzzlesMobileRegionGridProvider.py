import math

from bs4 import BeautifulSoup
from bs4.element import AttributeValueList

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
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
        borders_dict = {'br': Direction.right(), 'bl': Direction.left(), 'bt': Direction.up(), 'bb': Direction.down()}
        all_borders = set(Direction.orthogonal_directions())
        opened_grid = Grid([[set() for _ in range(column_count)] for _ in range(row_count)])
        for i, cell in enumerate(matrix_cells):
            position = Position(*divmod(i, column_count))
            classes = cell.get('class', AttributeValueList([]))
            closed_borders = (
                    {borders_dict[cls] for cls in classes if cls in borders_dict}
                    | ({Direction.up()} if position in opened_grid.edge_up_positions() else set())
                    | ({Direction.down()} if position in opened_grid.edge_down_positions() else set())
                    | ({Direction.left()} if position in opened_grid.edge_left_positions() else set())
                    | ({Direction.right()} if position in opened_grid.edge_right_positions() else set())
            )
            opened_grid[position] = all_borders - closed_borders

        return RegionsGrid.from_opened_grid(opened_grid)
