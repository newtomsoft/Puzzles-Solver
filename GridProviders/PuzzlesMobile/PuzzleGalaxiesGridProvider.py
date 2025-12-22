from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Position import Position
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleGalaxiesGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page, 'div.loop-dot')
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')

        cells = soup.find_all('div', class_='loop-task-cell')
        rows_number = sum(1 for cell in cells if 'left: 2px' in cell['style'])
        columns_number = sum(1 for cell in cells if 'top: 2px' in cell['style'])
        grid_size = (rows_number, columns_number)

        offset = 14
        cell_size = 29
        white_dots = soup.find_all('div', class_='dot-white')
        circles_positions = {
            index + 1: Position((float(dot['style'].split('top: ')[1].split('px')[0]) - offset) / cell_size, (float(dot['style'].split('left: ')[1].split('px')[0]) - offset) / cell_size)
            for index, dot in enumerate(white_dots)
        }
        return grid_size, circles_positions
