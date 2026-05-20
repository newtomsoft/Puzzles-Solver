import math
from bs4 import BeautifulSoup
from rebrowser_playwright.async_api import BrowserContext

from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleAkariGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str) -> dict:
        soup = BeautifulSoup(html_page, 'html.parser')
        puzzle_main = soup.find('div', class_='puzzle_main')
        if not puzzle_main:
            # Fallback: try the old JS-based extraction
            return self._get_grid_from_js(html_page)

        cells = puzzle_main.find_all('div', class_='p_cell')
        if not cells:
            return self._get_grid_from_js(html_page)

        total_cells = len(cells)
        size = int(math.sqrt(total_cells))
        if size * size != total_cells:
            return self._get_grid_from_js(html_page)

        black_cells = []
        number_constraints = {}

        for i, cell in enumerate(cells):
            r = i // size
            c = i % size
            cell_classes = cell.get('class', [])

            if 'cell_bl' in cell_classes:
                pos = (r, c)
                black_cells.append(pos)
                text = cell.get_text(strip=True)
                if text.isdigit():
                    number_constraints[pos] = int(text)

        return {
            'columns_number': size,
            'rows_number': size,
            'black_cells': black_cells,
            'number_constraints': number_constraints
        }

    def _get_grid_from_js(self, html_page: str) -> dict:
        """Fallback to the old JS-variable extraction."""
        import re

        size_match = re.search(r'(?:gpl\.|plz\.)?([Ss]ize)\s*=\s*(\d+);', html_page)
        if not size_match:
            raise ValueError("Could not find puzzle size in HTML")
        size = int(size_match.group(2))

        pqq_match = re.search(r'(?:gpl\.|plz\.)?pq{1,2}\s*=\s*"(.*?)";', html_page)
        if not pqq_match:
            raise ValueError("Could not find puzzle data (pq/pqq) in HTML")
        pqq_raw = pqq_match.group(1)

        pqq_string = self._decode_if_custom_base64(pqq_raw)
        pqq_string_list = self._split_to_list(pqq_string, size)

        black_cells = []
        number_constraints = {}

        for i in range(len(pqq_string_list)):
            r = i // size
            c = i % size
            char = pqq_string_list[i]

            if char == '.':
                pass
            elif char in '01234':
                pos = (r, c)
                black_cells.append(pos)
                number_constraints[pos] = int(char)
            elif char == '5':
                pos = (r, c)
                black_cells.append(pos)

        return {
            'columns_number': size,
            'rows_number': size,
            'black_cells': black_cells,
            'number_constraints': number_constraints
        }
