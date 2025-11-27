from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleBorderBlockGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    def get_grid(self, url: str) -> tuple[Grid, list[Position]]:
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url: str) -> tuple[Grid, list[Position]]:
        page = browser.pages[0]
        page.goto(url)

        data = page.evaluate("""() => {
            const gplData = {};
            if (typeof gpl !== 'undefined') {
                gplData.pq = gpl.pq;
                gplData.dots = gpl.dots;
                gplData.Size = gpl.Size;
            }
            return gplData;
        }""")

        if not data or 'pq' not in data or 'dots' not in data:
            raise ValueError("Could not retrieve puzzle data (gpl.pq or gpl.dots)")

        size = int(data['Size'])
        pq_string = self._decode_if_custom_base64(data['pq'])
        dots_string = data['dots']

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
