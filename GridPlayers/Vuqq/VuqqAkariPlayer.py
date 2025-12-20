
import asyncio
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer

class VuqqAkariPlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = self.browser.pages[0]

        meta = await page.evaluate("window.vuqq_meta")
        if not meta:
            raise Exception("No Vuqq metadata found. GridProvider must run before Player.")

        unique_xs = meta['xs']
        unique_ys = meta['ys']

        # solution is a Grid object (or iterable yielding (pos, val))
        # AkariSolver returns 1 for Bulb, 0 for Empty.

        for position, value in solution:
            if value == 1: # Bulb
                col_idx = position.c
                row_idx = position.r

                if col_idx < len(unique_xs) and row_idx < len(unique_ys):
                    # We need to click the cell.
                    # Coordinates in meta are top-left of the cell.
                    # Click center.
                    x = unique_xs[col_idx] + 50
                    y = unique_ys[row_idx] + 50

                    await page.mouse.click(x, y)
                    # Small delay to ensure click registers
                    # await asyncio.sleep(0.05)

        # Final sleep to let user see result
        await asyncio.sleep(1)
