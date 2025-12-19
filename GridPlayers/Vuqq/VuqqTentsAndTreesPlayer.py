import asyncio
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class VuqqTentsAndTreesPlayer(PlaywrightPlayer):
    async def play(self, solution):
        # PlaywrightPlayer stores the browser context or browser.
        # Check what 'self.browser' actually is.
        # Based on PlaywrightPlayer.py: self.browser = browser (which is type hint BrowserContext)
        # So it has .pages

        # If self.browser is BrowserContext, then .pages is correct.
        # If it is Browser, then .contexts[0].pages[0] is needed.
        # PlaywrightGridProvider uses: page = await browser.new_page().
        # Usually browser is passed to Player.

        # We try to get the first page.
        page = None
        if hasattr(self.browser, "pages") and self.browser.pages:
            page = self.browser.pages[0]
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

        # Iterate solution
        for r in range(solution.rows_number):
            for c in range(solution.columns_number):
                val = solution[r][c]

                # Assume standard behavior:
                # Left Click: Toggle Grass
                # Right Click: Toggle Tent
                # Or based on implementation details:
                # Usually: Left Click -> Grass. Right Click -> Tent.

                # Note: 'TREE' cells are fixed.
                if val == "TREE":
                    continue

                x = col_xs[c]
                y = row_ys[r]

                if val == "TENT":
                    # Place Tent
                    await page.mouse.click(x, y, button="right")
                elif val == "GRASS":
                    # Place Grass
                    await page.mouse.click(x, y, button="left")

        await asyncio.sleep(1)
