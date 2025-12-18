from bs4 import ResultSet, Tag
from playwright.async_api import BrowserContext

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileRegionGridProvider import PuzzlesMobileRegionGridProvider


class PuzzleStitchesGridProvider(PlaywrightGridProvider, PuzzlesMobileRegionGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_new_html_page(browser, url)
        regions_grid = self._scrap_region_grid(html_page)
        cell_divs, row_count, soup = self._scrap_grid_data(html_page)
        dots_by_column_row = self.clues_by_column_row(cell_divs, row_count)

        puzzle_info_text = self.get_puzzle_info_text(soup)
        puzzle_info_text_left = puzzle_info_text.split('÷')[0]
        if puzzle_info_text_left.isdigit():
            regions_connections = int(puzzle_info_text_left)
        elif '/' in puzzle_info_text_left:
            regions_connections = int(puzzle_info_text_left.split('/')[1])
        else:
            Warning(f"Can't parse regions connections from {puzzle_info_text_left} force to 1")
            regions_connections = 1

        return regions_grid, dots_by_column_row, regions_connections

    @staticmethod
    def clues_by_column_row(cell_divs: ResultSet[Tag], row_count: int) -> dict[str, list[int]]:
        task_cells = [cell_div for cell_div in cell_divs if 'task' in cell_div.get('class', [])]
        dots = [int(cell_div.text) for cell_div in task_cells]
        dots_by_column_row = {'column': dots[:row_count], 'row': dots[row_count:]}
        return dots_by_column_row
