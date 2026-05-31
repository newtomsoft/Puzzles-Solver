from collections import deque
from typing import Any

import puzzlekit

from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider


class PuzzLinkGridProvider(GridProvider):
    @staticmethod
    def decode_url(source: str):
        return puzzlekit.decode(source)

    @staticmethod
    def build_region_grid(ir) -> Grid:
        rows, cols = ir.rows, ir.cols

        region_borders = set()
        for k, v in ir.edges.items():
            (r1, c1), (r2, c2) = k
            if v.edge_type != 2:
                continue
            if c1 == c2:
                cell1 = (min(r1, r2), c1 - 1)
                cell2 = (min(r1, r2), c1)
            else:
                cell1 = (r1 - 1, min(c1, c2))
                cell2 = (r1, min(c1, c2))

            if 0 <= cell1[0] < rows and 0 <= cell1[1] < cols and 0 <= cell2[0] < rows and 0 <= cell2[1] < cols:
                region_borders.add(tuple(sorted([cell1, cell2])))

        visited = set()
        regions_list = []
        for r in range(rows):
            for c in range(cols):
                if (r, c) in visited:
                    continue
                region = []
                queue = deque([(r, c)])
                while queue:
                    cr, cc = queue.popleft()
                    if (cr, cc) in visited:
                        continue
                    visited.add((cr, cc))
                    region.append((cr, cc))
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                            border = tuple(sorted([(cr, cc), (nr, nc)]))
                            if border not in region_borders:
                                queue.append((nr, nc))
                regions_list.append(region)

        regions_grid = [[-1 for _ in range(cols)] for _ in range(rows)]
        for i, region in enumerate(regions_list):
            for rr, cc in region:
                regions_grid[rr][cc] = i

        return Grid(regions_grid)

    @staticmethod
    def build_number_grid(ir) -> Grid:
        rows, cols = ir.rows, ir.cols
        numbers_grid = [[None for _ in range(cols)] for _ in range(rows)]
        for (r, c), cell_state in ir.cells.items():
            if cell_state.number and cell_state.number.value is not None:
                try:
                    numbers_grid[r][c] = int(cell_state.number.value)
                except ValueError:
                    numbers_grid[r][c] = cell_state.number.value
        return Grid(numbers_grid)
