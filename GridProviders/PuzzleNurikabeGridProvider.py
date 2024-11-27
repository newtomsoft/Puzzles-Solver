from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from PlaywrightGridProvider import PlaywrightGridProvider
from Utils.Grid import Grid


class PuzzleNurikabeGridProvider(GridProvider, PlaywrightGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.new_page()
        page.goto(url)
        html_page = page.content()
        browser.close()
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_=['cell', 'nurikabe-task-cell'])
        rows_number = sum(1 for cell in cell_divs if 'left: 1px' in cell['style'])
        columns_number = sum(1 for cell in cell_divs if 'top: 1px' in cell['style'])
        cells_count = len(cell_divs)
        if columns_number * rows_number != cells_count:
            raise ValueError("Nurikabe grid parsing error")
        numbers = [int(inner_text) if (inner_text := cell_div.get_text()) else 0 for cell_div in cell_divs]
        matrix = []
        for i in range(0, cells_count, columns_number):
            matrix.append(numbers[i:i + columns_number])
        return Grid(matrix)
