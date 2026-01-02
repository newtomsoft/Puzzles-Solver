import re
from playwright.async_api import BrowserContext

from Domain.Board.Position import Position
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleAkariGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page, url)

    def get_grid_from_html(self, html: str, url: str) -> dict:
        # We implementation a more robust version of _get_canvas_data here
        # to handle variations in the HTML/JS structure.
        
        # Try to find size
        size_match = re.search(r'(?:gpl\.)?([Ss]ize)\s*=\s*(\d+);', html)
        if not size_match:
            raise ValueError("Could not find puzzle size in HTML")
        size = int(size_match.group(2))
        
        # Try to find pqq or pq data
        pqq_match = re.search(r'(?:gpl\.)?pq{1,2}\s*=\s*"(.*?)";', html)
        if not pqq_match:
            raise ValueError("Could not find puzzle data (pq/pqq) in HTML")
        pqq_raw = pqq_match.group(1)
        
        # Decode if base64 (using logic from Base provider)
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
