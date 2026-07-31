from playwright.async_api import BrowserContext

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.GameSolver import GameSolver
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


_ARROW_MAP = {
    1: Direction.up(),
    2: Direction.down(),
    3: Direction.left(),
    4: Direction.right(),
}


class PuzzLinkSashiganeGridProvider(PlaywrightGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        if len(browser.pages) == 0:
            page = await browser.new_page()
        else:
            page = browser.pages[0]

        await page.goto(url)
        await page.wait_for_selector("#divques svg", state="visible")
        await page.wait_for_function("typeof ui !== 'undefined' && ui.puzzle && ui.puzzle.board")

        return self._parse_url(url)

    @staticmethod
    def _parse_url(url: str) -> Grid:
        """Parse a puzz.link sashigane URL manually since puzzlekit does not support it yet."""
        # Extract path after ? or after p?
        if "?" in url:
            path = url.split("?", 1)[1]
        else:
            path = url

        path = path.split("&", 1)[0].split("#", 1)[0]
        parts = [p for p in path.split("/") if p]
        if len(parts) < 4:
            raise ValueError(f"Invalid puzz.link sashigane URL: {url}")

        cols = int(parts[1])
        rows = int(parts[2])
        body = parts[3]

        clues = PuzzLinkSashiganeGridProvider._decode_body(body, rows * cols)
        grid_data = []
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(clues[r * cols + c])
            grid_data.append(row)

        return Grid(grid_data)

    @staticmethod
    def _decode_body(body: str, max_cells: int) -> list:
        """Decode a puzz.link sashigane body (pzprjs loute.js Encode@sashigane).

        Each clue is one char in row-major order:
          - "g","h","i","j"  = arrow clues pointing toward the L pivot;
          - "0"-"9","a"-"f"  = number clues 0..15, "-" + 2 hex = 16..255,
            "." = circle (pivot clue without a number);
          - "@" = outside cell;
          - "k"-"z" = run-length skip of empty cells (value = run + 19 in base 36).
        """
        cells = [None] * max_cells
        c = 0
        i = 0

        while c < max_cells and i < len(body):
            char = body[i]

            if ("0" <= char <= "9") or ("a" <= char <= "f"):
                cells[c] = int(char, 16)
            elif char == "-":
                cells[c] = int(body[i + 1:i + 3], 16)
                i += 2
            elif char == ".":
                cells[c] = 0
            elif char in "%@":
                cells[c] = GameSolver.cell_outside
            elif "g" <= char <= "j":
                cells[c] = _ARROW_MAP[int(char, 20) - 15]
            elif "k" <= char <= "z":
                c += int(char, 36) - 20

            c += 1
            i += 1

        return cells
