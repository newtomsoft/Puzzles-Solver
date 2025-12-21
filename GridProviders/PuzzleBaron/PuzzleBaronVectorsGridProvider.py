from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzleBaron.Base.PuzzleBaronGridProvider import PuzzleBaronGridProvider


class PuzzleBaronVectorsGridProvider(PlaywrightGridProvider, PuzzleBaronGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        await page.goto(url)
        await self.new_game(page, 'div.gridbox')
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        grid_box_divs = soup.find_all('div', class_='gridbox')
        numbers = [int(text) if ((text := number_div.get_text()) != '') else '' for number_div in grid_box_divs]
        cells_count = len(grid_box_divs)
        rows_count = len(soup.find('table', class_='numberlink').find_all_next('tr'))
        columns_count = cells_count // rows_count
        matrix = []
        for i in range(0, cells_count, columns_count):
            matrix.append(numbers[i:i + columns_count])
        return Grid(matrix)
