import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleSlantGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.cell')

        # Inject JS to get computed styles for precise positioning
        element_data = page.evaluate("""() => {
            const divs = Array.from(document.querySelectorAll('div.cell, div.immutable, div.clue, div[class*="number"]'));
            return divs.map(d => {
                const rect = d.getBoundingClientRect();
                const style = window.getComputedStyle(d);
                return {
                    text: d.innerText,
                    class: d.className,
                    top: parseInt(style.top, 10),
                    left: parseInt(style.left, 10),
                    width: rect.width,
                    height: rect.height
                };
            });
        }""")

        # Process data
        # Assume cells are div.cell and clues are something else or implicitly found by position
        cells = [d for d in element_data if 'cell' in d['class']]

        if not cells:
             raise ValueError("No cells found")

        rows_number = int(math.sqrt(len(cells)))

        # Grid dimensions for clues: (rows_number + 1) x (columns_number + 1)
        clue_rows = rows_number + 1
        clue_cols = rows_number + 1 # Assuming square

        clues_matrix = [['' for _ in range(clue_cols)] for _ in range(clue_rows)]

        # We need to map clues to grid coordinates.
        # Clues are at intersections.
        # Find all elements that look like clues (digits)
        clue_candidates = [d for d in element_data if d['text'].strip().isdigit()]

        if not clue_candidates:
            # Maybe clues are empty? Or failed to find them.
            # If it's an empty grid (user just started), return empty clues.
            return Grid(clues_matrix)

        # Determine coordinates based on top/left
        # We need to normalize positions.
        # Find min top and left from cells to establish origin.
        min_top = min(d['top'] for d in cells)
        min_left = min(d['left'] for d in cells)

        # Estimate cell size
        # Sort by top then left
        cells.sort(key=lambda x: (x['top'], x['left']))

        # Distance between adjacent cells
        # This is likely the cell size.
        # We can also use width/height if available.
        # Let's assume standard grid layout.

        # If we have N cells, we have sqrt(N) rows.
        # Clues are at intersections.
        # Intersection (r, c) is at top-left of cell (r, c).
        # Intersection (r+1, c+1) is at bottom-right of cell (r, c).

        # Let's use cell positions to bucket clues.
        # Cell (r, c) at (left, top).
        # Clue (r, c) should be near (left, top) of cell (r, c).
        # Clue (r+1, c+1) should be near (left + width, top + height).

        # Actually, simpler:
        # Clues are at vertices.
        # We can just cluster the 'top' and 'left' values of clues.

        # Collect all tops and lefts of clues
        tops = sorted([d['top'] for d in clue_candidates])
        lefts = sorted([d['left'] for d in clue_candidates])

        # But we need to assign them to integer grid coords 0..N
        # We can use the cell grid as reference.
        # Cell (0,0) top/left corresponds to intersection (0,0).
        # Cell width/height gives stride.

        cell_0 = cells[0]
        # Check if there is a clue near cell_0.top, cell_0.left

        # Let's try to infer grid parameters from cells
        # Group cells by top to find rows
        # This is standard logic I can borrow/reimplement better.

        # Calculate cell size
        # Find smallest non-zero difference in lefts
        sorted_lefts = sorted(list(set(d['left'] for d in cells)))
        cell_width = sorted_lefts[1] - sorted_lefts[0] if len(sorted_lefts) > 1 else 50 # Fallback

        sorted_tops = sorted(list(set(d['top'] for d in cells)))
        cell_height = sorted_tops[1] - sorted_tops[0] if len(sorted_tops) > 1 else 50

        # Tolerance
        tol = cell_width / 4

        for clue in clue_candidates:
            # Find nearest grid intersection
            # Relative to min_left, min_top
            # Note: clues might be offset slightly

            # r index = round((clue.top - min_top) / cell_height)
            # c index = round((clue.left - min_left) / cell_width)

            r = int(round((clue['top'] - min_top) / cell_height))
            c = int(round((clue['left'] - min_left) / cell_width))

            # Validate bounds
            if 0 <= r < clue_rows and 0 <= c < clue_cols:
                clues_matrix[r][c] = int(clue['text'])

        return Grid(clues_matrix)
