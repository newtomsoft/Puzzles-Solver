import base64
import math
import re

from bs4 import BeautifulSoup, ResultSet, PageElement, Tag, NavigableString


class GridPuzzleGridProvider:
    @staticmethod
    def get_html(browser, url, board_selector: str | None = None):
        page = browser.pages[0]
        page.set_viewport_size({"width": 685, "height": 900})
        page.goto(url)
        html_page = page.content()
        if not board_selector:
            return html_page
        div_to_view = page.query_selector(board_selector)
        div_to_view.scroll_into_view_if_needed()
        return html_page

    @staticmethod
    def get_canvas_data(html_page):
        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        size = int(re.search(r'gpl\.Size = (\d+);', html_string).group(1))
        pqq_base64 = re.search(r'gpl\.pqq = "(.*?)";', html_string).group(1)
        pqq_raw = base64.b64decode(pqq_base64[3:])
        pqq_string = pqq_raw.decode('utf-8', errors='ignore')
        pqq_string_list = pqq_string.split('|')
        return pqq_string_list, size

    @staticmethod
    def _get_grid_data(html_page: str) -> tuple[BeautifulSoup, int, int, list[list], ResultSet[PageElement | Tag | NavigableString]]:
        soup = BeautifulSoup(html_page, 'html.parser')
        matrix_cells = soup.find_all('div', class_='g_cell')
        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        matrix = [[0 for _ in range(column_count)] for _ in range(row_count)]
        return soup, row_count, column_count, matrix, matrix_cells
