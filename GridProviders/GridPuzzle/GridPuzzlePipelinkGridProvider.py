from playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.Position import Position
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzlePipelinkGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, matrix_size = self._get_canvas_data(html_page)
        matrix = [[self.to_island(r, c, pqq_string_list[r * matrix_size + c]) for c in range(matrix_size)] for r in range(matrix_size)]
        grid = Grid(matrix)
        return grid

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


