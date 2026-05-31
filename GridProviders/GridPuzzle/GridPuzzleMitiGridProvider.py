import re
from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleMitiGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def get_grid(self, url: str) -> tuple[Grid, list[Position]]:
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url: str) -> tuple[list[Position], int]:
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        size_match = re.search(r'gpl\.Size\s*=\s*(\d+);', html_page)
        if not size_match:
            size_match = re.search(r'size\s*:\s*(\d+)', html_page)
        size = int(size_match.group(1))

        dots_match = re.search(r'gpl\.dots\s*=\s*"(.*?)";', html_page)
        dots_string = dots_match.group(1) if dots_match else ""

        dots_positions = []
        dots_cols = size + 1
        for i, char in enumerate(dots_string):
            if char == '#':
                r_idx = i // dots_cols
                c_idx = i % dots_cols
                pos = Position(r_idx - 0.5, c_idx - 0.5)
                dots_positions.append(pos)

        return dots_positions, size
