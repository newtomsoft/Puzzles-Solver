from playwright.sync_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class PuzzleMasyuGridPlayer(PlaywrightPlayer):
    def __init__(self, browser: BrowserContext):
        super().__init__(browser)
        self.page = self.browser.pages[0]
        self.dots = self.page.locator(".loop-dot")
        self.cell_width = self.page.locator(".loop-horizontal").nth(0).bounding_box()['width']
        self.cell_height = self.page.locator(".loop-vertical").nth(0).bounding_box()['height']
        self.columns_number = 0

    def play(self, solution: IslandGrid):
        self.columns_number = solution.columns_number
        frame = self.page.frames[0]
        video, rectangle = self._get_data_video(frame, '.board-mask', self.page, 50, 125, 50, 160)
        self._draw_path(solution)
        self.close()
        self._process_video(video, "masyu_puzzleMobiles", rectangle)

    def _draw_path(self, solution: IslandGrid):
        connected_positions = self._get_positions_from_position0_0(solution)
        for index, position in enumerate(connected_positions[:-1]):
            next_position = connected_positions[index + 1]
            direction = position.direction_to(next_position)
            self._trace_direction_from_position(direction, position)

    @staticmethod
    def _get_positions_from_position0_0(solution: IslandGrid) -> list[Position]:
        connected_positions = solution.follow_path()
        connected_positions.append(connected_positions[0])
        return connected_positions

    def _trace_direction_from_position(self, direction, position):
        index = position.r * self.columns_number + position.c
        dot = self.dots.nth(index).bounding_box()
        dot_x = dot['x'] + dot['width'] / 2
        dot_y = dot['y'] + dot['height'] / 2
        if direction == Direction.right():
            self.page.mouse.move(dot_x + self.cell_width / 2, dot_y)
        elif direction == Direction.left():
            self.page.mouse.move(dot_x - self.cell_width / 2, dot_y)
        elif direction == Direction.down():
            self.page.mouse.move(dot_x, dot_y + self.cell_height / 2)
        elif direction == Direction.up():
            self.page.mouse.move(dot_x, dot_y - self.cell_height / 2)
        self.page.mouse.down()
        self.page.mouse.up()