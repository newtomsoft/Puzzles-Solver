
import asyncio

from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class VuqqKakuroPlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = self.browser.pages[0]

        meta = await page.evaluate("window.vuqq_meta")
        if not meta:
            raise Exception("No Vuqq metadata found. GridProvider must run before Player.")

        screen_xs = meta['cx']
        screen_ys = meta['cy']

        for position, value in solution:
            if value == 0:
                continue

            col_idx = position.c
            row_idx = position.r

            if col_idx >= len(screen_xs) or row_idx >= len(screen_ys):
                print(f"Skipping out of bounds write at {position}")
                continue

            x = screen_xs[col_idx]
            y = screen_ys[row_idx]

            # Click cell
            await page.mouse.click(x, y)

            # Type number
            await page.keyboard.press(str(value))

            # Short delay for stability
            # await asyncio.sleep(0.05)

        await asyncio.sleep(1)
