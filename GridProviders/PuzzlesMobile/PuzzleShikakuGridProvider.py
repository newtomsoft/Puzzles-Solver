from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleShikakuGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page, 'div.cell')
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_='cell')
        rows_number = sum(1 for cell in cell_divs if 'left: 3px' in cell['style'])
        columns_number = sum(1 for cell in cell_divs if 'top: 3px' in cell['style'])
        cells_count = len(cell_divs)
        if columns_number * rows_number != cells_count:
            raise ValueError("Shikaku grid parsing error")
        numbers = [int(inner_text) if (inner_text := cell_div.get_text()) else -1 for cell_div in cell_divs]
        matrix = []
        for i in range(0, cells_count, columns_number):
            matrix.append(numbers[i:i + columns_number])
        return Grid(matrix)
