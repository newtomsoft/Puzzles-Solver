import math

from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Slant.SlantSolver import SlantSolver
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleSlantGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page, 'div.cell')

        element_data = await page.evaluate("""() => {
            const divs = Array.from(document.querySelectorAll('div.cell, div.immutable, div.clue, div[class*="number"], div.task'));
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

        return self._parse_grid_from_element_data(element_data)

    @staticmethod
    def _parse_grid_from_element_data(element_data):
        cells = [d for d in element_data if 'cell' in d['class']]
        if not cells:
            raise ValueError("No cells found")

        cell_count = len(cells)
        rows_number = int(round(math.sqrt(cell_count)))
        
        if rows_number * rows_number != cell_count:
            lower_bound = int(math.sqrt(cell_count))
            upper_bound = lower_bound + 1
            
            if lower_bound * lower_bound == cell_count:
                rows_number = lower_bound
            elif upper_bound * upper_bound == cell_count:
                rows_number = upper_bound
            else:
                raise ValueError(f"Cell count {cell_count} is not a perfect square. Expected {rows_number*rows_number} cells for {rows_number}x{rows_number} grid")
        
        clue_rows = rows_number + 1
        clue_cols = rows_number + 1
        clues_matrix = [[SlantSolver.empty for _ in range(clue_cols)] for _ in range(clue_rows)]

        clue_candidates = [d for d in element_data if 'task' in d['class'] or (d['text'].strip().isdigit() and 'cell' not in d['class'])]

        min_top = min(d['top'] for d in cells)
        min_left = min(d['left'] for d in cells)

        sorted_lefts = sorted(list(set(d['left'] for d in cells)))
        cell_width = sorted_lefts[1] - sorted_lefts[0] if len(sorted_lefts) > 1 else 50

        sorted_tops = sorted(list(set(d['top'] for d in cells)))
        cell_height = sorted_tops[1] - sorted_tops[0] if len(sorted_tops) > 1 else 50

        for clue in clue_candidates:
            text = clue['text'].strip()
            if not text.isdigit():
                continue
            
            clue_center_top = clue['top'] + (clue['height'] / 2)
            clue_center_left = clue['left'] + (clue['width'] / 2)

            r = int(round((clue_center_top - min_top) / cell_height))
            c = int(round((clue_center_left - min_left) / cell_width))

            if 0 <= r < clue_rows and 0 <= c < clue_cols:
                clues_matrix[r][c] = int(text)

        return Grid(clues_matrix)
