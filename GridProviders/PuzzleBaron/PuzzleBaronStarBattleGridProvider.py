import math

from bs4 import BeautifulSoup, Tag
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronGridProvider import PuzzleBaronGridProvider
from Utils.RegionsGrid import RegionsGrid


class PuzzleBaronStarBattleGridProvider(GridProvider, PlaywrightGridProvider, PuzzleBaronGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, '#playing_board')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        grid_box_divs: list[Tag] = list(soup.find_all('div', class_='box'))
        cells_count = len(grid_box_divs)
        rows_count = int(math.sqrt(cells_count))
        columns_count = rows_count
        if rows_count * columns_count != cells_count:
            raise ValueError("The grid must be square")

        regions_grid = self._get_regions_grid(rows_count, grid_box_divs)
        stars_number = self._get_stars_number(soup)

        return regions_grid, stars_number

    @staticmethod
    def _get_regions_grid(column_count, cells: list[Tag]) -> RegionsGrid:
        row_count = column_count
        open_matrix = PuzzleBaronStarBattleGridProvider._build_open_borders_matrix(row_count, column_count, cells)
        return RegionsGrid(open_matrix)

    @staticmethod
    def _build_open_borders_matrix(row_count, column_count, cells: list[Tag]) -> list[list[set]]:
        open_matrix = [[set() for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(cells):
            row = i // column_count
            col = i % column_count
            open_borders = PuzzleBaronStarBattleGridProvider._get_open_borders(cell)
            open_matrix[row][col] = open_borders

        return open_matrix

    @staticmethod
    def _get_open_borders(cell: Tag) -> set[str]:
        closed_borders = set([cls.removeprefix("border_") for cls in cell.get('class') if cls.startswith('border_') and not cls.endswith('_thick')])
        all_borders = {'right', 'left', 'top', 'bottom'}
        return all_borders - closed_borders

    @staticmethod
    def _get_stars_number(soup: BeautifulSoup):
        div_stars_number = soup.find_all('div', class_='header_font')[1]
        stars_number_text = div_stars_number.get_text()
        stars_number = stars_number_text.count("★")
        return stars_number
