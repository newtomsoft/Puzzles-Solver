import re

from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleObitaruGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str) -> Grid:
        html_string = self._prettify_html(html_page)
        size_match = re.search(r'gpl\.([Ss]ize)\s*=\s*(\d+);', html_string)
        if not size_match:
            size_match = re.search(r'size\s*:\s*(\d+)', html_string)
        size = int(size_match.group(2 if size_match.group(0).startswith('gpl') else 1))

        pqq_match = re.search(r'gpl\.pqq\s*=\s*"(.*?)";', html_string)
        pqq = pqq_match.group(1)
        pqq_string = self._decode_if_custom_base64(pqq)
        values = pqq_string.split('|')
        # GridPuzzle omits trailing empty cells; pad with '.'
        while len(values) < size * size:
            values.append('.')

        matrix = [[self._convert_to_domain(values[i * size + j]) for j in range(size)] for i in range(size)]
        return Grid(matrix)

    @staticmethod
    def _convert_to_domain(cell_code: str):
        if cell_code == 'W':
            return 'w'
        if cell_code == '.':
            return None
        if cell_code.isdigit():
            return int(cell_code)
        # Fallback for any other black-circle encoding
        return cell_code

    @staticmethod
    def _prettify_html(html_page: str) -> str:
        from bs4 import BeautifulSoup
        return BeautifulSoup(html_page, 'html.parser').prettify()
