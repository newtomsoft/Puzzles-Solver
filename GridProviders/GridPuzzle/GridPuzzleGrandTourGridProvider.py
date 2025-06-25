import base64
import re

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.Position import Position
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridProvider import GridPuzzleGridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleGrandTourGridProvider(GridProvider, GridPuzzleGridProvider, PlaywrightGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        qv_string_list, qh_string_list, size = self._get_canvas_data(html_page)
        grid_v = Grid([[bool(int(qv_string_list[i * (size + 1) + j])) for j in range(size + 1)] for i in range(size)])
        grid_h = Grid([[bool(int(qh_string_list[i * size + j])) for j in range(size)] for i in range(size + 1)])
        grid_size = size + 1
        grid = Grid([[0 for _ in range(grid_size)] for _ in range(grid_size)])

        for position, _ in grid:
            if (not position in grid_v or not grid_v[position]) and (not position in grid_h or not grid_h[position]):
                continue
            bridge_down_count = 1 if position in grid_v and grid_v[position] else 0
            bridge_right_count = 1 if position in grid_h and grid_h[position] else 0
            position_bridges_count: dict[Position, int] = {}
            if position in grid_v and grid_v[position]:
                position_bridges_count[position.down] = 1
            if position in grid_h and grid_h[position]:
                position_bridges_count[position.right] = 1
            island = Island(position, bridge_down_count + bridge_right_count, position_bridges_count)
            island.set_bridges_count_according_to_directions_bridges()
            grid.set_value(position, island)

        return grid

    @staticmethod
    def _get_canvas_data(html_page: str) -> tuple[list[str], list[str], int]:
        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        size = int(re.search(r'gpl\.([Ss]ize) = (\d+);', html_string).group(2))
        qv = re.search(r'gpl\.qv = "(.*?)";', html_string).group(1)
        qh = re.search(r'gpl\.qh = "(.*?)";', html_string).group(1)
        qv_string = GridPuzzleGrandTourGridProvider._decode_if_custom_base64(qv)
        qh_string = GridPuzzleGrandTourGridProvider._decode_if_custom_base64(qh)
        qv_string_list = GridPuzzleGrandTourGridProvider._split_to_list(qv_string)
        qh_string_list = GridPuzzleGrandTourGridProvider._split_to_list(qh_string)
        return qv_string_list, qh_string_list, size

    @staticmethod
    def _decode_if_custom_base64(string: str) -> str:
        if len(string) < 4 or not GridPuzzleGrandTourGridProvider._is_valid_base64(string[3:]):
            return string

        decoded = base64.b64decode(string[3:])
        return decoded.decode('utf-8', errors='ignore')

    @staticmethod
    def _is_valid_base64(string: str) -> bool:
        return len(string) % 4 == 0 and bool(re.match('^[A-Za-z0-9+/]*={0,2}$', string))

    @staticmethod
    def _split_to_list(string: str) -> list[str]:
        split_pipe = string.split('|')
        if len(split_pipe) > 1:
            return split_pipe
        return [string[i:i + 1] for i in range(len(string))]
