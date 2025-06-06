from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class PuzzleMasyuGridPlayer(PlaywrightPlayer):
    def play(self, solution: IslandGrid):
        page = self.browser.pages[0]
        dots = page.locator(".loop-dot")
        cell_width = page.locator(".loop-horizontal").nth(0).bounding_box()['width']
        cell_height = page.locator(".loop-vertical").nth(0).bounding_box()['height']

        self._draw_path(dots, page, solution, cell_width, cell_height)
        self.close()
        # self._process_video(video, "shingoki", rectangle)

    def _draw_path(self, dots, page, solution, cell_width, cell_height):
        connected_positions = self._get_positions_from_position0_0(solution)
        for index, position in enumerate(connected_positions[:-1]):
            next_position = connected_positions[index + 1]
            direction = position.direction_to(next_position)
            self._trace_direction_from_position(direction, position, page, dots, solution.columns_number, cell_width, cell_height)

    @staticmethod
    def _get_positions_from_position0_0(solution: IslandGrid) -> list[Position]:
        connected_positions = solution.follow_path()
        connected_positions.append(connected_positions[0])
        return connected_positions

    @staticmethod
    def _trace_direction_from_position(direction, position, page, dots, columns_number, cell_width, cell_height):
        index = position.r * columns_number + position.c
        dot = dots.nth(index).bounding_box()
        dot_x = dot['x'] + dot['width'] / 2
        dot_y = dot['y'] + dot['height'] / 2
        if direction == Direction.right():
            page.mouse.move(dot_x + cell_width / 2, dot_y)
            page.mouse.down()
            page.mouse.up()
            return
        if direction == Direction.left():
            page.mouse.move(dot_x -  cell_width / 2, dot_y)
            page.mouse.down()
            page.mouse.up()
            return
        if direction == Direction.down():
            page.mouse.move(dot_x, dot_y + cell_height/ 2)
            page.mouse.down()
            page.mouse.up()
            return
        if direction == Direction.up():
            page.mouse.move(dot_x, dot_y - cell_height / 2)
            page.mouse.down()
            page.mouse.up()
            return
