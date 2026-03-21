import re
from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridProviders.GridPuzzle.Base.GridPuzzleProvider import GridPuzzleProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleCirclesAndSquaresGridProvider(PlaywrightGridProvider, GridPuzzleProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str) -> Grid:
        return self._get_grid_from_html_tags(html_page)

    def _get_grid_from_html_tags(self, html_page: str) -> Grid:
        soup = BeautifulSoup(html_page, 'html.parser')
        matrix_cells = soup.find_all('div', class_='g_cell')
        
        if not matrix_cells:
            matrix_cells = soup.select('.grid-cell')

        cells_count = len(matrix_cells)
        size = int(cells_count ** 0.5)
        if size * size != cells_count:
            raise ValueError(f"Grid cell count {cells_count} is not a perfect square")
        
        matrix = [[None for _ in range(size)] for _ in range(size)]
        
        for i, cell in enumerate(matrix_cells):
            r, c = divmod(i, size)
            
            classes = cell.get('class', [])
            
            is_black = any(cls in ['black_circle', 'circle_black', 'b_circle', 'circle_b', 'black', 'bb_cell'] for cls in classes)
            is_white = any(cls in ['white_circle', 'circle_white', 'w_circle', 'circle_w', 'white', 'ww_cell'] for cls in classes)
            
            # Also check for child divs or spans which often contain the circle
            if not is_black:
                is_black = bool(cell.find('div', class_=re.compile(r'black|circle_b|b_circle')))
            if not is_white:
                is_white = bool(cell.find('div', class_=re.compile(r'white|circle_w|w_circle')))
            
            if is_black:
                matrix[r][c] = True
            elif is_white:
                matrix[r][c] = False
            else:
                matrix[r][c] = None
        
        return Grid(matrix)