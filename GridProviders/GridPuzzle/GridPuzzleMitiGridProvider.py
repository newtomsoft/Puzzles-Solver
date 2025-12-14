from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleMitiGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    def get_grid(self, url: str) -> tuple[Grid, list[Position]]:
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url: str) -> tuple[list[Position], int]:
        page = browser.pages[0]
        page.goto(url)

        data = page.evaluate("""() => {
            const gplData = {};
            if (typeof gpl !== 'undefined') {
                gplData.dots = gpl.dots;
                gplData.Size = gpl.Size;
            }
            return gplData;
        }""")

        if not data or 'dots' not in data:
            raise ValueError("Could not retrieve puzzle data (gpl.dots)")

        size = int(data['Size'])
        dots_string = data['dots']
        dots_positions = []
        dots_cols = size + 1
        for i, char in enumerate(dots_string):
            if char == '#':
                r_idx = i // dots_cols
                c_idx = i % dots_cols
                pos = Position(r_idx - 0.5, c_idx - 0.5)
                dots_positions.append(pos)

        return dots_positions, size
