from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleShakashakaGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        # Wait for the game grid to be visible
        page.wait_for_selector('div.cell')

        # Puzzles-mobile style scraping
        # Extract all cells and clues
        element_data = page.evaluate("""() => {
            const divs = Array.from(document.querySelectorAll('div.cell'));
            return divs.map(d => {
                const rect = d.getBoundingClientRect();
                const style = window.getComputedStyle(d);
                return {
                    text: d.innerText,
                    class: d.className,
                    top: parseInt(style.top, 10),
                    left: parseInt(style.left, 10),
                    width: rect.width,
                    height: rect.height,
                    is_black: d.classList.contains('black') || d.style.backgroundColor === 'black' || d.classList.contains('cell-off') || d.classList.contains('immutable'),
                    # Number might be in a child span or direct text
                    number: d.innerText.trim()
                };
            });
        }""")

        return self._parse_grid_from_element_data(element_data)

    def _parse_grid_from_element_data(self, element_data):
        import math

        if not element_data:
            raise ValueError("No cells found")

        # Determine grid dimensions
        # Assuming square or rectangular grid
        # Group by top/left

        # Filter valid cells
        cells = element_data

        # Coordinates normalization
        ys = sorted(list(set(c['top'] for c in cells)))
        xs = sorted(list(set(c['left'] for c in cells)))

        rows = len(ys)
        cols = len(xs)

        if rows * cols != len(cells):
            # Maybe some cells are missing or misalignment
            # Try to map robustly
            pass

        matrix = [[-1 for _ in range(cols)] for _ in range(rows)]

        for c_data in cells:
            try:
                r = ys.index(c_data['top'])
                c = xs.index(c_data['left'])
            except ValueError:
                continue # Skip outliers

            # Identify content
            # 0-4: Numbered Black
            # -2: Empty Black (No number)
            # -1: White (Empty)

            # Check for specific classes used in Shakashaka on this site
            # Usually: 'cell-black' or 'black'
            # And inner text for number

            text = c_data['number']

            # Heuristic for Black cell
            is_black = False
            if 'black' in c_data['class'] or 'immutable' in c_data['class']:
                is_black = True

            # Check number
            if text.isdigit():
                val = int(text)
                matrix[r][c] = val # Numbered implies Black usually
            elif is_black:
                matrix[r][c] = -2 # Black, no number
            else:
                matrix[r][c] = -1 # White

        return Grid(matrix)
