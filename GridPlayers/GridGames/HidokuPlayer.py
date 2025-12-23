import asyncio
import logging

from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class HidokuPlayer(PlaywrightPlayer):
    async def play(self, solution: Grid) -> PlayStatus:
        page = self.browser.pages[0]

        rows = solution.rows_number
        cols = solution.columns_number

        logging.debug("starting canvas wait")
        await page.wait_for_selector("canvas", state="visible")
        logging.debug("canvas visible")

        logging.debug("starting geometry calculation")
        start_x, start_y, stride_x, stride_y = await self._get_grid_geometry(page, rows, cols)
        logging.debug("dimensions found: ", start_x, start_y, stride_x, stride_y)

        for position, value in solution:
            if not value:
                continue

            x = start_x + position.c * stride_x
            y = start_y + position.r * stride_y

            val_str = str(value)

            if len(val_str) == 1:
                await asyncio.sleep(0.5)
            await page.mouse.click(x, y)
            if len(val_str) == 1:
                await asyncio.sleep(0.5)

            for i, char in enumerate(val_str):
                await page.keyboard.press(char)

        logging.debug("Waiting for success message")
        success_element = await page.wait_for_selector("._message_112rc_40", state="visible")
        return PlayStatus.SUCCESS if success_element else PlayStatus.FAILED_NO_SUCCESS_SELECTOR

    @staticmethod
    async def _get_grid_geometry(page, rows, cols):
        canvas_info = await page.evaluate("""
            () => {
                const c = document.querySelector('canvas');
                if (!c) return null;
                const r = c.getBoundingClientRect();
                return {
                    rect: {x: r.x, y: r.y, width: r.width, height: r.height},
                    width: c.width,
                    height: c.height
                };
            }
        """)

        if not canvas_info:
            raise Exception("Canvas not found for geometry calculation")

        rect = canvas_info["rect"]
        internal_w = canvas_info["width"]
        internal_h = canvas_info["height"]

        internal_stride_x = internal_w / cols
        internal_stride_y = internal_h / rows

        internal_start_x = internal_stride_x / 2
        internal_start_y = internal_stride_y / 2

        scale_x = rect["width"] / internal_w
        scale_y = rect["height"] / internal_h

        screen_stride_x = internal_stride_x * scale_x
        screen_stride_y = internal_stride_y * scale_y

        screen_start_x = rect["x"] + (internal_start_x * scale_x)
        screen_start_y = rect["y"] + (internal_start_y * scale_y)

        return screen_start_x, screen_start_y, screen_stride_x, screen_stride_y
