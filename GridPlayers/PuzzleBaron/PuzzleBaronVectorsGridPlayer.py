from time import sleep

from playwright.sync_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Position import Position
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class PuzzleBaronVectorsGridPlayer(PlaywrightGridPlayer):
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
                    cls.move_start_down_move_end_up(page.mouse, solution, start_position, end_position, grid_box_divs)

        sleep(20)
