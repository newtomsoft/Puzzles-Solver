from typing import List, Set

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


class RegionsGrid(Grid):
    def __init__(self, matrix: List[List[Set]]):
        super().__init__(matrix)
        self._matrix = self._compute_regions_grid()

    def _compute_regions_grid(self):
        cells_number = self.rows_number * self.columns_number
        while True:
            visited_regions = set()
            regions_count = 0
            matrix = [[None for _ in range(self.columns_number)] for _ in range(self.rows_number)]
            for position, _ in self:
                if position in visited_regions:
                    continue
                regions_count += 1
                region = self._depth_first_search_regions(position)
                for rr, cc in region:
                    matrix[rr][cc] = regions_count
                visited_regions.update(region)
            if len(visited_regions) == cells_number:
                break
        return matrix

    def _depth_first_search_regions(self, current_position: Position, visited=None):
        if visited is None:
            visited = set()
        if current_position in visited:
            return visited
        visited.add(current_position)

        positions = {
            'right': Position(0, 1),
            'left': Position(0, -1),
            'bottom': Position(1, 0),
            'top': Position(-1, 0)
        }
        opened_on = self[current_position]
        for new_position in [current_position + positions[position] for position in positions if position in opened_on and current_position + positions[position] in self]:
            new_visited = self._depth_first_search_regions(new_position, visited)
            if new_visited != visited:
                return new_visited
        return visited
