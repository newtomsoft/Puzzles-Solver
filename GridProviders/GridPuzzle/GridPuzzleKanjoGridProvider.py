import re

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.Position import Position
from Domain.Puzzles.Kanjo.KanjoSolver import KanjoSolver
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleKanjoGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        pqq_string_list, board_string_list, matrix_size = self._get_canvas_data_Kanjo(html_page)
        matrix = [[self._convert(r, c, pqq_string_list[r * matrix_size + c], board_string_list[r * matrix_size + c]) for c in range(matrix_size)] for r in range(matrix_size)]
        grid = Grid(matrix)

        return grid

    @staticmethod
    def _get_canvas_data_Kanjo(html_page: str) -> tuple[list[str], list[str], int]:
        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        size = int(re.search(r'gpl\.([Ss]ize) = (\d+);', html_string).group(2))
        pqq = re.search(r'gpl\.pq{1,2} = "(.*?)";', html_string).group(1)
        pqq_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(pqq)
        pqq_string_list = GridPuzzleGridCanvasProvider._split_to_list(pqq_string, size)
        board = re.search(r'gpl\.board = "(.*?)";', html_string).group(1)
        board_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(board)
        board_string_list = GridPuzzleGridCanvasProvider._split_to_list(board_string, size)

        return pqq_string_list, board_string_list, size

    @staticmethod
    def _convert(r: int, c: int, pqq_string: str, board_string: str):
        if pqq_string == '-':
            return KanjoSolver.horizontal
        if pqq_string == '|':
            return KanjoSolver.vertical
        if pqq_string.isdigit():
            return int(pqq_string)
        return GridPuzzleKanjoGridProvider._to_island(r, c, board_string)

    @staticmethod
    def _to_island(r: int, c: int, island_car_code: str):
        position = Position(r, c)
        initial_position_bridges = {
            position.up: 0,
            position.down: 0,
            position.left: 0,
            position.right: 0,
        }
        island = Island(position, 0, initial_position_bridges)
        match island_car_code:
            case '|':
                island.set_bridge_to_direction(Direction.up(), 1)
                island.set_bridge_to_direction(Direction.down(), 1)
            case '-':
                island.set_bridge_to_direction(Direction.left(), 1)
                island.set_bridge_to_direction(Direction.right(), 1)
            case '+':
                island.set_bridge_to_direction(Direction.up(), 1)
                island.set_bridge_to_direction(Direction.down(), 1)
                island.set_bridge_to_direction(Direction.left(), 1)
                island.set_bridge_to_direction(Direction.right(), 1)
            case '1':
                island.set_bridge_to_direction(Direction.up(), 1)
                island.set_bridge_to_direction(Direction.right(), 1)
            case '2':
                island.set_bridge_to_direction(Direction.down(), 1)
                island.set_bridge_to_direction(Direction.right(), 1)
            case '3':
                island.set_bridge_to_direction(Direction.left(), 1)
                island.set_bridge_to_direction(Direction.down(), 1)
            case '4':
                island.set_bridge_to_direction(Direction.up(), 1)
                island.set_bridge_to_direction(Direction.left(), 1)

        island.set_bridges_count_according_to_directions_bridges()
        return island
