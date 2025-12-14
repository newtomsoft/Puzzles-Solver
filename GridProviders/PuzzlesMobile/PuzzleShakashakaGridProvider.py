from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleShakashakaGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str) -> Grid:
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url: str) -> Grid:
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page)
        page.wait_for_selector('div.cell')

        cells_data = page.evaluate("""() => {
            const cells = document.querySelectorAll('#game .board-back > div.cell, #game .board-back > div.shakashaka-task-cell');
            const data = [];
            cells.forEach(el => {
                const style = window.getComputedStyle(el);
                const topStr = style.top;
                const leftStr = style.left;
                if (!topStr || !leftStr || topStr === 'auto' || leftStr === 'auto') return;
                const top = parseInt(topStr);
                const left = parseInt(leftStr);
                if (isNaN(top) || isNaN(left)) return;
                const row = Math.round((top - 1) / 26);
                const col = Math.round((left - 1) / 26);
                let val = -1; // Default white
                if (el.classList.contains('shakashaka-task-cell')) {
                    if (el.classList.contains('wall')) {
                        val = -2; // Black Wall
                    } else {
                        const text = el.innerText.trim();
                        val = text !== "" ? parseInt(text) : -2;
                    }
                } else if (el.classList.contains('cell')) {
                    val = -1;
                }
                data.push({r: row, c: col, v: val});
            });
            return data;
        }""")

        if not cells_data:
            raise Exception("No cells found on the page.")

        max_r = int(max(item['r'] for item in cells_data))
        max_c = int(max(item['c'] for item in cells_data))
        rows = max_r + 1
        cols = max_c + 1

        matrix = [[-1 for _ in range(cols)] for _ in range(rows)]

        for item in cells_data:
            r, c, v = item['r'], item['c'], item['v']
            if 0 <= r < rows and 0 <= c < cols:
                matrix[r][c] = v

        return Grid(matrix)
