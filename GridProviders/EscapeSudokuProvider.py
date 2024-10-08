import math

from playwright.sync_api import sync_playwright, BrowserContext

from Grid import Grid
from GridProviders.GridProvider import GridProvider
from PlaywrightGridProvider import PlaywrightGridProvider
from Utils.utils import is_perfect_square


class EscapeSudokuGridProvider(GridProvider, PlaywrightGridProvider):
    def scrap_grid(self, browser: BrowserContext, url):
        pass

    def get_grid(self, source: str):
        with sync_playwright() as playwright:
            config = self.get_config()
            headless = config['DEFAULT']['headless'] == 'True'
            user_data_dir = 'D:\\Boulot\\projets info\\PuzzleGames\\GridProviders\\Chromium\\user'  # todo
            extension_path = 'D:\\Boulot\\projets info\\PuzzleGames\\GridProviders\\Chromium\\1.0.13_0'  # todo
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir,
                headless=headless,
                args=[f'--disable-extensions-except={extension_path}', f'--load-extension={extension_path}']
            )
            page = browser.new_page()
            page.goto(source)
            page.wait_for_selector('div.game-boxes')
            slot_divs = page.query_selector_all('div.slot')
            cells_count = len(slot_divs)
            matrix_size = int(math.sqrt(cells_count))
            if is_perfect_square(matrix_size):
                sub_square_row_number = int(math.sqrt(matrix_size))
                sub_square_column_number = sub_square_row_number
            elif matrix_size == 6:
                sub_square_row_number = 2
                sub_square_column_number = 3
            elif matrix_size == 12:
                sub_square_row_number = 3
                sub_square_column_number = 4
            elif matrix_size == 21:
                sub_square_row_number = 3
                sub_square_column_number = 3
            else:
                browser.close()
                raise ValueError("Sudoku subgrid unknown")
            numbers_str = [
                EscapeSudokuGridProvider.get_span_inner_text(span) if (span := slot_div.query_selector('span.value')) else -1
                for slot_div in slot_divs
            ]
            matrix = [[-1 for _ in range(matrix_size)] for _ in range(matrix_size)]
            index = 0
            for sub_square_row in range(0, matrix_size, sub_square_row_number):
                for sub_square_col in range(0, matrix_size, sub_square_column_number):
                    for r in range(sub_square_row_number):
                        for c in range(sub_square_column_number):
                            matrix[sub_square_row + r][sub_square_col + c] = EscapeSudokuGridProvider.convert_to_int_or_keep(numbers_str[index])
                            index += 1
            browser.close()
            return Grid(matrix)

    @staticmethod
    def get_span_inner_text(span):
        inner_text = span.inner_text()
        return EscapeSudokuGridProvider.convert_to_int_or_keep(inner_text) if inner_text != '' else span.query_selector('img').get_attribute('alt')

    @staticmethod
    def convert_to_int_or_keep(entry: str) -> int | str:
        try:
            return int(entry)
        except ValueError:
            return entry
