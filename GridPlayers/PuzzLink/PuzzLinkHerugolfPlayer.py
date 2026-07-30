import asyncio

from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer, Point, Rectangle


class PuzzLinkHerugolfPlayer(PlaywrightPlayer):
    game_name = "herugolf"

    _ARROW_TO_DIR = {
        '↓': (1, 0),   # DOWN
        '→': (0, 1),   # RIGHT
        '↑': (-1, 0),  # UP
        '←': (0, -1),  # LEFT
    }

    async def play(self, solution) -> PlayStatus:
        page = self.browser.pages[0]
        await page.wait_for_selector("#divques svg", state="visible")
        await page.wait_for_function(
            "typeof ui !== 'undefined' && ui.puzzle && ui.puzzle.board"
        )

        video, viewport_rect = await self._get_data_video_viewport(page)
        video_rect = None

        cols = solution.columns_number
        rows = solution.rows_number

        svg = await page.wait_for_selector("#divques svg")
        bbox = await svg.bounding_box()
        x0 = bbox['x']
        y0 = bbox['y']

        viewbox_w = cols * 36 + 11
        viewbox_h = rows * 36 + 11

        if viewport_rect is not None:
            x1 = x0 - 36 * bbox['width'] / viewbox_w
            x2 = x0 + bbox['width'] + 36 * bbox['width'] / viewbox_w
            video_rect = Rectangle(Point(int(x1), viewport_rect.y1), Point(int(x2), viewport_rect.y2))

        def cell_center(r, c):
            x = x0 + (23.5 + c * 36) * bbox['width'] / viewbox_w
            y = y0 + (23.5 + r * 36) * bbox['height'] / viewbox_h
            return x, y

        arrows = []
        for position, value in solution:
            dr, dc = self._ARROW_TO_DIR.get(value, (0, 0))
            if dr == 0 and dc == 0:
                continue
            r, c = position.r, position.c
            tr, tc = r + dr, c + dc
            arrows.append((r, c, tr, tc))

        if arrows:
            for r, c, tr, tc in arrows:
                sx, sy = cell_center(r, c)
                tx, ty = cell_center(tr, tc)
                await page.mouse.move(sx, sy)
                await asyncio.sleep(0.01)
                await page.mouse.down()
                await asyncio.sleep(0.01)
                await page.mouse.move(tx, ty, steps=5)
                await asyncio.sleep(0.01)
                await page.mouse.up()
                await asyncio.sleep(0.03)

            await page.wait_for_timeout(100)

        await self.close()
        await self._process_video(video, video_rect, 0)
        return PlayStatus.SUCCESS
