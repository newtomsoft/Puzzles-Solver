import asyncio
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class HidokuPlayer(PlaywrightPlayer):
    async def play(self, solution: Grid):
        page = self.browser.pages[0]
            
        rows = solution.rows_number
        cols = solution.columns_number

        await page.wait_for_selector("canvas", state="visible")
        
        start_x, start_y, stride_x, stride_y = await self._get_grid_geometry(page, rows, cols)

        for position, value in solution:
            if not value: continue

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

        pass

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

        rect = canvas_info['rect']
        internal_w = canvas_info['width']
        internal_h = canvas_info['height']

        internal_stride_x = internal_w / cols
        internal_stride_y = internal_h / rows
        
        internal_start_x = internal_stride_x / 2
        internal_start_y = internal_stride_y / 2
        
        scale_x = rect['width'] / internal_w
        scale_y = rect['height'] / internal_h

        screen_stride_x = internal_stride_x * scale_x
        screen_stride_y = internal_stride_y * scale_y
        
        screen_start_x = rect['x'] + (internal_start_x * scale_x)
        screen_start_y = rect['y'] + (internal_start_y * scale_y)
        
        return screen_start_x, screen_start_y, screen_stride_x, screen_stride_y
