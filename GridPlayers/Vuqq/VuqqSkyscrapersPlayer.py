import asyncio

from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class VuqqSkyscrapersPlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        
        meta = await page.evaluate("window.vuqq_meta")
        if not meta:
            raise Exception("No Vuqq metadata found. GridProvider must run before Player.")
            
        unique_xs = meta['xs']
        unique_ys = meta['ys']

        for position, value in solution:
            if not value:
                continue
                
            col_idx = position.c
            row_idx = position.r

            x = unique_xs[col_idx + 1]
            y = unique_ys[row_idx + 1]
            
            await page.mouse.click(x, y)
            await page.keyboard.press(str(value))
            
        await asyncio.sleep(1)
