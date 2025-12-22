import math

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileRegionGridProvider import PuzzlesMobileRegionGridProvider


class PuzzleJigsawSudokuGridProvider(PlaywrightGridProvider, PuzzlesMobileRegionGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page, 'div.selectable')
        html_page = await page.content()

        regions_grid = self._scrap_region_grid(html_page)

        soup = BeautifulSoup(html_page, 'html.parser')
        cells_divs = soup.find_all('div', class_='cell')
        matrix_cells = [cell_div for cell_div in cells_divs if 'selectable' in cell_div.get('class', [])]
        numbers_divs = soup.find_all('div', class_='number')
        numbers_str = [text if (text := cell_div.text) else -1 for cell_div in numbers_divs]
        cells_count = len(matrix_cells)
        side = int(math.sqrt(cells_count))
        conversion_base = side + 1
        numbers = [int(number, conversion_base) if number != -1 else -1 for number in numbers_str]
        matrix = []
        for i in range(0, cells_count, side):
            matrix.append(numbers[i:i + side])

        return Grid(matrix), regions_grid
