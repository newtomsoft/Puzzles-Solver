from abc import ABC

from playwright.async_api import BrowserContext, Mouse

from Board.Grid import Grid
from Board.Position import Position


class PlaywrightGridPlayer(ABC):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        pass

    @classmethod
    def mouse_move(cls, mouse: Mouse, solution: Grid, position: Position, cell_divs):
        index = solution.get_index_from_position(position)
        bounding_box = cell_divs[index].bounding_box()
        x = bounding_box['x'] + bounding_box['width'] / 2
        y = bounding_box['y'] + bounding_box['height'] / 2
        mouse.move(x, y)

    @classmethod
    def move_start_down_move_end_up(cls, mouse: Mouse, solution: Grid, start_position: Position, end_position: Position, cell_divs):
        start_index = solution.get_index_from_position(start_position)
        start_bounding_box = cell_divs[start_index].bounding_box()
        start_x = start_bounding_box['x'] + start_bounding_box['width'] / 2
        start_y = start_bounding_box['y'] + start_bounding_box['height'] / 2

        end_index = solution.get_index_from_position(end_position)
        end_bounding_box = cell_divs[end_index].bounding_box()
        end_x = end_bounding_box['x'] + end_bounding_box['width'] / 2
        end_y = end_bounding_box['y'] + end_bounding_box['height'] / 2

        mouse.move(start_x, start_y)
        mouse.down()
        mouse.move(end_x, end_y, steps=int(end_position.distance(start_position)))
        mouse.up()

    @classmethod
    def mouse_down(cls, mouse):
        mouse.down()

    @classmethod
    def mouse_up(cls, mouse):
        mouse.up()
