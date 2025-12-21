from bs4 import BeautifulSoup, Tag
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzleBaron.Base.PuzzleBaronGridProvider import PuzzleBaronGridProvider


###### TODO: Implement the PuzzleBaronCampsitesGridProvider class ######
class PuzzleBaronCampsitesGridProvider(PlaywrightGridProvider, PuzzleBaronGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        await page.goto(url)
        await self.new_game(page, 'div.gridbox')
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cells: list[Tag] = list(soup.find_all('div', class_='gridbox'))
        trees = [-1 if 'marked3' in cell_div.get('class', []) else 0 for cell_div in cells]

        table = soup.find('table', {'id': 'campsite'})
        cells_count = len(cells)
        rows_number = len(table.find_all('tr')) - 1  # minus the footer row
        columns_number = cells_count // rows_number
        if columns_number * rows_number != cells_count:
            raise ValueError("Campsites grid parsing error")

        matrix = []
        for i in range(0, cells_count, columns_number):
            matrix.append(trees[i:i + columns_number])

        task_cells: list[Tag] = list(soup.find_all('td', class_='tdnumber'))[:-1]  # exclude the bottom right cell
        tents_numbers = [int(cell_div.getText()) for cell_div in task_cells]
        tents_numbers_by_column_row = {'column': tents_numbers[rows_number:], 'row': tents_numbers[:rows_number]}

        return Grid(matrix), tents_numbers_by_column_row
