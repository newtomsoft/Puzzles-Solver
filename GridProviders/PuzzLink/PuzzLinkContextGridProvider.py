from playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class PuzzLinkContextGridProvider(PlaywrightGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        if len(browser.pages) == 0:
            page = await browser.new_page()
        else:
            page = browser.pages[0]

        await page.goto(url)
        await page.wait_for_selector("#divques svg", state="visible")
        await page.wait_for_function("typeof ui !== 'undefined' && ui.puzzle && ui.puzzle.board")

        number_grid = self._parse_url(url)
        return number_grid

    @staticmethod
    def _parse_url(url: str) -> Grid:
        """Parse a puzz.link context URL manually since puzzlekit does not support it yet."""
        # Extract path after ? or after p?
        if "?" in url:
            path = url.split("?", 1)[1]
        else:
            path = url

        path = path.split("&", 1)[0].split("#", 1)[0]
        parts = [p for p in path.split("/") if p]
        if len(parts) < 4:
            raise ValueError(f"Invalid puzz.link context URL: {url}")

        cols = int(parts[1])
        rows = int(parts[2])
        body = parts[3]

        numbers = PuzzLinkContextGridProvider._decode_number16(body, rows * cols)
        grid_data = []
        for r in range(rows):
            row = []
            for c in range(cols):
                idx = r * cols + c
                val = numbers[idx]
                row.append(val if val is not None else None)
            grid_data.append(row)

        return Grid(grid_data)

    @staticmethod
    def _decode_number16(body: str, max_cells: int):
        """Decode puzz.link number16 format (same as nurikabe family)."""
        numbers = [None] * max_cells
        i = 0
        c = 0

        while i < len(body) and c < max_cells:
            char = body[i]

            if ('0' <= char <= '9') or ('a' <= char <= 'f'):
                numbers[c] = int(char, 16)
                i += 1
                c += 1
            elif char == '-':
                numbers[c] = int(body[i + 1:i + 3], 16)
                i += 3
                c += 1
            elif char == '+':
                numbers[c] = int(body[i + 1:i + 4], 16)
                i += 4
                c += 1
            elif char == '=':
                numbers[c] = int(body[i + 1:i + 4], 16) + 4096
                i += 4
                c += 1
            elif char == '%':
                numbers[c] = int(body[i + 1:i + 4], 16) + 8192
                i += 4
                c += 1
            elif char == '*':
                numbers[c] = int(body[i + 1:i + 5], 16) + 12240
                i += 5
                c += 1
            elif char == '$':
                numbers[c] = int(body[i + 1:i + 6], 16) + 77776
                i += 6
                c += 1
            elif char == '.':
                numbers[c] = None
                i += 1
                c += 1
            elif 'g' <= char <= 'z':
                skip = int(char, 36) - 15
                c += skip
                i += 1
            else:
                i += 1

        return numbers
