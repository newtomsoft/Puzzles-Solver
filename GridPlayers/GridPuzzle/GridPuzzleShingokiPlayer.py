from time import sleep

from playwright.sync_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class GridPuzzleShingokiPlayer(GridPlayer, PlaywrightGridPlayer):
    @classmethod
    def play(cls, solution: IslandGrid, browser: BrowserContext):
        cell_height, cell_width, page, x0, y0 = cls._get_canvas_data(browser, solution)
        video, rectangle = cls._get_data_video_viewport(page)

        connected_positions = cls._get_positions_from_position0_0(solution)
        for index, position in enumerate(connected_positions[:-1]):
            next_position = connected_positions[index + 1]
            direction = position.direction_to(next_position)
            cls._trace_direction_from_position(direction, position, page, cell_width, cell_height, x0, y0)

        sleep(3)
        browser.close()
        cls._process_video(video, "shingoki", rectangle)

    @classmethod
    def _get_positions_from_position0_0(cls, solution: IslandGrid) -> list[Position]:
        connected_positions = solution.follow_path()
        connected_positions.append(connected_positions[0])
        return connected_positions

    @classmethod
    def _trace_direction_from_position(cls, direction, position, page, cell_width, cell_height, x0, y0):
        if direction == Direction.right():
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.down()
            page.mouse.move(x0 + cell_width / 2 + (position.c + 1) * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.up()
            return
        if direction == Direction.down():
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.down()
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + (position.r + 1) * cell_height)
            page.mouse.up()
            return
        if direction == Direction.left():
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.down()
            page.mouse.move(x0 + cell_width / 2 + (position.c - 1) * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            return
        if direction == Direction.up():
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.down()
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + (position.r - 1) * cell_height)
            return
