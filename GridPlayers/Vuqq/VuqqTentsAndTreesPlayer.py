import asyncio

from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class VuqqTentsAndTreesPlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = None
        if hasattr(self.browser, "pages") and self.browser.pages:
            found_page = None
            for p in self.browser.pages:
                try:
                    logs_check = await p.evaluate("typeof window.vuqq_logs !== 'undefined'")
                    if logs_check:
                        page = p
                        break
                except:
                    continue
            
            if not page:
                 page = self.browser.pages[0] # Default Fallback
        
        elif hasattr(self.browser, "contexts") and self.browser.contexts:
             if self.browser.contexts[0].pages:
                 page = self.browser.contexts[0].pages[0]

        if not page:
            # Fallback: maybe we need to create one? No, Player plays on existing page.
            raise Exception("No active page found to play on.")

        # We need to re-parse logs to get coordinates because solution Grid might be a copy without metadata
        # or we simply rely on the page state which is preserved.
        logs = await page.evaluate("window.vuqq_logs")
        if not logs:
            raise Exception("No logs found. GridProvider must run before Player.")

        texts = [l for l in logs if l["type"] == "text"]
        xs = [t["x"] for t in texts]
        ys = [t["y"] for t in texts]
        max_x = max(xs)
        max_y = max(ys)

        row_clues = sorted([t for t in texts if abs(t["x"] - max_x) < 5], key=lambda t: t["y"])
        col_clues = sorted([t for t in texts if abs(t["y"] - max_y) < 5], key=lambda t: t["x"])

        row_ys = [t["y"] for t in row_clues]
        col_xs = [t["x"] for t in col_clues]

        rects = [l for l in logs if l["type"] == "rect"]
        
        # Find Trees (same logic as Provider)
        trunks = [r for r in rects if r.get("colour") == 3]
        tree_positions = set()
        
        cols = solution.columns_number
        rows = solution.rows_number
        
        for trunk in trunks:
            tx, ty = trunk["x"], trunk["y"]
            trunk_cx = tx + trunk["w"] / 2
            trunk_cy = ty + trunk["h"] / 2

            # Find closest cell
            if col_xs and row_ys:
                c = min(range(cols), key=lambda i: abs(col_xs[i] - trunk_cx))
                r = min(range(rows), key=lambda i: abs(row_ys[i] - trunk_cy))
                tree_positions.add((r, c))

        # Iterate solution
        for r in range(solution.rows_number):
            for c in range(solution.columns_number):
                val = solution[r][c]
                
                # Check if this is a tree known from logs
                if (r, c) in tree_positions:
                    continue

                if c < len(col_xs) and r < len(row_ys):
                    x = col_xs[c]
                    y = row_ys[r]

                    if val: # True = Tent
                        # Place Tent
                        await page.mouse.click(x, y, button="right")
                    else: # False = Grass (or empty)
                        # Place Grass
                        await page.mouse.click(x, y, button="left")

        await asyncio.sleep(1)
