from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleMasyuGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page, 'div.loop-dot')
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        dot_divs = soup.find_all('div', class_='loop-dot')
        rows_number = sum(1 for cell in dot_divs if 'left: 0px' in cell['style'])
        columns_number = sum(1 for cell in dot_divs if 'top: 0px' in cell['style'])
        matrix = [[' ' for _ in range(columns_number)] for _ in range(rows_number)]
        for index, dot_div in enumerate(dot_divs):
            row = index // columns_number
            column = index % columns_number
            if 'dot-white' in dot_div['class']:
                matrix[row][column] = 'w'
                continue
            if 'dot-black' in dot_div['class']:
                matrix[row][column] = 'b'

        return Grid(matrix)
