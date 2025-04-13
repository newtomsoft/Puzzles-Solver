from time import sleep

from playwright.sync_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from GridPlayers.GridPlayer import GridPlayer


class GridPuzzleShingokiGridPlayer(GridPlayer):
    @classmethod
    def play(cls, solution: IslandGrid, browser: BrowserContext):
        page = browser.pages[0]
        rows_number = solution.rows_number
        columns_number = solution.columns_number
        bounded_box = page.locator("canvas").bounding_box()
        x0 = bounded_box['x']
        y0 = bounded_box['y']
        width = bounded_box['width']
        height = bounded_box['height']
        cell_width = width / columns_number
        cell_height = height / rows_number
        for island in solution.islands.values():
            if Direction.right() in island.direction_position_bridges:
                page.mouse.move(x0 + cell_width / 2 + island.position.c * cell_width, y0 + cell_height / 2 + island.position.r * cell_height)
                page.mouse.down()
                page.mouse.move(x0 + cell_width / 2 + (island.position.c + 1) * cell_width, y0 + cell_height / 2 + island.position.r * cell_height)
                page.mouse.up()
            if Direction.down() in island.direction_position_bridges:
                page.mouse.move(x0 + cell_width / 2 + island.position.c * cell_width, y0 + cell_height / 2 + island.position.r * cell_height)
                page.mouse.down()
                page.mouse.move(x0 + cell_width / 2 + island.position.c * cell_width, y0 + cell_height / 2 + (island.position.r + 1) * cell_height)
                page.mouse.up()
        sleep(3)
