
import json
from collections import defaultdict

from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class VuqqAkariGridProvider(PlaywrightGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = await browser.new_page()

        await page.goto(url)
        await page.wait_for_load_state('networkidle')

        # Inject hook to capture fillText and fillRect calls
        await page.evaluate("""
            (() => {
                window.capturedTexts = [];
                window.capturedRects = [];
                const originalFillText = CanvasRenderingContext2D.prototype.fillText;
                const originalFillRect = CanvasRenderingContext2D.prototype.fillRect;

                CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
                    window.capturedTexts.push({text: text, x: x, y: y});
                    return originalFillText.apply(this, arguments);
                };

                CanvasRenderingContext2D.prototype.fillRect = function(x, y, w, h) {
                    window.capturedRects.push({x: x, y: y, w: w, h: h, style: this.fillStyle});
                    return originalFillRect.apply(this, arguments);
                };
            })();
        """)

        # Trigger a redraw
        if await page.is_visible('.game-new'):
            await page.click('.game-new')
        elif await page.is_visible('.game-restart'):
            await page.click('.game-restart')

        # Wait for canvas to be redrawn
        await page.wait_for_timeout(1000)

        captured_texts = await page.evaluate("window.capturedTexts")
        captured_rects = await page.evaluate("window.capturedRects")

        if not captured_rects:
             # Try resizing to force redraw
             await page.set_viewport_size({"width": 1000, "height": 1000})
             await page.wait_for_timeout(500)
             captured_texts = await page.evaluate("window.capturedTexts")
             captured_rects = await page.evaluate("window.capturedRects")

        if not captured_rects:
            raise Exception("No rects captured from canvas.")

        # Filter relevant rects (cells are usually 100x100)
        # Background is usually the largest one.
        # Cells: w=100, h=100 (approx)
        cells = [r for r in captured_rects if 95 <= r['w'] <= 105 and 95 <= r['h'] <= 105]

        if not cells:
             raise Exception("No cell-sized rects found.")

        # Determine grid size
        xs = sorted(list(set([c['x'] for c in cells])))
        ys = sorted(list(set([c['y'] for c in cells])))

        def cluster(values, tolerance=10):
            if not values: return []
            clusters = []
            curr = [values[0]]
            for v in values[1:]:
                if v - curr[-1] < tolerance:
                    curr.append(v)
                else:
                    clusters.append(sum(curr)/len(curr))
                    curr = [v]
            clusters.append(sum(curr)/len(curr))
            return clusters

        unique_xs = cluster([c['x'] for c in cells])
        unique_ys = cluster([c['y'] for c in cells])

        rows = len(unique_ys)
        cols = len(unique_xs)

        # Initialize Grid with -1 (White)
        matrix = [[-1 for _ in range(cols)] for _ in range(rows)]

        # Map Black cells (-2)
        # We saw '#000000' for black cells in inspection.
        # But wait, cells with numbers might be black too.
        # Actually, Akari only has White (Empty) and Black (Wall).
        # Black can have number or not.
        # We need to identify Black cells.

        # Helper to find index
        def get_index(val, clusters):
            for i, c in enumerate(clusters):
                if abs(val - c) < 20:
                    return i
            return -1

        for c in cells:
            r = get_index(c['y'], unique_ys)
            c_idx = get_index(c['x'], unique_xs)

            if r != -1 and c_idx != -1:
                # Check style.
                # White: #f3f4f8 (or close to it)
                # Black: #000000 (or close to it)
                style = str(c['style']).lower()
                if style != '#f3f4f8' and style != '#ffffff':
                    matrix[r][c_idx] = -2  # Black, potentially with number
                else:
                    matrix[r][c_idx] = -1 # White

        # Map Clues (0-4) onto Black cells
        # Text coords are centered.
        # We can map text x/y to cell indices.
        # Text x ~ cell x + 50. Text y ~ cell y + 50.

        for t in captured_texts:
            try:
                val = int(t['text'])
                tx = t['x']
                ty = t['y']

                # Find which cell contains this text
                # We can reuse unique_xs/ys but with offset
                # If cell x is 1, center is 51.
                # So we look for index where unique_xs[i] is close to tx - 50

                c_idx = get_index(tx - 50, unique_xs)
                r_idx = get_index(ty - 50, unique_ys)

                if c_idx != -1 and r_idx != -1:
                    matrix[r_idx][c_idx] = val
            except ValueError:
                pass

        grid = Grid(matrix)

        # Pass metadata to player
        metadata = {'xs': unique_xs, 'ys': unique_ys}
        await page.evaluate(f"window.vuqq_meta = {json.dumps(metadata)}")

        return grid
