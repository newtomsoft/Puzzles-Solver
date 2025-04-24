import base64
import re

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class GridPuzzleNumberChainGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        html_page = page.content()
        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        size = int(re.search(r'gpl\.Size = (\d+);', html_string).group(1))
        pqq_base64 = re.search(r'gpl\.pqq = "(.*?)";', html_string).group(1)
        pqq_raw = base64.b64decode(pqq_base64[3:])
        pqq_string = pqq_raw.decode('utf-8', errors='ignore')
        pqq_string_list = pqq_string.split('|')
        matrix = [[int(pqq_string_list[i * size + j]) for j in range(size)] for i in range(size)]
        return Grid(matrix)
