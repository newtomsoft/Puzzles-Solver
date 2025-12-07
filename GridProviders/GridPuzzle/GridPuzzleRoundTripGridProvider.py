from playwright.sync_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.Position import Position
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleRoundTripGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        pqq_string_list, up_down_right_left, matrix_size = self._get_canvas_data_extended2(html_page)
        matrix = [[self.to_island(r, c, pqq_string_list[r * matrix_size + c]) for c in range(matrix_size)] for r in range(matrix_size)]
        grid = Grid(matrix)

        clues = self.transform_to_dict(up_down_right_left)

        return grid, clues

    @staticmethod
    def to_island(r: int, c: int, island_car_code: str):
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

    @staticmethod
    def transform_to_dict(up_down_right_left: list[list[int]]):
        return {
            Direction.down(): up_down_right_left[0],
            Direction.up(): up_down_right_left[1],
            Direction.right(): up_down_right_left[2],
            Direction.left(): up_down_right_left[3]
        }