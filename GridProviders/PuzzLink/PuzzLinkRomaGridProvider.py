from collections import deque
from typing import Tuple

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


_ARROW_MAP = {
    1: '↑',
    2: '↓',
    3: '←',
    4: '→',
}


class PuzzLinkRomaGridProvider(PlaywrightGridProvider):
    async def scrap_grid(self, browser, url):
        if len(browser.pages) == 0:
            page = await browser.new_page()
        else:
            page = browser.pages[0]

        await page.goto(url)
        return self._parse_url(url)

    @staticmethod
    def _parse_url(url: str) -> Tuple[Grid, Grid]:
        """Parse a puzz.link roma URL and return (arrows_grid, regions_grid).

        The URL body encodes:
          - cell arrows/numbers via decodeNumber10 (base-10 run-length),
          - cell borders via decodeBorder (base-32 bit-packed),
        then regions are recovered by flood-filling across the borders.
        """
        if "?" in url:
            path = url.split("?", 1)[1]
        else:
            path = url

        path = path.split("&", 1)[0].split("#", 1)[0]
        parts = [p for p in path.split("/") if p]
        if len(parts) < 4:
            raise ValueError(f"Invalid puzz.link roma URL: {url}")

        cols = int(parts[1])
        rows = int(parts[2])
        body = parts[3]

        cell_values, border_data = PuzzLinkRomaGridProvider._decode_body(body, rows, cols)
        arrows_grid = PuzzLinkRomaGridProvider._build_arrows_grid(cell_values, rows, cols)
        regions_grid = PuzzLinkRomaGridProvider._build_regions_grid(border_data, rows, cols)
        return arrows_grid, regions_grid

    @staticmethod
    def _decode_body(body: str, rows: int, cols: int) -> Tuple[list, list]:
        """Decode the puzz.link roma body.

        Returns (cell_values, border_data) where:
          - cell_values[r * cols + c] is an arrow direction (1..4), or None, or GameSolver.cell_empty
          - border_data is a flat list of booleans for vertical then horizontal borders
        """
        max_cells = rows * cols
        vert_borders = (cols - 1) * rows
        horiz_borders = cols * (rows - 1)

        cell_values = [None] * max_cells

        # decodeBorder first (same order as pzprjs Encode@roma)
        bstr = body
        pos1 = min(((vert_borders + 4) // 5), len(bstr))
        pos2 = min(((horiz_borders + 4) // 5) + pos1, len(bstr))

        border_data = [False] * (vert_borders + horiz_borders)
        twi = [16, 8, 4, 2, 1]
        id_ = 0

        for j in range(pos1):
            ca = int(bstr[j], 32)
            for w in range(5):
                if id_ < vert_borders:
                    border_data[id_] = bool(ca & twi[w])
                    id_ += 1

        for j in range(pos1, pos2):
            ca = int(bstr[j], 32)
            for w in range(5):
                if id_ < vert_borders + horiz_borders:
                    border_data[id_] = bool(ca & twi[w])
                    id_ += 1

        # decodeNumber10 on the remaining body
        remaining = bstr[pos2:] if pos2 < len(bstr) else ""
        c = 0
        i = 0
        while c < max_cells and i < len(remaining):
            ca = remaining[i]
            if ca == ".":
                cell_values[c] = -2
            elif "0" <= ca <= "9":
                cell_values[c] = int(ca, 10)
            elif "a" <= ca <= "z":
                c += int(ca, 36) - 10
            c += 1
            i += 1

        return cell_values, border_data

    @staticmethod
    def _build_arrows_grid(cell_values: list, rows: int, cols: int) -> Grid:
        grid_data = []
        for r in range(rows):
            row = []
            for c in range(cols):
                idx = r * cols + c
                val = cell_values[idx]
                if val is None or val == -2:
                    row.append(None)
                elif 1 <= val <= 4:
                    row.append(_ARROW_MAP[val])
                elif val == 5:
                    row.append('G')
                else:
                    row.append(val)
            grid_data.append(row)
        return Grid(grid_data)

    @staticmethod
    def _build_regions_grid(border_data: list, rows: int, cols: int) -> Grid:
        vert_borders = (cols - 1) * rows
        horiz_borders = cols * (rows - 1)

        def has_border(r1: int, c1: int, r2: int, c2: int) -> bool:
            if r1 == r2:
                # vertical border between (r1, c1) and (r2, c2)
                if c1 > c2:
                    c1, c2 = c2, c1
                idx = r1 * (cols - 1) + c1
            else:
                # horizontal border between (r1, c1) and (r2, c2)
                if r1 > r2:
                    r1, r2 = r2, r1
                idx = vert_borders + r1 * cols + c1
            return border_data[idx]

        visited = [[False] * cols for _ in range(rows)]
        regions_grid = [[-1] * cols for _ in range(rows)]
        region_id = 0

        for r in range(rows):
            for c in range(cols):
                if visited[r][c]:
                    continue

                queue = deque([(r, c)])
                visited[r][c] = True
                while queue:
                    cr, cc = queue.popleft()
                    regions_grid[cr][cc] = region_id + 1

                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                            if not has_border(cr, cc, nr, nc):
                                visited[nr][nc] = True
                                queue.append((nr, nc))

                region_id += 1

        return Grid(regions_grid)
