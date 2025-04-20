import re

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext, Page

from Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Domain.Board.RegionsGrid import RegionsGrid


class VingtMinutesKemaruGridProvider(GridProvider, PlaywrightGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page)
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cells = soup.find_all('g', class_='grid-cell')
        matrix_cells = [cell for cell in cells]
        rects_x0 = soup.find_all('rect', {'x': '0'})
        row_count = len(rects_x0)
        cells_count = len(matrix_cells)
        column_count = cells_count // row_count

        numbers_str = [text if (text := matrix_cell.get_text()) else 0 for matrix_cell in matrix_cells]
        numbers = [int(number) if number != 0 else 0 for number in numbers_str]

        cells_with_color = soup.find_all('g', class_=re.compile(r'grid-cell--color-\d+'))
        color_numbers = []
        for cell in cells_with_color:
            classes = cell.get('class', [])
            for class_name in classes:
                match = re.match(r'grid-cell--color-(\d+)', class_name)
                if match:
                    color_number = int(match.group(1))
                    color_numbers.append(color_number)
                    break

        matrix_number = []
        matrix_color = []
        for i in range(0, cells_count, column_count):
            matrix_number.append(numbers[i:i + column_count])
            matrix_color.append(color_numbers[i:i + column_count])
        grid_numbers = Grid(matrix_number)
        regions_grid = Grid(matrix_color)

        shapes1 = regions_grid.get_all_shapes(1, 'orthogonal')
        shapes2 = regions_grid.get_all_shapes(2, 'orthogonal')
        shapes3 = regions_grid.get_all_shapes(3, 'orthogonal')
        shapes4 = regions_grid.get_all_shapes(4, 'orthogonal')

        shapes = set()
        for shape in shapes1:
            shapes.add(shape)
        for shape2 in shapes2:
            shapes.add(shape2)
        for shape3 in shapes3:
            shapes.add(shape3)
        for shape4 in shapes4:
            shapes.add(shape4)

        for index_shape, positions_region in enumerate(shapes):
            for position in positions_region:
                regions_grid[position[0]][position[1]] = index_shape + 1

        return grid_numbers, regions_grid

    @staticmethod
    def new_game(page: Page, selector_to_waite='grid-cell'):
        new_game_button = page.locator('[data-test-id="action-button-start-puzzle"]')
        if new_game_button.count() > 0:
            new_game_button.click()
            page.wait_for_selector(selector_to_waite)

