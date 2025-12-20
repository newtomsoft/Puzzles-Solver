import asyncio

from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class VuqqTentsAndTreesPlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = None
        pages = []

        # Collect all pages from browser and contexts
        if hasattr(self.browser, "pages"):
             pages.extend(self.browser.pages)
        if hasattr(self.browser, "contexts"):
             for ctx in self.browser.contexts:
                 pages.extend(ctx.pages)

        # Find the page with our metadata
        for p in pages:
            try:
                meta_check = await p.evaluate("typeof window.vuqq_meta !== 'undefined'")
                if meta_check:
                    page = p
                    break
            except:
                continue

        if not page:
             # Fallback to first page if available
             if pages:
                 page = pages[0]
             else:
                 raise Exception("No active page found to play on.")

        # Get metadata
        meta = await page.evaluate("window.vuqq_meta")
        if not meta:
            raise Exception("No Vuqq metadata found. GridProvider must run before Player.")

        unique_xs = meta['col_xs']
        unique_ys = meta['row_ys']
        trees = meta.get('trees', []) # list of [r, c] pairs
        
        # Convert trees to set of tuples for efficient lookup
        tree_set = set()
        for t in trees:
            if len(t) >= 2:
                tree_set.add((t[0], t[1]))

        cols = solution.columns_number
        rows = solution.rows_number
        
        # Iterate solution and play
        for r in range(rows):
            for c in range(cols):
                val = solution[r][c]
                
                # Check if this is a tree known from metadata
                if (r, c) in tree_set:
                    continue

                if c < len(unique_xs) and r < len(unique_ys):
                    x = unique_xs[c]
                    y = unique_ys[r]

                    if val: # True = Tent
                        # Place Tent
                        await page.mouse.click(x, y, button="right")
                    else: # False = Grass (or empty)
                        # Place Grass
                        await page.mouse.click(x, y, button="left")

        await asyncio.sleep(1)
