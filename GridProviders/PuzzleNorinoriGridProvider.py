import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Utils.RegionsGrid import RegionsGrid


class PuzzleNorinoriGridProvider(GridProvider, PlaywrightGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.new_page()
        page.goto(url)
        html_page = page.content()
        browser.close()
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_='cell')
        cells_count = len(cell_divs)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        borders_dict = {'br': 'right', 'bl': 'left', 'bt': 'top', 'bb': 'bottom'}
        opens = {'right', 'left', 'top', 'bottom'}
        open_matrix = [[set() for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(cell_divs):
            row = i // column_count
            col = i % column_count
            cell_classes = cell.get('class', [])
            if row == 0:
                cell_classes.append('bt')
            if row == row_count - 1:
                cell_classes.append('bb')
            if col == 0:
                cell_classes.append('bl')
            if col == column_count - 1:
                cell_classes.append('br')
            cell_borders = {borders_dict[cls] for cls in cell_classes if cls in borders_dict.keys()}
            open_matrix[row][col] = opens - cell_borders

        regions_grid = RegionsGrid(open_matrix).compute_regions_grid()

        return regions_grid

