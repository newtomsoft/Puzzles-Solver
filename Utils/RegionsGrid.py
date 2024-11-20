from Utils.Grid import Grid

class RegionsGrid(Grid):
    def __init__(self, matrix: list[list[set]]):
        super().__init__(matrix)
        self._matrix = matrix
        self.rows_number = len(matrix)
        self.columns_number = len(matrix[0])

    def compute_regions_grid(self):
        while True:
            visited_regions = set()
            regions_count = 0
            matrix = [[None for _ in range(self.columns_number)] for _ in range(self.rows_number)]
            for r in range(self.rows_number):
                for c in range(self.columns_number):
                    if (r, c) in visited_regions:
                        continue
                    regions_count += 1
                    region = self._depth_first_search_regions(r, c)
                    for rr, cc in region:
                        matrix[rr][cc] = regions_count
                    visited_regions.update(region)
            if len(visited_regions) == self.rows_number * self.columns_number:
                break
        return Grid(matrix)

    def _depth_first_search_regions(self, r, c, visited=None):
        if visited is None:
            visited = set()
        if (r, c) in visited:
            return visited
        visited.add((r, c))

        directions = {
            'right': (0, 1),
            'left': (0, -1),
            'bottom': (1, 0),
            'top': (-1, 0)
        }
        opened = self._matrix[r][c]
        for direction in directions:
            if direction in opened:
                dr, dc = directions[direction]
                if 0 <= r + dr < self.rows_number and 0 <= c + dc < self.columns_number:
                    new_visited = self._depth_first_search_regions(r + dr, c + dc, visited)
                    if new_visited != visited:
                        return new_visited

        return visited
