from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer, Point, Rectangle


class PuzzLinkContextPlayer(PlaywrightPlayer):
    game_name = "context"

    async def play(self, solution) -> PlayStatus:
        page = self.browser.pages[0]
        svg = await page.wait_for_selector("#divques svg", state="visible", timeout=30000)
        bbox = await svg.bounding_box()
        x0 = bbox['x']
        y0 = bbox['y']
        cell_width = bbox['width'] / solution.columns_number
        cell_height = bbox['height'] / solution.rows_number

        video, viewport_rect = await self._get_data_video_viewport(page)
        x1 = int(x0 - cell_width)
        x2 = int(x0 + bbox['width'] + cell_width)
        rectangle = Rectangle(Point(x1, viewport_rect.y1), Point(x2, viewport_rect.y2))

        for position, value in solution:
            if not value:
                x = x0 + (position.c + 0.5) * cell_width
                y = y0 + (position.r + 0.5) * cell_height
                await page.mouse.click(x, y)

        await self.close()
        await self._process_video(video, rectangle, 0)
        return PlayStatus.SUCCESS
