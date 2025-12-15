from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileRegionGridProvider import PuzzlesMobileRegionGridProvider


class PuzzleStarBattleGridProvider(PlaywrightGridProvider, PuzzlesMobileRegionGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        page.wait_for_selector('div.cell')
        PuzzlesMobileGridProvider.new_game(page)
        html_page = page.content()

        regions_grid = self._scrap_region_grid(html_page)

        soup = BeautifulSoup(html_page, 'html.parser')
        puzzle_info_text = self.get_puzzle_info_text(soup)
        puzzle_info_text_left = puzzle_info_text.split('★')[0]
        if puzzle_info_text_left.isdigit():
            stars_count_by_region_column_row = int(puzzle_info_text_left)
        elif '/' in puzzle_info_text_left:
            stars_count_by_region_column_row = int(puzzle_info_text_left.split('/')[1])
        else:
            Warning(f"Can't parse regions connections from {puzzle_info_text_left} force to 1")
            stars_count_by_region_column_row = 1
        return regions_grid, stars_count_by_region_column_row
