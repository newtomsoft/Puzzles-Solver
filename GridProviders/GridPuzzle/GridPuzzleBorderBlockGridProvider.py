import re
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleBorderBlockGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def get_grid(self, url: str) -> tuple[Grid, list[Position]]:
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url: str) -> tuple[Grid, list[Position]]:
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        size_match = re.search(r'gpl\.Size\s*=\s*(\d+);', html_page)
        if not size_match:
            size_match = re.search(r'size\s*:\s*(\d+)', html_page)
        size = int(size_match.group(1))

        pq_match = re.search(r'gpl\.pq\s*=\s*"(.*?)";', html_page)
        pq_raw = pq_match.group(1) if pq_match else ""

        dots_match = re.search(r'gpl\.dots\s*=\s*"(.*?)";', html_page)
        dots_string = dots_match.group(1) if dots_match else ""

        pq_string = self._decode_if_custom_base64(pq_raw)
        pq_list = self._split_to_list(pq_string, size)
        matrix = []
        for r in range(size):
            row = []
            for c in range(size):
                val_str = pq_list[r * size + c]
                if val_str == '.' or val_str == '':
                    row.append(None)
                else:
                    row.append(int(val_str))
            matrix.append(row)

        grid = Grid(matrix)

        dots_positions = []
        dots_cols = size + 1
        for i, char in enumerate(dots_string):
            if char == '#':
                r_idx = i // dots_cols
                c_idx = i % dots_cols
                pos = Position(r_idx - 0.5, c_idx - 0.5)
                dots_positions.append(pos)

        return grid, dots_positions
