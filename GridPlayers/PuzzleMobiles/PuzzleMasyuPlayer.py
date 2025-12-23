import asyncio

from playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class PuzzleMasyuPlayer(PuzzlesMobilePlayer):
    game_name = "masyu_puzzleMobiles"
    def __init__(self, browser: BrowserContext):
        super().__init__(browser)
        self.page = self.browser.pages[0]
        self.dots = self.page.locator(".loop-dot")
        self.cell_width = 0
        self.cell_height = 0
        self.columns_number = 0

    async def play(self, solution: IslandGrid) -> PlayStatus:
        self.columns_number = solution.columns_number
        self.cell_width = (await self.page.locator(".loop-horizontal").nth(0).bounding_box())['width']
        self.cell_height = (await self.page.locator(".loop-vertical").nth(0).bounding_box())['height']

        frame = self.page.frames[0]
        video, rectangle = await self._get_data_video(frame, '.board-mask', self.page, 50, 125, 50, 160)
        await self._draw_path(solution)

        await asyncio.sleep(2)
        result = await self.submit_score(self.page)
        await asyncio.sleep(3)

        await self.close()
        self._process_video(video, rectangle)

        return result

    async def _draw_path(self, solution: IslandGrid):
        connected_positions = self._get_positions_from_position0_0(solution)
        for index, position in enumerate(connected_positions[:-1]):
            next_position = connected_positions[index + 1]
            direction = position.direction_to(next_position)
            await self._trace_direction_from_position(direction, position)

    @staticmethod
    def _get_positions_from_position0_0(solution: IslandGrid) -> list[Position]:
        connected_positions = solution.follow_path()
        connected_positions.append(connected_positions[0])
        return connected_positions

    async def _trace_direction_from_position(self, direction, position):
        index = position.r * self.columns_number + position.c
        dot = await self.dots.nth(index).bounding_box()
        dot_x = dot['x'] + dot['width'] / 2
        dot_y = dot['y'] + dot['height'] / 2
        if direction == Direction.right():
            await self.page.mouse.move(dot_x + self.cell_width / 2, dot_y)
        elif direction == Direction.left():
            await self.page.mouse.move(dot_x - self.cell_width / 2, dot_y)
        elif direction == Direction.down():
            await self.page.mouse.move(dot_x, dot_y + self.cell_height / 2)
        elif direction == Direction.up():
            await self.page.mouse.move(dot_x, dot_y - self.cell_height / 2)
        await self.page.mouse.down()
        await self.page.mouse.up()
