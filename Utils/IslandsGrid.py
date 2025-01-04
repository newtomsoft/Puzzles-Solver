from Puzzles.Hashi.Island import Island
from Utils.Grid import Grid
from Utils.Position import Position


class IslandGrid(Grid):
    def __init__(self, matrix: list[list[Island]]):
        super().__init__(matrix)
        self.rows_number = len(matrix)
        self.columns_number = len(matrix[0])

    def add_island(self, position: Position, bridges: int):
        self._matrix[r][c] = bridges