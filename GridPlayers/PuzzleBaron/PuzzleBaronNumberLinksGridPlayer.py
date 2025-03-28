from time import sleep

from playwright.sync_api import BrowserContext, Mouse

from Domain.Grid.Grid import Grid
from Domain.Position import Position
from GridPlayers.GridPlayer import GridPlayer


class PuzzleBaronNumberLinksGridPlayer(GridPlayer):
    @classmethod
    def play(cls, solution: Grid, browser: BrowserContext):
        page = browser.pages[0]
        grid_box_divs = page.query_selector_all('div.gridbox')
        numbers = [int(inner_text) if (inner_text := number_div.inner_text()) else -1 for number_div in grid_box_divs]

        numbers_processed = set()
        for start_position, start_value in solution:
            if numbers[solution.get_index_from_position(start_position)] == -1 or start_value in numbers_processed:
                continue
            numbers_processed.add(start_value)
            positions_processed = {start_position}
            cls.mouse_move(page.mouse, solution, start_position, grid_box_divs)
            cls.mouse_down(page.mouse)
            next_position = cls._next_position(solution, start_position, start_value, positions_processed)
            while next_position:
                positions_processed.add(next_position)
                cls.mouse_move(page.mouse, solution, next_position, grid_box_divs)
                next_position = cls._next_position(solution, next_position, start_value, positions_processed)
        cls.mouse_up(page.mouse)
        sleep(20)

    @classmethod
    def mouse_move(cls, mouse: Mouse, solution: Grid, next_position: Position, grid_box_divs):
        end_index = solution.get_index_from_position(next_position)
        end_bounding_box = grid_box_divs[end_index].bounding_box()
        end_x = end_bounding_box['x'] + end_bounding_box['width'] / 2
        end_y = end_bounding_box['y'] + end_bounding_box['height'] / 2
        mouse.move(end_x, end_y)

    @classmethod
    def _next_position(cls, solution: Grid[int], start_position: Position, start_value: int, positions_processed: set[Position]) -> Position:
        return next((neighbor_position for neighbor_position in solution.neighbors_positions(start_position) if neighbor_position not in positions_processed and solution[neighbor_position] == start_value), None)

    @classmethod
    def mouse_down(cls, mouse):
        mouse.down()

    @classmethod
    def mouse_up(cls, mouse):
        mouse.up()
