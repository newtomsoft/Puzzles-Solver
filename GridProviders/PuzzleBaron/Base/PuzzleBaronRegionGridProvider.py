import re

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.PuzzleBaron.Base.PuzzleBaronGridProvider import PuzzleBaronGridProvider


class PuzzleBaronRegionGridProvider(PuzzleBaronGridProvider):
    @staticmethod
    def _get_regions_grid(row_count: int, column_count: int, cells) -> RegionsGrid:
        opened_grid = PuzzleBaronRegionGridProvider._build_opened_grid(row_count, column_count, cells)
        regions_grid = RegionsGrid.from_opened_grid(opened_grid)
        return regions_grid

    @staticmethod
    def _build_opened_grid(row_count: int, column_count: int, cells) -> Grid:
        opened_grid = Grid([[set() for _ in range(column_count)] for _ in range(row_count)])
        for i, cell in enumerate(cells):
            position = Position(*divmod(i, column_count))
            open_borders = PuzzleBaronRegionGridProvider._get_cell_borders(cell)
            opened_grid[position] = open_borders

        return opened_grid

    @staticmethod
    def _get_cell_borders(cell):
        open_border_mappings = {
            1: {Direction.right(), Direction.left(), Direction.up(), Direction.down()},
            2: {Direction.right(), Direction.up(), Direction.down()},
            3: {Direction.right(), Direction.left(), Direction.down()},
            4: {Direction.left(), Direction.up(), Direction.down()},
            5: {Direction.right(), Direction.left(), Direction.up()},
            6: {Direction.right(), Direction.down()},
            7: {Direction.up(), Direction.down()},
            8: {Direction.right(), Direction.up()},
            9: {Direction.left(), Direction.down()},
            10: {Direction.right(), Direction.left()},
            11: {Direction.left(), Direction.up()},
            12: {Direction.down()},
            13: {Direction.left()},
            14: {Direction.up()},
            15: {Direction.right()},
        }
        layout_class: str = next((cls for cls in cell.get('class', []) if re.match(r'^layout', cls)), '')
        layout = int(layout_class.removeprefix("layout"))
        if layout not in open_border_mappings:
            raise ValueError(f"Invalid layout class: layout{layout}")

        return open_border_mappings[layout]
