from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from Utils.Position import Position


class PuzzleBaronVectorsGridPlayer(GridPlayer):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        page = browser.pages[0]
        grid_box_divs = page.query_selector_all('div.gridbox')
        numbers = [int(inner_text) if (inner_text := number_div.inner_text()) else 0 for number_div in grid_box_divs]

        for position, value in solution:
            index = solution.get_index(position)
            if numbers[index] == 0:
                continue

            end_position = Position(position.r, position.c)
            while end_position.up in solution and solution[end_position.up] == value:
                end_position = end_position.up
            if end_position != position:
                cls.move_and_click(end_position, grid_box_divs, index, page, solution)

            end_position = Position(position.r, position.c)
            while end_position.down in solution and solution[end_position.down] == value:
                end_position = end_position.down
            if end_position != position:
                cls.move_and_click(end_position, grid_box_divs, index, page, solution)

            end_position = Position(position.r, position.c)
            while end_position.left in solution and solution[end_position.left] == value:
                end_position = end_position.left
            if end_position != position:
                cls.move_and_click(end_position, grid_box_divs, index, page, solution)

            end_position = Position(position.r, position.c)
            while end_position.right in solution and solution[end_position.right] == value:
                end_position = end_position.right
            if end_position != position:
                cls.move_and_click(end_position, grid_box_divs, index, page, solution)

        sleep(20)

    @classmethod
    def move_and_click(cls, end_position, grid_box_divs, index, page, solution):
        start_bounding_box = grid_box_divs[index].bounding_box()
        start_x = start_bounding_box['x'] + start_bounding_box['width'] / 2
        start_y = start_bounding_box['y'] + start_bounding_box['height'] / 2

        end_bounding_box = grid_box_divs[solution.get_index(end_position)].bounding_box()
        end_x = end_bounding_box['x'] + end_bounding_box['width'] / 2
        end_y = end_bounding_box['y'] + end_bounding_box['height'] / 2

        step_x = start_bounding_box['width'] / 3 if start_x != end_x else 0
        step_y = start_bounding_box['height'] / 3 if start_y != end_y else 0

        page.mouse.move(start_x, start_y)
        page.mouse.down()
        while abs(start_x + step_x - end_x) < step_x or abs(start_y + step_y - end_y) < step_y:
            start_x += step_x
            start_y += step_y
            page.mouse.move(start_x, start_y)
        page.mouse.up()
