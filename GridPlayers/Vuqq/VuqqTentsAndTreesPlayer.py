import asyncio

from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class VuqqTentsAndTreesPlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = None
        pages = []

        if hasattr(self.browser, "pages"):
             pages.extend(self.browser.pages)
        if hasattr(self.browser, "contexts"):
             for ctx in self.browser.contexts:
                 pages.extend(ctx.pages)

        for p in pages:
            try:
                meta_check = await p.evaluate("typeof window.vuqq_meta !== 'undefined'")
                if meta_check:
                    page = p
                    break
            except Exception:
                continue

        if not page:
             if pages:
                 page = pages[0]
             else:
                 raise Exception("No active page found to play on.")

        meta = await page.evaluate("window.vuqq_meta")
        if not meta:
            raise Exception("No Vuqq metadata found. GridProvider must run before Player.")

        unique_xs = meta['col_xs']
        unique_ys = meta['row_ys']
        trees = meta.get('trees', [])
        
        tree_set = set()
        for t in trees:
            if len(t) >= 2:
                tree_set.add((t[0], t[1]))

        cols = solution.columns_number
        rows = solution.rows_number
        
        for r in range(rows):
            for c in range(cols):
                val = solution[r][c]
                
                if (r, c) in tree_set:
                    continue

                if c < len(unique_xs) and r < len(unique_ys):
                    x = unique_xs[c]
                    y = unique_ys[r]

                    if val:
                        await page.mouse.click(x, y, button="right")
                    else:
                        await page.mouse.click(x, y, button="left")

        await asyncio.sleep(1)
