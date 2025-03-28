from time import sleep

from playwright.sync_api import BrowserContext, Mouse

from Domain.Direction import Direction
from Domain.Grid.Grid import Grid
from Domain.Position import Position
from GridPlayers.GridPlayer import GridPlayer


class PuzzleBaronVectorsGridPlayer(GridPlayer):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        page = browser.pages[0]
        grid_box_divs = page.query_selector_all('div.gridbox')
        numbers = [int(inner_text) if (inner_text := number_div.inner_text()) else 0 for number_div in grid_box_divs]

        for start_position, value in solution:
            if numbers[solution.get_index_from_position(start_position)] == 0:
                continue
            for direction in Direction.orthogonals():
                end_position = Position(start_position.r, start_position.c)
                while end_position in solution and solution[end_position] == value:
                    end_position = end_position.after(direction)
                end_position = end_position.before(direction)
                if end_position != start_position:
                    cls.move_and_click(page.mouse, solution, start_position, end_position, grid_box_divs)

        sleep(20)

    @classmethod
    def move_and_click(cls, mouse: Mouse, solution: Grid, start_position: Position, end_position: Position, grid_box_divs):
        start_index = solution.get_index_from_position(start_position)
        start_bounding_box = grid_box_divs[start_index].bounding_box()
        start_x = start_bounding_box['x'] + start_bounding_box['width'] / 2
        start_y = start_bounding_box['y'] + start_bounding_box['height'] / 2

        end_index = solution.get_index_from_position(end_position)
        end_bounding_box = grid_box_divs[end_index].bounding_box()
        end_x = end_bounding_box['x'] + end_bounding_box['width'] / 2
        end_y = end_bounding_box['y'] + end_bounding_box['height'] / 2

        mouse.move(start_x, start_y)
        mouse.down()
        mouse.move(end_x, end_y, steps=int(end_position.distance(start_position)))
        mouse.up()
